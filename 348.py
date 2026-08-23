#!/usr/bin/env python3
"""Proof of concept for dynamic deterministic boundaries around LLM agents.

This module implements the mechanism described in :mod:`patent.md` as a small,
dependency-free, executable prototype.  The prototype deliberately separates two
ideas that are easy to conflate:

* **Consequence** answers *which operations must be protected*.  Consequential
  sinks are derived from machine-readable tool contracts plus runtime state.
* **Enforcement cost** answers *where protection is cheapest*.  Candidate gate
  nodes receive reproducible integer costs derived from the controls required by
  all consequential operations reachable from that node.

The graph analyzer then finds a minimum-cost *vertex* cut between probabilistic
request nodes and consequential tool nodes.  It does so by splitting every
workflow vertex ``v`` into ``v:in -> v:out`` and running Edmonds--Karp max flow.
Eligible candidate nodes receive their computed gate cost on that internal edge;
all other internal edges and all ordinary workflow edges receive an effectively
infinite capacity.  By max-flow/min-cut duality, the resulting edge cut identifies
the cheapest set of workflow vertices at which deterministic gates can intercept
every consequential path.

The second half of the module demonstrates what happens *at* one such boundary.
An untrusted, structured LLM refund proposal is normalized to a canonical action,
bound to a ledger snapshot, checked against evidence and policy, executed with an
idempotency key, post-condition checked, and summarized in a hash-linked execution
certificate.

This is educational POC code, not a production payment or security component.
Important simplifications include an in-memory executor, SHA-256 integrity hashes
without digital signatures, estimated rather than measured telemetry, no durable
transaction/lock manager, and a structured proposal instead of a production-grade
parser.  These limitations are made explicit because a demo that merely *looks*
safe is worse than one whose trust boundaries are visible.

Run the narrated demonstration::

    python3 348.py

Run the embedded unit tests::

    python3 348.py --test

The implementation uses only the Python standard library (Python 3.10+).
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import sys
import unittest
from collections import deque
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any, Iterable, Mapping, Sequence


# ---------------------------------------------------------------------------
# Canonical serialization and hashing
# ---------------------------------------------------------------------------


def _canonical_value(value: Any) -> Any:
    """Convert ``value`` into the deliberately small canonical JSON domain.

    Deterministic certificates are only useful if equivalent values serialize to
    identical bytes.  The standard JSON encoder already supports sorted mapping
    keys, but it does not define how sets, enums, or dataclasses should be encoded.
    This helper makes those choices explicit and rejects floats.  Financial values
    in this POC are integer cents; silently accepting an IEEE-754 float would make
    an avoidable ambiguity part of a security-sensitive identifier.

    The function is intentionally strict.  Extending it is possible, but each new
    type becomes part of the canonicalization protocol and therefore should be
    versioned in a real system.
    """

    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        raise TypeError("floating-point values are forbidden in canonical data")
    if isinstance(value, Enum):
        return _canonical_value(value.value)
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {
            item.name: _canonical_value(getattr(value, item.name))
            for item in dataclasses.fields(value)
        }
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("canonical mappings require string keys")
            result[key] = _canonical_value(item)
        return result
    if isinstance(value, (set, frozenset)):
        normalized = [_canonical_value(item) for item in value]
        return sorted(
            normalized,
            key=lambda item: json.dumps(
                item, sort_keys=True, separators=(",", ":"), ensure_ascii=False
            ),
        )
    if isinstance(value, (list, tuple)):
        return [_canonical_value(item) for item in value]
    raise TypeError(f"unsupported canonical value: {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    """Return the version-independent canonical JSON byte representation."""

    return json.dumps(
        _canonical_value(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def sha256_document(value: Any) -> str:
    """Hash a canonical document and return a lowercase hexadecimal digest."""

    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _ceil_div(numerator: int, denominator: int) -> int:
    """Integer ceiling division used by the fixed-point cost model."""

    if numerator < 0 or denominator <= 0:
        raise ValueError("ceiling division requires numerator >= 0 and denominator > 0")
    return (numerator + denominator - 1) // denominator


# ---------------------------------------------------------------------------
# Machine-readable tool contracts and runtime effects
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EffectDescriptor:
    """Static side-effect metadata supplied by a tool owner.

    Merely giving a workflow node a name such as ``send_message`` or ``refund`` is
    not enough for automated analysis.  A contract explicitly states the kinds of
    effects that invocation can produce.  The runtime state below can suppress a
    real effect for a verified dry run or change the number of affected targets.
    """

    writes_external_state: bool
    financial: bool = False
    availability_impact: bool = False
    sensitive_data_disclosure: bool = False
    reversible: bool = True
    default_fanout: int = 1

    def __post_init__(self) -> None:
        if self.default_fanout < 0:
            raise ValueError("default_fanout must be non-negative")

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> "EffectDescriptor":
        """Parse and type-check an effect descriptor from a JSON-like mapping."""

        def boolean(name: str, default: bool) -> bool:
            value = document.get(name, default)
            if not isinstance(value, bool):
                raise TypeError(f"effects.{name} must be a boolean")
            return value

        fanout = document.get("default_fanout", 1)
        if not isinstance(fanout, int) or isinstance(fanout, bool):
            raise TypeError("effects.default_fanout must be an integer")
        return cls(
            writes_external_state=boolean("writes_external_state", False),
            financial=boolean("financial", False),
            availability_impact=boolean("availability_impact", False),
            sensitive_data_disclosure=boolean(
                "sensitive_data_disclosure", False
            ),
            reversible=boolean("reversible", True),
            default_fanout=fanout,
        )


@dataclass(frozen=True)
class ToolRuntimeState:
    """Verified runtime facts that can change a tool's effective consequence."""

    enabled: bool = True
    dry_run: bool = False
    target_count: int | None = None
    environment: str = "production"
    state_version: str = "state/v1"

    def __post_init__(self) -> None:
        if self.target_count is not None and self.target_count < 0:
            raise ValueError("target_count must be non-negative")


@dataclass(frozen=True)
class ToolContract:
    """A validated tool schema used by both graph analysis and runtime gating."""

    name: str
    effects: EffectDescriptor
    required_permission: str
    required_inputs: frozenset[str]
    validators: frozenset[str]
    state_dependencies: frozenset[str]
    deterministic_controls: frozenset[str]
    version: str

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> "ToolContract":
        """Ingest a compact machine-readable contract.

        Contract parsing is kept strict so malformed metadata cannot quietly make
        a consequential tool look harmless.  A production registry would also
        authenticate the publisher and enforce schema/version compatibility.
        """

        def string(name: str) -> str:
            value = document.get(name)
            if not isinstance(value, str) or not value:
                raise TypeError(f"tool contract {name!r} must be a non-empty string")
            return value

        def string_set(name: str) -> frozenset[str]:
            value = document.get(name, [])
            if not isinstance(value, list) or any(
                not isinstance(item, str) or not item for item in value
            ):
                raise TypeError(f"tool contract {name!r} must be a list of strings")
            return frozenset(value)

        effects = document.get("effects")
        if not isinstance(effects, Mapping):
            raise TypeError("tool contract 'effects' must be a mapping")
        return cls(
            name=string("name"),
            effects=EffectDescriptor.from_document(effects),
            required_permission=string("required_permission"),
            required_inputs=string_set("required_inputs"),
            validators=string_set("validators"),
            state_dependencies=string_set("state_dependencies"),
            deterministic_controls=string_set("deterministic_controls"),
            version=string("version"),
        )

    def is_consequential(self, runtime: ToolRuntimeState) -> bool:
        """Return whether this invocation is a consequential sink *right now*.

        ``dry_run`` is trusted only because ``runtime`` is assumed to come from a
        verified tool adapter, not from the LLM.  If a provider's so-called dry run
        can mutate state, its contract must still describe it as consequential.
        """

        if not runtime.enabled or runtime.dry_run:
            return False
        effects = self.effects
        return any(
            (
                effects.writes_external_state,
                effects.financial,
                effects.availability_impact,
                effects.sensitive_data_disclosure,
            )
        )

    def effective_fanout(self, runtime: ToolRuntimeState) -> int:
        """Return verified target count, falling back to the contract default."""

        if runtime.target_count is not None:
            return runtime.target_count
        return self.effects.default_fanout

    def to_document(self) -> Mapping[str, Any]:
        """Return a stable representation suitable for policy digests."""

        return {
            "name": self.name,
            "effects": self.effects,
            "required_permission": self.required_permission,
            "required_inputs": self.required_inputs,
            "validators": self.validators,
            "state_dependencies": self.state_dependencies,
            "deterministic_controls": self.deterministic_controls,
            "version": self.version,
        }

    @property
    def digest(self) -> str:
        return sha256_document(self.to_document())


# ---------------------------------------------------------------------------
# Workflow graph and boundary-candidate facts
# ---------------------------------------------------------------------------


class NodeKind(str, Enum):
    """Coarse workflow role; capabilities, not labels, determine eligibility."""

    REQUEST = "request"
    PROBABILISTIC = "probabilistic"
    CANDIDATE = "candidate_action"
    ACTION = "tool_action"
    ADVISORY = "advisory"


@dataclass(frozen=True)
class NodeTelemetry:
    """Measured or estimated resources for enforcing a gate at one node.

    These quantities are facts, not final weights.  Keeping raw telemetry separate
    from :class:`CostPolicy` lets an auditor replay a cost computation under the
    exact policy version used for boundary placement.
    """

    canonicalization_cpu_us: int = 0
    checkpoint_bytes: int = 0
    semantic_action_classes: int = 1
    expected_review_basis_points: int = 0

    def __post_init__(self) -> None:
        values = (
            self.canonicalization_cpu_us,
            self.checkpoint_bytes,
            self.semantic_action_classes,
            self.expected_review_basis_points,
        )
        if any(value < 0 for value in values):
            raise ValueError("node telemetry values must be non-negative")
        if self.expected_review_basis_points > 10_000:
            raise ValueError("review probability cannot exceed 10,000 basis points")


@dataclass(frozen=True)
class WorkflowNode:
    """One node plus the verified facts available at that workflow location.

    No ``eligible=True`` switch exists.  Eligibility is derived later by comparing
    these capabilities with the union of downstream enforcement requirements.
    This is the POC's answer to the transcript's main outstanding question: avoid
    manually labelling boundary nodes whenever the required facts can be derived.
    """

    node_id: str
    kind: NodeKind
    tool_name: str | None = None
    known_inputs: frozenset[str] = field(default_factory=frozenset)
    canonicalizable_tools: frozenset[str] = field(default_factory=frozenset)
    available_validators: frozenset[str] = field(default_factory=frozenset)
    available_state_dependencies: frozenset[str] = field(default_factory=frozenset)
    available_controls: frozenset[str] = field(default_factory=frozenset)
    authorization_context_available: bool = False
    already_executed: bool = False
    telemetry: NodeTelemetry = field(default_factory=NodeTelemetry)

    def __post_init__(self) -> None:
        if not self.node_id:
            raise ValueError("workflow node IDs must be non-empty")
        if self.kind is NodeKind.ACTION and not self.tool_name:
            raise ValueError("tool-action nodes require tool_name")
        if self.kind is not NodeKind.ACTION and self.tool_name is not None:
            raise ValueError("only tool-action nodes may set tool_name")

    def to_document(self) -> Mapping[str, Any]:
        return {
            "node_id": self.node_id,
            "kind": self.kind,
            "tool_name": self.tool_name,
            "known_inputs": self.known_inputs,
            "canonicalizable_tools": self.canonicalizable_tools,
            "available_validators": self.available_validators,
            "available_state_dependencies": self.available_state_dependencies,
            "available_controls": self.available_controls,
            "authorization_context_available": self.authorization_context_available,
            "already_executed": self.already_executed,
            "telemetry": self.telemetry,
        }


class WorkflowGraph:
    """A small directed graph with deterministic serialization and traversal."""

    def __init__(self) -> None:
        self._nodes: dict[str, WorkflowNode] = {}
        self._successors: dict[str, set[str]] = {}

    @property
    def nodes(self) -> Mapping[str, WorkflowNode]:
        return self._nodes

    def add_node(self, node: WorkflowNode) -> None:
        if node.node_id in self._nodes:
            raise ValueError(f"duplicate workflow node: {node.node_id}")
        self._nodes[node.node_id] = node
        self._successors[node.node_id] = set()

    def add_edge(self, source: str, target: str) -> None:
        if source not in self._nodes or target not in self._nodes:
            raise KeyError(f"edge endpoint missing: {source!r} -> {target!r}")
        self._successors[source].add(target)

    def successors(self, node_id: str) -> tuple[str, ...]:
        return tuple(sorted(self._successors[node_id]))

    def predecessors(self) -> Mapping[str, tuple[str, ...]]:
        result: dict[str, list[str]] = {node_id: [] for node_id in self._nodes}
        for source, targets in self._successors.items():
            for target in targets:
                result[target].append(source)
        return {
            node_id: tuple(sorted(sources)) for node_id, sources in result.items()
        }

    def edges(self) -> tuple[tuple[str, str], ...]:
        return tuple(
            sorted(
                (source, target)
                for source, targets in self._successors.items()
                for target in targets
            )
        )

    def to_document(self) -> Mapping[str, Any]:
        return {
            "nodes": [self._nodes[node_id].to_document() for node_id in sorted(self._nodes)],
            "edges": self.edges(),
        }

    @property
    def digest(self) -> str:
        return sha256_document(self.to_document())


# ---------------------------------------------------------------------------
# Enforcement-contract derivation, eligibility, and fixed-point gate costs
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EnforcementContract:
    """Union of requirements for consequential actions below a candidate node."""

    action_nodes: frozenset[str]
    tool_names: frozenset[str]
    required_inputs: frozenset[str]
    required_permissions: frozenset[str]
    validators: frozenset[str]
    state_dependencies: frozenset[str]
    deterministic_controls: frozenset[str]
    total_target_count: int

    def to_document(self) -> Mapping[str, Any]:
        return dataclasses.asdict(self)


@dataclass(frozen=True)
class EligibilityAssessment:
    """Replayable explanation of why one graph node can or cannot host a gate."""

    eligible: bool
    reasons: tuple[str, ...]
    enforcement_contract: EnforcementContract | None


@dataclass(frozen=True)
class GateCostBreakdown:
    """Integer cost components used as a node's internal-edge capacity."""

    gate_setup: int
    canonicalization: int
    requirements: int
    checkpoint: int
    coordination: int
    expected_review: int

    @property
    def total(self) -> int:
        return sum(
            (
                self.gate_setup,
                self.canonicalization,
                self.requirements,
                self.checkpoint,
                self.coordination,
                self.expected_review,
            )
        )

    def to_document(self) -> Mapping[str, int]:
        result = dataclasses.asdict(self)
        result["total"] = self.total
        return result


@dataclass(frozen=True)
class CostPolicy:
    """Versioned, integer-only weighting policy for deterministic enforcement.

    The units are illustrative "cost points."  A production system could map them
    to latency, CPU, I/O, lock time, storage, and human-review measurements, or use
    lexicographic optimization.  Integer arithmetic avoids platform-dependent
    rounding and makes repeated analysis bit-for-bit reproducible.
    """

    version: str = "cost-policy/2026-08-poc-v1"
    gate_setup_cost: int = 100
    cpu_us_per_cost_unit: int = 100
    semantic_class_cost: int = 20
    required_input_cost: int = 3
    validator_cost: int = 12
    permission_check_cost: int = 10
    state_dependency_cost: int = 5
    deterministic_control_cost: int = 8
    checkpoint_bytes_per_cost_unit: int = 4_096
    extra_action_coordination_cost: int = 20
    extra_target_coordination_cost: int = 4
    review_at_100_percent_cost: int = 200

    def __post_init__(self) -> None:
        numeric_values = [
            value
            for item in dataclasses.fields(self)
            if item.name != "version"
            for value in (getattr(self, item.name),)
        ]
        if any(not isinstance(value, int) or value < 0 for value in numeric_values):
            raise ValueError("cost weights must be non-negative integers")
        if self.cpu_us_per_cost_unit == 0 or self.checkpoint_bytes_per_cost_unit == 0:
            raise ValueError("cost quantization divisors must be positive")

    def price(
        self, node: WorkflowNode, contract: EnforcementContract
    ) -> GateCostBreakdown:
        """Derive a reproducible capacity from telemetry and requirements."""

        telemetry = node.telemetry
        canonicalization = _ceil_div(
            telemetry.canonicalization_cpu_us, self.cpu_us_per_cost_unit
        ) + telemetry.semantic_action_classes * self.semantic_class_cost

        requirements = (
            len(contract.required_inputs) * self.required_input_cost
            + len(contract.validators) * self.validator_cost
            + len(contract.required_permissions) * self.permission_check_cost
            + len(contract.state_dependencies) * self.state_dependency_cost
            + len(contract.deterministic_controls)
            * self.deterministic_control_cost
        )

        checkpoint = _ceil_div(
            telemetry.checkpoint_bytes, self.checkpoint_bytes_per_cost_unit
        )
        coordination = (
            max(0, len(contract.action_nodes) - 1)
            * self.extra_action_coordination_cost
            + max(0, contract.total_target_count - len(contract.action_nodes))
            * self.extra_target_coordination_cost
        )
        expected_review = _ceil_div(
            telemetry.expected_review_basis_points
            * self.review_at_100_percent_cost,
            10_000,
        )
        return GateCostBreakdown(
            gate_setup=self.gate_setup_cost,
            canonicalization=canonicalization,
            requirements=requirements,
            checkpoint=checkpoint,
            coordination=coordination,
            expected_review=expected_review,
        )

    def to_document(self) -> Mapping[str, Any]:
        return dataclasses.asdict(self)


# ---------------------------------------------------------------------------
# Edmonds--Karp max flow and minimum edge cut
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MaxFlowResult:
    """Result plus augmenting paths, retained to make the algorithm inspectable."""

    total_flow: int
    source_reachable: frozenset[str]
    cut_edges: tuple[tuple[str, str, int], ...]
    augmenting_paths: tuple[tuple[str, ...], ...]


class CapacityNetwork:
    """Directed integer-capacity network using Edmonds--Karp.

    Edmonds--Karp repeatedly uses breadth-first search to find the shortest path in
    the *residual* network.  After sending the path bottleneck, it subtracts that
    amount from each forward residual edge and adds it to the corresponding reverse
    edge.  A later path can therefore undo and reroute an earlier choice.

    Complexity is ``O(V * E**2)``.  That is more than adequate for this transparent
    POC; a production planner could replace it with a faster max-flow library
    without changing the graph transformation or boundary semantics.
    """

    def __init__(self) -> None:
        self._capacity: dict[tuple[str, str], int] = {}
        self._neighbors: dict[str, set[str]] = {}

    def add_edge(self, source: str, target: str, capacity: int) -> None:
        if capacity < 0:
            raise ValueError("edge capacity must be non-negative")
        self._capacity[(source, target)] = (
            self._capacity.get((source, target), 0) + capacity
        )
        self._neighbors.setdefault(source, set()).add(target)
        self._neighbors.setdefault(target, set()).add(source)

    def max_flow_min_cut(self, source: str, sink: str) -> MaxFlowResult:
        """Compute maximum flow and the corresponding source-side min-cut set."""

        if source == sink:
            raise ValueError("source and sink must differ")
        residual: dict[tuple[str, str], int] = {
            edge: capacity for edge, capacity in self._capacity.items()
        }
        for left, right in tuple(self._capacity):
            residual.setdefault((right, left), 0)

        total_flow = 0
        paths: list[tuple[str, ...]] = []

        while True:
            parent: dict[str, str | None] = {source: None}
            queue: deque[str] = deque([source])
            while queue and sink not in parent:
                current = queue.popleft()
                for neighbor in sorted(self._neighbors.get(current, ())):
                    if neighbor in parent:
                        continue
                    if residual.get((current, neighbor), 0) <= 0:
                        continue
                    parent[neighbor] = current
                    queue.append(neighbor)

            if sink not in parent:
                break

            path_reversed = [sink]
            cursor = sink
            while parent[cursor] is not None:
                cursor = parent[cursor]  # type: ignore[assignment]
                path_reversed.append(cursor)
            path = tuple(reversed(path_reversed))
            bottleneck = min(
                residual[(left, right)]
                for left, right in zip(path, path[1:])
            )

            for left, right in zip(path, path[1:]):
                residual[(left, right)] -= bottleneck
                residual[(right, left)] = residual.get((right, left), 0) + bottleneck
            total_flow += bottleneck
            paths.append(path)

        # A residual reachability walk produces the S side of the min cut.
        reachable = {source}
        queue = deque([source])
        while queue:
            current = queue.popleft()
            for neighbor in sorted(self._neighbors.get(current, ())):
                if neighbor in reachable:
                    continue
                if residual.get((current, neighbor), 0) > 0:
                    reachable.add(neighbor)
                    queue.append(neighbor)

        cut_edges = tuple(
            sorted(
                (left, right, capacity)
                for (left, right), capacity in self._capacity.items()
                if capacity > 0 and left in reachable and right not in reachable
            )
        )
        return MaxFlowResult(
            total_flow=total_flow,
            source_reachable=frozenset(reachable),
            cut_edges=cut_edges,
            augmenting_paths=tuple(paths),
        )


# ---------------------------------------------------------------------------
# Dynamic deterministic-boundary analysis
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BoundaryAnalysis:
    """Complete, replay-oriented result of one graph/policy/state analysis."""

    graph_digest: str
    analysis_digest: str
    source_nodes: tuple[str, ...]
    consequential_sinks: tuple[str, ...]
    downstream_actions: Mapping[str, tuple[str, ...]]
    eligibility: Mapping[str, EligibilityAssessment]
    costs: Mapping[str, GateCostBreakdown]
    boundary_nodes: tuple[str, ...]
    crossing_nodes: tuple[str, ...]
    source_side_nodes: tuple[str, ...]
    sink_side_nodes: tuple[str, ...]
    minimum_cut_cost: int
    infinite_capacity: int
    fully_protected: bool
    unsafe_paths: tuple[tuple[str, ...], ...]


class BoundaryAnalyzer:
    """Derive effects, capacities, and a minimum deterministic vertex cut."""

    _SUPER_SOURCE = "@super-source"
    _SUPER_SINK = "@super-sink"

    def __init__(
        self,
        graph: WorkflowGraph,
        tool_contracts: Mapping[str, ToolContract],
        runtime_state: Mapping[str, ToolRuntimeState] | None = None,
        cost_policy: CostPolicy | None = None,
    ) -> None:
        self.graph = graph
        self.tool_contracts = dict(tool_contracts)
        self.runtime_state = dict(runtime_state or {})
        self.cost_policy = cost_policy or CostPolicy()

        for node in graph.nodes.values():
            if node.kind is NodeKind.ACTION and node.tool_name not in self.tool_contracts:
                raise KeyError(
                    f"action node {node.node_id!r} references unknown tool "
                    f"{node.tool_name!r}"
                )

    @staticmethod
    def _node_in(node_id: str) -> str:
        return f"@in:{node_id}"

    @staticmethod
    def _node_out(node_id: str) -> str:
        return f"@out:{node_id}"

    def _runtime_for(self, tool_name: str) -> ToolRuntimeState:
        return self.runtime_state.get(tool_name, ToolRuntimeState())

    def _consequential_sinks(self) -> tuple[str, ...]:
        result: list[str] = []
        for node_id, node in self.graph.nodes.items():
            if node.kind is not NodeKind.ACTION:
                continue
            assert node.tool_name is not None
            contract = self.tool_contracts[node.tool_name]
            if contract.is_consequential(self._runtime_for(node.tool_name)):
                result.append(node_id)
        return tuple(sorted(result))

    def _propagate_downstream_actions(
        self, sinks: Sequence[str]
    ) -> Mapping[str, tuple[str, ...]]:
        """Propagate each sink identity backward, including through graph cycles."""

        downstream: dict[str, set[str]] = {
            node_id: set() for node_id in self.graph.nodes
        }
        predecessors = self.graph.predecessors()
        for sink in sinks:
            visited = {sink}
            queue = deque([sink])
            while queue:
                current = queue.popleft()
                downstream[current].add(sink)
                for predecessor in predecessors[current]:
                    downstream[predecessor].add(sink)
                    if predecessor not in visited:
                        visited.add(predecessor)
                        queue.append(predecessor)
        return {
            node_id: tuple(sorted(actions))
            for node_id, actions in downstream.items()
        }

    def _derive_enforcement_contract(
        self, action_nodes: Iterable[str]
    ) -> EnforcementContract | None:
        action_ids = frozenset(action_nodes)
        if not action_ids:
            return None

        tools: set[str] = set()
        inputs: set[str] = set()
        permissions: set[str] = set()
        validators: set[str] = set()
        state_dependencies: set[str] = set()
        controls: set[str] = set()
        total_targets = 0

        for action_id in sorted(action_ids):
            action = self.graph.nodes[action_id]
            if action.kind is not NodeKind.ACTION or action.tool_name is None:
                raise ValueError(f"{action_id!r} is not a valid action node")
            contract = self.tool_contracts[action.tool_name]
            runtime = self._runtime_for(action.tool_name)
            tools.add(contract.name)
            inputs.update(contract.required_inputs)
            permissions.add(contract.required_permission)
            validators.update(contract.validators)
            state_dependencies.update(contract.state_dependencies)
            controls.update(contract.deterministic_controls)
            total_targets += contract.effective_fanout(runtime)

        return EnforcementContract(
            action_nodes=action_ids,
            tool_names=frozenset(tools),
            required_inputs=frozenset(inputs),
            required_permissions=frozenset(permissions),
            validators=frozenset(validators),
            state_dependencies=frozenset(state_dependencies),
            deterministic_controls=frozenset(controls),
            total_target_count=total_targets,
        )

    def _assess_node(
        self, node: WorkflowNode, action_nodes: Sequence[str]
    ) -> EligibilityAssessment:
        contract = self._derive_enforcement_contract(action_nodes)
        reasons: list[str] = []

        if contract is None:
            reasons.append("no consequential action is reachable")
            return EligibilityAssessment(False, tuple(reasons), None)
        if node.kind is NodeKind.REQUEST:
            reasons.append("a raw request is not a canonical action")
        if node.kind is NodeKind.ACTION:
            reasons.append("the external operation has already been reached")
        if node.already_executed:
            reasons.append("the node is marked as already executed")

        missing_tools = contract.tool_names - node.canonicalizable_tools
        if missing_tools:
            reasons.append(
                "cannot canonicalize tools: " + ", ".join(sorted(missing_tools))
            )
        missing_inputs = contract.required_inputs - node.known_inputs
        if missing_inputs:
            reasons.append("unresolved inputs: " + ", ".join(sorted(missing_inputs)))
        missing_validators = contract.validators - node.available_validators
        if missing_validators:
            reasons.append(
                "validators unavailable: " + ", ".join(sorted(missing_validators))
            )
        missing_state = (
            contract.state_dependencies - node.available_state_dependencies
        )
        if missing_state:
            reasons.append(
                "state unavailable: " + ", ".join(sorted(missing_state))
            )
        missing_controls = contract.deterministic_controls - node.available_controls
        if missing_controls:
            reasons.append(
                "controls unavailable: " + ", ".join(sorted(missing_controls))
            )
        if contract.required_permissions and not node.authorization_context_available:
            reasons.append("authorization context is unavailable")

        return EligibilityAssessment(not reasons, tuple(reasons), contract)

    def _find_unsafe_paths(
        self,
        source_nodes: Sequence[str],
        sinks: Sequence[str],
        eligible_nodes: frozenset[str],
    ) -> tuple[tuple[str, ...], ...]:
        """Find witness paths containing no possible deterministic gate.

        A witness is more useful than a bare ``False``: it tells an operator which
        route bypasses every eligible enforcement point.  We return at most one
        shortest witness per source/sink pair to keep diagnostics compact.
        """

        witnesses: list[tuple[str, ...]] = []
        for source in sorted(source_nodes):
            for sink in sorted(sinks):
                parent: dict[str, str | None] = {source: None}
                queue = deque([source])
                while queue and sink not in parent:
                    current = queue.popleft()
                    for neighbor in self.graph.successors(current):
                        if neighbor in parent:
                            continue
                        if neighbor in eligible_nodes and neighbor != sink:
                            continue
                        parent[neighbor] = current
                        queue.append(neighbor)
                if sink not in parent:
                    continue
                reverse_path = [sink]
                cursor = sink
                while parent[cursor] is not None:
                    cursor = parent[cursor]  # type: ignore[assignment]
                    reverse_path.append(cursor)
                witnesses.append(tuple(reversed(reverse_path)))
        return tuple(witnesses)

    def analyze(self, source_nodes: Iterable[str] | None = None) -> BoundaryAnalysis:
        """Compute a state- and policy-bound minimum deterministic boundary."""

        if source_nodes is None:
            sources = tuple(
                sorted(
                    node_id
                    for node_id, node in self.graph.nodes.items()
                    if node.kind is NodeKind.REQUEST
                )
            )
        else:
            sources = tuple(sorted(set(source_nodes)))
        if not sources:
            raise ValueError("at least one probabilistic source is required")
        unknown_sources = set(sources) - set(self.graph.nodes)
        if unknown_sources:
            raise KeyError(f"unknown source nodes: {sorted(unknown_sources)}")

        sinks = self._consequential_sinks()
        downstream = self._propagate_downstream_actions(sinks)
        eligibility: dict[str, EligibilityAssessment] = {}
        costs: dict[str, GateCostBreakdown] = {}
        for node_id in sorted(self.graph.nodes):
            assessment = self._assess_node(
                self.graph.nodes[node_id], downstream[node_id]
            )
            eligibility[node_id] = assessment
            if assessment.eligible:
                assert assessment.enforcement_contract is not None
                costs[node_id] = self.cost_policy.price(
                    self.graph.nodes[node_id], assessment.enforcement_contract
                )

        # INF is strictly larger than the cost of selecting every eligible node.
        # Therefore, any feasible all-finite cut is cheaper than even one forbidden
        # edge.  A min-cut value >= INF proves there is no fully enforceable cut.
        infinite_capacity = 1 + sum(cost.total for cost in costs.values())
        network = CapacityNetwork()
        for node_id in sorted(self.graph.nodes):
            internal_capacity = (
                costs[node_id].total if node_id in costs else infinite_capacity
            )
            network.add_edge(
                self._node_in(node_id),
                self._node_out(node_id),
                internal_capacity,
            )
        for left, right in self.graph.edges():
            network.add_edge(
                self._node_out(left), self._node_in(right), infinite_capacity
            )
        for source in sources:
            network.add_edge(
                self._SUPER_SOURCE, self._node_in(source), infinite_capacity
            )
        for sink in sinks:
            network.add_edge(
                self._node_out(sink), self._SUPER_SINK, infinite_capacity
            )

        flow = network.max_flow_min_cut(self._SUPER_SOURCE, self._SUPER_SINK)
        crossing_nodes = tuple(
            sorted(
                node_id
                for node_id in self.graph.nodes
                if self._node_in(node_id) in flow.source_reachable
                and self._node_out(node_id) not in flow.source_reachable
            )
        )
        fully_protected = not sinks or flow.total_flow < infinite_capacity
        boundary_nodes = (
            crossing_nodes
            if fully_protected and all(node_id in costs for node_id in crossing_nodes)
            else ()
        )
        eligible_nodes = frozenset(costs)
        unsafe_paths = self._find_unsafe_paths(sources, sinks, eligible_nodes)
        if fully_protected:
            # A finite cut and an ungated witness cannot both exist.  Treat a
            # disagreement as an implementation error, never as authorization.
            if unsafe_paths:
                raise AssertionError("finite cut disagrees with unsafe-path analysis")
        elif not unsafe_paths and sinks:
            raise AssertionError("infinite cut lacks an unsafe-path witness")

        source_side = tuple(
            sorted(
                node_id
                for node_id in self.graph.nodes
                if self._node_out(node_id) in flow.source_reachable
            )
        )
        sink_side = tuple(
            sorted(
                node_id
                for node_id in self.graph.nodes
                if self._node_in(node_id) not in flow.source_reachable
            )
        )

        inputs_document = {
            "graph": self.graph.to_document(),
            "contracts": {
                name: contract.to_document()
                for name, contract in sorted(self.tool_contracts.items())
            },
            "runtime_state": {
                name: state for name, state in sorted(self.runtime_state.items())
            },
            "cost_policy": self.cost_policy.to_document(),
            "sources": sources,
        }
        result_document = {
            "inputs_digest": sha256_document(inputs_document),
            "sinks": sinks,
            "downstream": downstream,
            "eligible_costs": {
                node_id: cost.to_document() for node_id, cost in sorted(costs.items())
            },
            "boundary_nodes": boundary_nodes,
            "crossing_nodes": crossing_nodes,
            "minimum_cut_cost": flow.total_flow,
            "infinite_capacity": infinite_capacity,
            "fully_protected": fully_protected,
            "unsafe_paths": unsafe_paths,
        }
        return BoundaryAnalysis(
            graph_digest=self.graph.digest,
            analysis_digest=sha256_document(result_document),
            source_nodes=sources,
            consequential_sinks=sinks,
            downstream_actions=downstream,
            eligibility=eligibility,
            costs=costs,
            boundary_nodes=boundary_nodes,
            crossing_nodes=crossing_nodes,
            source_side_nodes=source_side,
            sink_side_nodes=sink_side,
            minimum_cut_cost=flow.total_flow,
            infinite_capacity=infinite_capacity,
            fully_protected=fully_protected,
            unsafe_paths=unsafe_paths,
        )


# ---------------------------------------------------------------------------
# Deterministic refund boundary: canonical action, state, evidence, and policy
# ---------------------------------------------------------------------------


class TransactionStatus(str, Enum):
    PENDING = "PENDING"
    SETTLED = "SETTLED"


@dataclass(frozen=True)
class Transaction:
    """Minimal immutable ledger transaction used by the refund example."""

    transaction_id: str
    amount_cents: int
    status: TransactionStatus
    merchant_order_reference: str
    posted_at_epoch_s: int
    refundable: bool = True

    def __post_init__(self) -> None:
        if not self.transaction_id or not self.merchant_order_reference:
            raise ValueError("transaction identifiers must be non-empty")
        if self.amount_cents <= 0:
            raise ValueError("transaction amounts must be positive")


@dataclass(frozen=True)
class RefundRecord:
    refund_id: str
    transaction_id: str
    amount_cents: int
    idempotency_key: str


@dataclass(frozen=True)
class AccountSnapshot:
    """Immutable, canonically hashable view of the relevant account state."""

    account_id: str
    version: str
    transactions: tuple[Transaction, ...]
    refunds: tuple[RefundRecord, ...] = ()

    def __post_init__(self) -> None:
        transaction_ids = [item.transaction_id for item in self.transactions]
        refund_ids = [item.refund_id for item in self.refunds]
        if len(transaction_ids) != len(set(transaction_ids)):
            raise ValueError("duplicate transaction IDs in account snapshot")
        if len(refund_ids) != len(set(refund_ids)):
            raise ValueError("duplicate refund IDs in account snapshot")

    def transaction(self, transaction_id: str) -> Transaction | None:
        return next(
            (
                item
                for item in self.transactions
                if item.transaction_id == transaction_id
            ),
            None,
        )

    def refunded_cents(self, transaction_id: str) -> int:
        return sum(
            item.amount_cents
            for item in self.refunds
            if item.transaction_id == transaction_id
        )

    def to_document(self) -> Mapping[str, Any]:
        return {
            "account_id": self.account_id,
            "version": self.version,
            "transactions": sorted(
                self.transactions, key=lambda item: item.transaction_id
            ),
            "refunds": sorted(self.refunds, key=lambda item: item.refund_id),
        }

    @property
    def state_root(self) -> str:
        """POC state root; a real deployment could use a Merkle state root."""

        return sha256_document(self.to_document())


class RefundReason(str, Enum):
    DUPLICATE_CHARGE = "DUPLICATE_CHARGE"


@dataclass(frozen=True)
class CanonicalRefundAction:
    """The only refund representation accepted by the deterministic gate."""

    account_id: str
    transaction_id: str
    amount_cents: int
    reason_code: RefundReason
    action_type: str = field(default="REFUND", init=False)
    schema_version: str = field(default="refund-action/v1", init=False)

    def __post_init__(self) -> None:
        if not self.account_id or not self.transaction_id:
            raise ValueError("canonical action identifiers must be non-empty")
        if not isinstance(self.amount_cents, int) or isinstance(
            self.amount_cents, bool
        ):
            raise TypeError("amount_cents must be an integer")

    def to_document(self) -> Mapping[str, Any]:
        return {
            "schema_version": self.schema_version,
            "action_type": self.action_type,
            "account_id": self.account_id,
            "transaction_id": self.transaction_id,
            "amount_cents": self.amount_cents,
            "reason_code": self.reason_code,
        }

    @property
    def digest(self) -> str:
        return sha256_document(self.to_document())

    @property
    def idempotency_key(self) -> str:
        # The full digest is retained to make collisions negligible.  Namespace
        # prefixes prevent accidental reuse by a different operation family.
        return f"refund:v1:{self.digest}"


def normalize_refund_proposal(
    proposal: Mapping[str, Any],
) -> CanonicalRefundAction:
    """Deterministically normalize an *untrusted structured* LLM proposal.

    This function does not ask the model to reinterpret its own output.  It accepts
    only a small allow-list of keys and exact aliases, then emits a typed action.
    Free-form natural language remains on the probabilistic side of the boundary.
    Unknown keys are rejected so they cannot smuggle provider-specific parameters
    past policy checks.
    """

    allowed_keys = {
        "proposed_action",
        "account_id",
        "transaction_id",
        "amount_cents",
        "reason",
    }
    unexpected = set(proposal) - allowed_keys
    if unexpected:
        raise ValueError("unexpected proposal keys: " + ", ".join(sorted(unexpected)))

    proposed_action = proposal.get("proposed_action")
    if not isinstance(proposed_action, str):
        raise TypeError("proposed_action must be a string")
    action_alias = proposed_action.strip().casefold().replace("-", "_")
    if action_alias not in {"refund", "issue_refund"}:
        raise ValueError(f"unsupported proposed action: {proposed_action!r}")

    account_id = proposal.get("account_id")
    transaction_id = proposal.get("transaction_id")
    if not isinstance(account_id, str) or not account_id:
        raise TypeError("account_id must be a non-empty string")
    if not isinstance(transaction_id, str) or not transaction_id:
        raise TypeError("transaction_id must be a non-empty string")

    amount_cents = proposal.get("amount_cents")
    if not isinstance(amount_cents, int) or isinstance(amount_cents, bool):
        raise TypeError("amount_cents must be an integer; decimal floats are forbidden")

    reason = proposal.get("reason")
    if not isinstance(reason, str):
        raise TypeError("reason must be a string")
    reason_alias = "_".join(reason.strip().casefold().replace("-", " ").split())
    reason_codes = {
        "duplicate_charge": RefundReason.DUPLICATE_CHARGE,
        "probable_duplicate_charge": RefundReason.DUPLICATE_CHARGE,
    }
    if reason_alias not in reason_codes:
        raise ValueError(f"unsupported refund reason: {reason!r}")

    return CanonicalRefundAction(
        account_id=account_id,
        transaction_id=transaction_id,
        amount_cents=amount_cents,
        reason_code=reason_codes[reason_alias],
    )


@dataclass(frozen=True)
class DuplicateChargeEvidence:
    """Evidence reference; its truth is independently recomputed by the gate."""

    evidence_version: str
    state_root: str
    first_transaction_id: str
    second_transaction_id: str

    def to_document(self) -> Mapping[str, Any]:
        return dataclasses.asdict(self)

    @property
    def digest(self) -> str:
        return sha256_document(self.to_document())


@dataclass(frozen=True)
class RefundPolicy:
    """Versioned deterministic refund policy used for replay."""

    version: str
    maximum_automatic_refund_cents: int
    duplicate_window_seconds: int
    required_permission: str = "refund.execute"

    def __post_init__(self) -> None:
        if self.maximum_automatic_refund_cents < 0:
            raise ValueError("automatic refund limit must be non-negative")
        if self.duplicate_window_seconds < 0:
            raise ValueError("duplicate window must be non-negative")

    @property
    def digest(self) -> str:
        return sha256_document(self)


@dataclass(frozen=True)
class ActorContext:
    """Authenticated principal facts supplied independently of the LLM."""

    actor_id: str
    permissions: frozenset[str]
    automatic_refund_authority_cents: int

    @property
    def digest(self) -> str:
        return sha256_document(self)


@dataclass(frozen=True)
class GateCheck:
    name: str
    passed: bool
    detail: str


class GateOutcome(str, Enum):
    APPROVED = "APPROVED"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    DEFERRED = "DEFERRED"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class GateDecision:
    """Deterministic result bound to action, state, evidence, actor, and policy."""

    outcome: GateOutcome
    reason: str
    checks: tuple[GateCheck, ...]
    action_digest: str
    before_state_root: str
    evidence_digest: str
    policy_digest: str
    actor_digest: str
    idempotency_key: str

    def to_document(self) -> Mapping[str, Any]:
        return dataclasses.asdict(self)

    @property
    def digest(self) -> str:
        return sha256_document(self.to_document())


class DeterministicRefundGate:
    """Validate a canonical refund without relying on LLM assertions."""

    def evaluate(
        self,
        action: CanonicalRefundAction,
        account: AccountSnapshot,
        evidence: DuplicateChargeEvidence,
        actor: ActorContext,
        policy: RefundPolicy,
    ) -> GateDecision:
        """Return the same decision for the same canonical inputs.

        Checks are deliberately ordered and outcomes are explicit:

        * malformed/prohibited actions are rejected;
        * incomplete or stale state is deferred for refresh;
        * otherwise-valid actions above automatic authority go to human review;
        * only a complete passing set is approved.
        """

        checks: list[GateCheck] = []

        def check(name: str, passed: bool, detail: str) -> bool:
            checks.append(GateCheck(name, passed, detail))
            return passed

        def decision(outcome: GateOutcome, reason: str) -> GateDecision:
            return GateDecision(
                outcome=outcome,
                reason=reason,
                checks=tuple(checks),
                action_digest=action.digest,
                before_state_root=account.state_root,
                evidence_digest=evidence.digest,
                policy_digest=policy.digest,
                actor_digest=actor.digest,
                idempotency_key=action.idempotency_key,
            )

        if not check(
            "account_matches_action",
            action.account_id == account.account_id,
            "canonical account ID must equal the verified ledger account ID",
        ):
            return decision(GateOutcome.REJECTED, "ACCOUNT_MISMATCH")

        transaction = account.transaction(action.transaction_id)
        if not check(
            "transaction_exists",
            transaction is not None,
            "target transaction must exist in the verified account snapshot",
        ):
            return decision(GateOutcome.REJECTED, "TRANSACTION_NOT_FOUND")
        assert transaction is not None

        if not check(
            "positive_amount",
            action.amount_cents > 0,
            "refund amount must be a positive integer number of cents",
        ):
            return decision(GateOutcome.REJECTED, "INVALID_AMOUNT")

        already_refunded = account.refunded_cents(action.transaction_id)
        if not check(
            "not_already_fully_refunded",
            already_refunded < transaction.amount_cents,
            "verified refund records must leave refundable principal",
        ):
            return decision(GateOutcome.REJECTED, "ALREADY_REFUNDED")

        if not check(
            "amount_within_remaining_principal",
            action.amount_cents <= transaction.amount_cents - already_refunded,
            "refund cannot exceed the original amount less prior refunds",
        ):
            return decision(GateOutcome.REJECTED, "AMOUNT_EXCEEDS_ORIGINAL")

        if not check(
            "transaction_refundable",
            transaction.refundable,
            "payment provider marked the transaction refundable",
        ):
            return decision(GateOutcome.REJECTED, "NOT_REFUNDABLE")

        if not check(
            "transaction_settled",
            transaction.status is TransactionStatus.SETTLED,
            "pending transactions are deferred rather than refunded",
        ):
            return decision(GateOutcome.DEFERRED, "TRANSACTION_NOT_SETTLED")

        if not check(
            "evidence_bound_to_state",
            evidence.state_root == account.state_root,
            "evidence root must match the exact ledger snapshot being evaluated",
        ):
            return decision(GateOutcome.DEFERRED, "STALE_EVIDENCE")

        pair = {
            evidence.first_transaction_id,
            evidence.second_transaction_id,
        }
        other_ids = pair - {action.transaction_id}
        pair_shape_valid = (
            len(pair) == 2
            and action.transaction_id in pair
            and len(other_ids) == 1
        )
        if not check(
            "evidence_identifies_target_pair",
            pair_shape_valid,
            "evidence must identify target plus one distinct comparison transaction",
        ):
            return decision(GateOutcome.DEFERRED, "INCOMPLETE_DUPLICATE_EVIDENCE")

        other = account.transaction(next(iter(other_ids)))
        if not check(
            "comparison_transaction_exists",
            other is not None,
            "comparison transaction must exist in the same account snapshot",
        ):
            return decision(GateOutcome.DEFERRED, "INCOMPLETE_DUPLICATE_EVIDENCE")
        assert other is not None

        duplicate_verified = all(
            (
                other.status is TransactionStatus.SETTLED,
                other.amount_cents == transaction.amount_cents,
                other.merchant_order_reference
                == transaction.merchant_order_reference,
                abs(other.posted_at_epoch_s - transaction.posted_at_epoch_s)
                <= policy.duplicate_window_seconds,
            )
        )
        if not check(
            "duplicate_charge_verified",
            duplicate_verified,
            "settled charges must share amount/reference and fall within policy window",
        ):
            return decision(GateOutcome.DEFERRED, "DUPLICATE_NOT_VERIFIED")

        if not check(
            "actor_authorized",
            policy.required_permission in actor.permissions,
            "authenticated actor must hold the policy's execution permission",
        ):
            return decision(GateOutcome.REJECTED, "PERMISSION_DENIED")

        automatic_limit = min(
            policy.maximum_automatic_refund_cents,
            actor.automatic_refund_authority_cents,
        )
        if not check(
            "within_automatic_authority",
            action.amount_cents <= automatic_limit,
            "amount above policy or actor authority requires human approval",
        ):
            return decision(GateOutcome.HUMAN_REVIEW, "AUTHORITY_LIMIT_EXCEEDED")

        return decision(GateOutcome.APPROVED, "ALL_CHECKS_PASSED")


# ---------------------------------------------------------------------------
# Idempotent execution, post-condition verification, and replay certificate
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProviderReceipt:
    """Deterministic stand-in for a provider's signed execution receipt."""

    provider_reference: str
    action_digest: str
    idempotency_key: str
    after_state_root: str

    @property
    def digest(self) -> str:
        return sha256_document(self)


@dataclass(frozen=True)
class RefundExecution:
    after_state: AccountSnapshot
    receipt: ProviderReceipt


class InMemoryPaymentExecutor:
    """Tiny idempotent executor used to demonstrate exactly-once intent.

    The cache is process-local and therefore not durable.  Real execution needs a
    transactional idempotency store colocated with, or honored by, the payment
    provider.  The important protocol property shown here is that retrying the same
    canonical action returns the original result instead of creating a second
    refund.
    """

    def __init__(self) -> None:
        self._executions: dict[str, RefundExecution] = {}

    def execute(
        self,
        action: CanonicalRefundAction,
        gate_decision: GateDecision,
        current_state: AccountSnapshot,
    ) -> RefundExecution:
        if gate_decision.idempotency_key != action.idempotency_key:
            raise ValueError("decision is bound to a different idempotency key")

        previous = self._executions.get(action.idempotency_key)
        if previous is not None:
            if previous.receipt.action_digest != action.digest:
                raise AssertionError("idempotency-key collision detected")
            return previous

        if gate_decision.outcome is not GateOutcome.APPROVED:
            raise PermissionError("only an APPROVED gate decision may execute")
        if gate_decision.action_digest != action.digest:
            raise ValueError("gate decision is bound to a different action")
        if gate_decision.before_state_root != current_state.state_root:
            raise ValueError("state changed after validation; re-evaluation required")

        transaction = current_state.transaction(action.transaction_id)
        if transaction is None:
            raise ValueError("target transaction disappeared before execution")
        if (
            current_state.refunded_cents(action.transaction_id) + action.amount_cents
            > transaction.amount_cents
        ):
            raise ValueError("execution precondition no longer holds")

        refund_id = "RF-" + sha256_document(
            {"idempotency_key": action.idempotency_key}
        )[:16].upper()
        refund = RefundRecord(
            refund_id=refund_id,
            transaction_id=action.transaction_id,
            amount_cents=action.amount_cents,
            idempotency_key=action.idempotency_key,
        )
        after_state = replace(
            current_state,
            version=current_state.version + "+refund",
            refunds=current_state.refunds + (refund,),
        )

        # Post-condition verification happens before a successful receipt is made
        # visible.  It verifies observed state, not a model-generated assertion.
        expected_total = (
            current_state.refunded_cents(action.transaction_id) + action.amount_cents
        )
        if after_state.refunded_cents(action.transaction_id) != expected_total:
            raise AssertionError("refund post-condition failed")

        receipt = ProviderReceipt(
            provider_reference="PAY-" + sha256_document(
                {
                    "action": action.to_document(),
                    "before_state_root": current_state.state_root,
                }
            )[:20].upper(),
            action_digest=action.digest,
            idempotency_key=action.idempotency_key,
            after_state_root=after_state.state_root,
        )
        execution = RefundExecution(after_state=after_state, receipt=receipt)
        self._executions[action.idempotency_key] = execution
        return execution


@dataclass(frozen=True)
class ExecutionCertificate:
    """Hash-linked record of analysis, decision, execution, and resulting state.

    SHA-256 provides an integrity checksum only.  A production certificate should
    be digitally signed or written to an authenticated append-only log to prove who
    issued it.  Replaying the complete decision also requires retaining the policy,
    actor, evidence, and before-state documents whose digests appear here.
    """

    certificate_version: str
    analysis_digest: str
    boundary_nodes: tuple[str, ...]
    action: CanonicalRefundAction
    action_digest: str
    gate_decision_digest: str
    policy_digest: str
    evidence_digest: str
    actor_digest: str
    before_state_root: str
    after_state_root: str
    idempotency_key: str
    provider_receipt: ProviderReceipt
    certificate_digest: str

    def _payload(self) -> Mapping[str, Any]:
        return {
            "certificate_version": self.certificate_version,
            "analysis_digest": self.analysis_digest,
            "boundary_nodes": self.boundary_nodes,
            "action": self.action.to_document(),
            "action_digest": self.action_digest,
            "gate_decision_digest": self.gate_decision_digest,
            "policy_digest": self.policy_digest,
            "evidence_digest": self.evidence_digest,
            "actor_digest": self.actor_digest,
            "before_state_root": self.before_state_root,
            "after_state_root": self.after_state_root,
            "idempotency_key": self.idempotency_key,
            "provider_receipt": self.provider_receipt,
        }

    @classmethod
    def issue(
        cls,
        analysis: BoundaryAnalysis,
        action: CanonicalRefundAction,
        decision: GateDecision,
        execution: RefundExecution,
    ) -> "ExecutionCertificate":
        if not analysis.fully_protected or not analysis.boundary_nodes:
            raise ValueError("cannot certify execution from an unprotected analysis")
        if decision.outcome is not GateOutcome.APPROVED:
            raise ValueError("cannot certify a non-approved gate decision")
        if execution.receipt.action_digest != action.digest:
            raise ValueError("provider receipt is bound to another action")
        if execution.receipt.after_state_root != execution.after_state.state_root:
            raise ValueError("provider receipt does not match resulting state")

        provisional = cls(
            certificate_version="execution-certificate/v1",
            analysis_digest=analysis.analysis_digest,
            boundary_nodes=analysis.boundary_nodes,
            action=action,
            action_digest=action.digest,
            gate_decision_digest=decision.digest,
            policy_digest=decision.policy_digest,
            evidence_digest=decision.evidence_digest,
            actor_digest=decision.actor_digest,
            before_state_root=decision.before_state_root,
            after_state_root=execution.after_state.state_root,
            idempotency_key=decision.idempotency_key,
            provider_receipt=execution.receipt,
            certificate_digest="",
        )
        return replace(
            provisional,
            certificate_digest=sha256_document(provisional._payload()),
        )

    def verify_integrity(self) -> bool:
        """Check all internal bindings and the certificate's integrity digest."""

        return all(
            (
                self.action_digest == self.action.digest,
                self.idempotency_key == self.action.idempotency_key,
                self.provider_receipt.action_digest == self.action_digest,
                self.provider_receipt.idempotency_key == self.idempotency_key,
                self.provider_receipt.after_state_root == self.after_state_root,
                self.certificate_digest == sha256_document(self._payload()),
            )
        )


# ---------------------------------------------------------------------------
# Demonstration fixtures
# ---------------------------------------------------------------------------


TOOL_CONTRACT_DOCUMENTS: tuple[Mapping[str, Any], ...] = (
    {
        "name": "payment.refund",
        "version": "payment.refund/v3",
        "effects": {
            "writes_external_state": True,
            "financial": True,
            "reversible": False,
            "default_fanout": 1,
        },
        "required_permission": "refund.execute",
        "required_inputs": [
            "account_id",
            "transaction_id",
            "amount_cents",
            "reason_code",
        ],
        "validators": [
            "account_owns_transaction",
            "transaction_settled",
            "not_already_refunded",
            "duplicate_charge_evidence",
            "amount_within_original",
        ],
        "state_dependencies": ["account_ledger"],
        "deterministic_controls": [
            "state_binding",
            "idempotency",
            "postcondition",
        ],
    },
    {
        "name": "customer.set_status",
        "version": "customer.set_status/v2",
        "effects": {
            "writes_external_state": True,
            "sensitive_data_disclosure": False,
            "reversible": True,
            "default_fanout": 1,
        },
        "required_permission": "customer.write",
        "required_inputs": ["account_id", "new_status"],
        "validators": ["account_exists", "status_transition_allowed"],
        "state_dependencies": ["account_record"],
        "deterministic_controls": [
            "state_binding",
            "idempotency",
            "postcondition",
        ],
    },
    {
        "name": "messaging.send",
        "version": "messaging.send/v5",
        "effects": {
            "writes_external_state": True,
            "sensitive_data_disclosure": True,
            "reversible": False,
            "default_fanout": 1,
        },
        "required_permission": "message.send",
        "required_inputs": ["account_id", "recipient", "template_id"],
        "validators": ["recipient_verified", "template_approved"],
        "state_dependencies": ["contact_record"],
        "deterministic_controls": [
            "state_binding",
            "idempotency",
            "delivery_receipt",
        ],
    },
)


def load_demo_contracts() -> Mapping[str, ToolContract]:
    """Parse the demo contracts as a registry would at startup."""

    contracts = [
        ToolContract.from_document(document) for document in TOOL_CONTRACT_DOCUMENTS
    ]
    return {contract.name: contract for contract in contracts}


ACTION_DEFINITIONS: Mapping[str, tuple[str, str]] = {
    "refund": ("refund_intent", "execute_refund"),
    "update": ("update_intent", "update_account"),
    "message": ("message_intent", "send_message"),
}

ACTION_TO_TOOL: Mapping[str, str] = {
    "refund": "payment.refund",
    "update": "customer.set_status",
    "message": "messaging.send",
}


def build_demo_workflow(
    contracts: Mapping[str, ToolContract],
    included_actions: Iterable[str] = ("refund",),
    *,
    unsafe_refund_bypass: bool = False,
) -> WorkflowGraph:
    """Build refund-only or expanded workflow graphs from the same node schema."""

    included = tuple(sorted(set(included_actions)))
    unknown = set(included) - set(ACTION_DEFINITIONS)
    if unknown:
        raise ValueError(f"unknown demo actions: {sorted(unknown)}")
    if not included:
        raise ValueError("the demo workflow needs at least one action branch")

    graph = WorkflowGraph()
    graph.add_node(WorkflowNode("request", NodeKind.REQUEST))
    graph.add_node(
        WorkflowNode(
            "interpret",
            NodeKind.PROBABILISTIC,
            known_inputs=frozenset({"account_id"}),
            telemetry=NodeTelemetry(
                canonicalization_cpu_us=2_000,
                checkpoint_bytes=16_384,
                semantic_action_classes=8,
                expected_review_basis_points=2_500,
            ),
        )
    )
    graph.add_node(
        WorkflowNode(
            "investigate",
            NodeKind.PROBABILISTIC,
            known_inputs=frozenset({"account_id", "transaction_id"}),
            available_state_dependencies=frozenset({"account_ledger"}),
            telemetry=NodeTelemetry(
                canonicalization_cpu_us=1_200,
                checkpoint_bytes=12_288,
                semantic_action_classes=6,
                expected_review_basis_points=1_500,
            ),
        )
    )
    graph.add_node(WorkflowNode("advisory_answer", NodeKind.ADVISORY))

    included_contracts = [contracts[ACTION_TO_TOOL[name]] for name in included]
    all_inputs = frozenset().union(
        *(contract.required_inputs for contract in included_contracts)
    )
    all_tools = frozenset(contract.name for contract in included_contracts)
    all_validators = frozenset().union(
        *(contract.validators for contract in included_contracts)
    )
    all_state = frozenset().union(
        *(contract.state_dependencies for contract in included_contracts)
    )
    all_controls = frozenset().union(
        *(contract.deterministic_controls for contract in included_contracts)
    )
    graph.add_node(
        WorkflowNode(
            "action_plan",
            NodeKind.CANDIDATE,
            known_inputs=all_inputs,
            canonicalizable_tools=all_tools,
            available_validators=all_validators,
            available_state_dependencies=all_state,
            available_controls=all_controls,
            authorization_context_available=True,
            telemetry=NodeTelemetry(
                canonicalization_cpu_us=800,
                checkpoint_bytes=8_192,
                # The plan is semantically broader than any specialized intent,
                # even when runtime pruning leaves only one consequential branch.
                semantic_action_classes=4,
                expected_review_basis_points=500,
            ),
        )
    )

    for action_name in included:
        intent_id, action_id = ACTION_DEFINITIONS[action_name]
        contract = contracts[ACTION_TO_TOOL[action_name]]
        graph.add_node(
            WorkflowNode(
                intent_id,
                NodeKind.CANDIDATE,
                known_inputs=contract.required_inputs,
                canonicalizable_tools=frozenset({contract.name}),
                available_validators=contract.validators,
                available_state_dependencies=contract.state_dependencies,
                available_controls=contract.deterministic_controls,
                authorization_context_available=True,
                telemetry=NodeTelemetry(
                    canonicalization_cpu_us=100,
                    checkpoint_bytes=2_048,
                    semantic_action_classes=1,
                    expected_review_basis_points=100,
                ),
            )
        )
        graph.add_node(
            WorkflowNode(
                action_id,
                NodeKind.ACTION,
                tool_name=contract.name,
                already_executed=False,
            )
        )

    graph.add_edge("request", "interpret")
    graph.add_edge("interpret", "investigate")
    graph.add_edge("investigate", "advisory_answer")
    graph.add_edge("investigate", "action_plan")
    for action_name in included:
        intent_id, action_id = ACTION_DEFINITIONS[action_name]
        graph.add_edge("action_plan", intent_id)
        graph.add_edge(intent_id, action_id)

    if unsafe_refund_bypass:
        if "refund" not in included:
            raise ValueError("refund bypass requires the refund action branch")
        # This deliberately unsafe route contains no node at which the action is
        # canonicalizable and validatable.  Analysis must return fail-closed.
        graph.add_edge("request", "execute_refund")

    return graph


def build_refund_fixture() -> tuple[
    CanonicalRefundAction,
    AccountSnapshot,
    DuplicateChargeEvidence,
    ActorContext,
    RefundPolicy,
]:
    """Create the two-settled-charge scenario from the transcript."""

    proposal = {
        "proposed_action": "refund",
        "account_id": "C-417",
        "transaction_id": "TX-782",
        "amount_cents": 7_500,
        "reason": "Probable duplicate charge",
    }
    action = normalize_refund_proposal(proposal)
    account = AccountSnapshot(
        account_id="C-417",
        version="ledger/42",
        transactions=(
            Transaction(
                transaction_id="TX-781",
                amount_cents=7_500,
                status=TransactionStatus.SETTLED,
                merchant_order_reference="ORDER-9001",
                posted_at_epoch_s=1_787_332_860,
            ),
            Transaction(
                transaction_id="TX-782",
                amount_cents=7_500,
                status=TransactionStatus.SETTLED,
                merchant_order_reference="ORDER-9001",
                posted_at_epoch_s=1_787_332_920,
            ),
        ),
    )
    evidence = DuplicateChargeEvidence(
        evidence_version="duplicate-evidence/v1",
        state_root=account.state_root,
        first_transaction_id="TX-781",
        second_transaction_id="TX-782",
    )
    actor = ActorContext(
        actor_id="support-agent-12",
        permissions=frozenset({"refund.execute"}),
        automatic_refund_authority_cents=10_000,
    )
    policy = RefundPolicy(
        version="refund-policy/2026-08-21",
        maximum_automatic_refund_cents=10_000,
        duplicate_window_seconds=300,
    )
    return action, account, evidence, actor, policy


# ---------------------------------------------------------------------------
# Human-readable demo/reporting
# ---------------------------------------------------------------------------


def render_analysis(title: str, analysis: BoundaryAnalysis) -> str:
    """Render the facts most useful for understanding a boundary decision."""

    lines = [title, "=" * len(title)]
    lines.append(
        "Consequential sinks: "
        + (", ".join(analysis.consequential_sinks) or "(none)")
    )
    if analysis.costs:
        lines.append("Eligible gate costs:")
        for node_id, cost in sorted(analysis.costs.items()):
            lines.append(
                f"  - {node_id}: {cost.total} "
                f"(setup={cost.gate_setup}, canonicalize={cost.canonicalization}, "
                f"requirements={cost.requirements}, checkpoint={cost.checkpoint}, "
                f"coordination={cost.coordination}, review={cost.expected_review})"
            )
    else:
        lines.append("Eligible gate costs: (none)")

    lines.append(f"Minimum-cut cost: {analysis.minimum_cut_cost}")
    lines.append(f"Fully protected: {analysis.fully_protected}")
    if analysis.fully_protected:
        lines.append("Boundary nodes: " + ", ".join(analysis.boundary_nodes))
        lines.append("Source side: " + ", ".join(analysis.source_side_nodes))
        lines.append("Sink side: " + ", ".join(analysis.sink_side_nodes))
    else:
        lines.append("Decision: FAIL CLOSED; no finite eligible cut exists")
        for path in analysis.unsafe_paths:
            lines.append("Unsafe path: " + " -> ".join(path))
    lines.append(f"Analysis digest: {analysis.analysis_digest}")
    return "\n".join(lines)


def run_demo() -> None:
    """Run four boundary scenarios and one end-to-end refund execution."""

    contracts = load_demo_contracts()

    refund_graph = build_demo_workflow(contracts, ("refund",))
    refund_analysis = BoundaryAnalyzer(refund_graph, contracts).analyze()

    expanded_graph = build_demo_workflow(
        contracts, ("refund", "update", "message")
    )
    expanded_analysis = BoundaryAnalyzer(expanded_graph, contracts).analyze()

    # The graph remains expanded, but verified dry-run state means update and
    # message calls no longer have real external effects.  Re-analysis moves the
    # cut from a broad shared plan to the cheaper specialized refund intent.
    narrowed_runtime = {
        "customer.set_status": ToolRuntimeState(dry_run=True),
        "messaging.send": ToolRuntimeState(dry_run=True),
    }
    narrowed_analysis = BoundaryAnalyzer(
        expanded_graph, contracts, narrowed_runtime
    ).analyze()

    unsafe_graph = build_demo_workflow(
        contracts, ("refund",), unsafe_refund_bypass=True
    )
    unsafe_analysis = BoundaryAnalyzer(unsafe_graph, contracts).analyze()

    reports = (
        render_analysis("1. Refund-only graph", refund_analysis),
        render_analysis("2. Expanded three-action graph", expanded_analysis),
        render_analysis("3. Same graph after runtime consequence change", narrowed_analysis),
        render_analysis("4. Graph containing a direct unsafe bypass", unsafe_analysis),
    )
    print("\n\n".join(reports))

    action, before, evidence, actor, policy = build_refund_fixture()
    gate = DeterministicRefundGate()
    gate_decision = gate.evaluate(action, before, evidence, actor, policy)
    if gate_decision.outcome is not GateOutcome.APPROVED:
        raise RuntimeError(f"demo refund unexpectedly {gate_decision.outcome.value}")

    executor = InMemoryPaymentExecutor()
    first_execution = executor.execute(action, gate_decision, before)
    retried_execution = executor.execute(action, gate_decision, before)
    certificate = ExecutionCertificate.issue(
        refund_analysis, action, gate_decision, first_execution
    )
    replayed_decision = gate.evaluate(action, before, evidence, actor, policy)

    print("\n\n5. Deterministic refund gate and execution")
    print("==========================================")
    print("Canonical action: " + canonical_json_bytes(action.to_document()).decode())
    for item in gate_decision.checks:
        print(f"  {'PASS' if item.passed else 'FAIL'}  {item.name}")
    print(f"Gate outcome: {gate_decision.outcome.value}")
    print(f"Idempotency key: {action.idempotency_key}")
    print(f"Provider receipt: {first_execution.receipt.provider_reference}")
    print(f"Retry returned original execution: {first_execution == retried_execution}")
    print(f"Replay reproduced decision: {replayed_decision == gate_decision}")
    print(f"Certificate integrity valid: {certificate.verify_integrity()}")
    print(f"Certificate digest: {certificate.certificate_digest}")


# ---------------------------------------------------------------------------
# Embedded tests: executable claims about the POC's safety properties
# ---------------------------------------------------------------------------


class DeterministicBoundaryPocTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contracts = load_demo_contracts()

    def test_refund_only_selects_specialized_intent(self) -> None:
        graph = build_demo_workflow(self.contracts, ("refund",))
        result = BoundaryAnalyzer(graph, self.contracts).analyze()
        self.assertTrue(result.fully_protected)
        self.assertEqual(result.boundary_nodes, ("refund_intent",))
        self.assertLess(
            result.costs["refund_intent"].total,
            result.costs["action_plan"].total,
        )

    def test_expanded_graph_selects_shared_plan(self) -> None:
        graph = build_demo_workflow(
            self.contracts, ("refund", "update", "message")
        )
        result = BoundaryAnalyzer(graph, self.contracts).analyze()
        specialized_total = sum(
            result.costs[node_id].total
            for node_id in ("refund_intent", "update_intent", "message_intent")
        )
        self.assertEqual(result.boundary_nodes, ("action_plan",))
        self.assertLess(result.costs["action_plan"].total, specialized_total)

    def test_runtime_recomputation_moves_boundary_later(self) -> None:
        graph = build_demo_workflow(
            self.contracts, ("refund", "update", "message")
        )
        runtime = {
            "customer.set_status": ToolRuntimeState(dry_run=True),
            "messaging.send": ToolRuntimeState(dry_run=True),
        }
        result = BoundaryAnalyzer(graph, self.contracts, runtime).analyze()
        self.assertEqual(result.consequential_sinks, ("execute_refund",))
        self.assertEqual(result.boundary_nodes, ("refund_intent",))

    def test_direct_bypass_fails_closed_with_witness(self) -> None:
        graph = build_demo_workflow(
            self.contracts, ("refund",), unsafe_refund_bypass=True
        )
        result = BoundaryAnalyzer(graph, self.contracts).analyze()
        self.assertFalse(result.fully_protected)
        self.assertEqual(result.boundary_nodes, ())
        self.assertIn(("request", "execute_refund"), result.unsafe_paths)
        self.assertGreaterEqual(result.minimum_cut_cost, result.infinite_capacity)

    def test_edmonds_karp_uses_reverse_residual_edge(self) -> None:
        # This is the exact rerouting example from patent.md.  The first shortest
        # path consumes A->C; the second must traverse residual C->A to undo it.
        network = CapacityNetwork()
        for left, right in (
            ("S", "A"),
            ("S", "B"),
            ("A", "C"),
            ("A", "D"),
            ("B", "X"),
            ("X", "C"),
            ("D", "Y"),
            ("C", "T"),
            ("Y", "T"),
        ):
            network.add_edge(left, right, 1)
        result = network.max_flow_min_cut("S", "T")
        self.assertEqual(result.total_flow, 2)
        self.assertEqual(result.augmenting_paths[0], ("S", "A", "C", "T"))
        self.assertIn(("C", "A"), tuple(zip(result.augmenting_paths[1], result.augmenting_paths[1][1:])))

    def test_refund_is_state_bound_idempotent_and_certified(self) -> None:
        graph = build_demo_workflow(self.contracts, ("refund",))
        analysis = BoundaryAnalyzer(graph, self.contracts).analyze()
        action, before, evidence, actor, policy = build_refund_fixture()
        gate = DeterministicRefundGate()
        decision = gate.evaluate(action, before, evidence, actor, policy)
        self.assertEqual(decision.outcome, GateOutcome.APPROVED)

        executor = InMemoryPaymentExecutor()
        first = executor.execute(action, decision, before)
        second = executor.execute(action, decision, before)
        self.assertEqual(first, second)
        self.assertEqual(
            first.after_state.refunded_cents(action.transaction_id),
            action.amount_cents,
        )

        certificate = ExecutionCertificate.issue(analysis, action, decision, first)
        self.assertTrue(certificate.verify_integrity())
        self.assertFalse(
            replace(certificate, after_state_root="tampered").verify_integrity()
        )

    def test_stale_evidence_is_deferred(self) -> None:
        action, before, evidence, actor, policy = build_refund_fixture()
        stale = replace(evidence, state_root="old-state-root")
        decision = DeterministicRefundGate().evaluate(
            action, before, stale, actor, policy
        )
        self.assertEqual(decision.outcome, GateOutcome.DEFERRED)
        self.assertEqual(decision.reason, "STALE_EVIDENCE")

    def test_authority_limit_routes_to_human_review(self) -> None:
        action, before, evidence, actor, policy = build_refund_fixture()
        low_authority = replace(actor, automatic_refund_authority_cents=5_000)
        decision = DeterministicRefundGate().evaluate(
            action, before, evidence, low_authority, policy
        )
        self.assertEqual(decision.outcome, GateOutcome.HUMAN_REVIEW)

    def test_normalizer_rejects_float_amount(self) -> None:
        with self.assertRaises(TypeError):
            normalize_refund_proposal(
                {
                    "proposed_action": "refund",
                    "account_id": "C-417",
                    "transaction_id": "TX-782",
                    "amount_cents": 7_500.0,
                    "reason": "duplicate charge",
                }
            )


def run_tests() -> bool:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        DeterministicBoundaryPocTests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Dynamic deterministic-boundary proof of concept"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="run the embedded safety/property tests instead of the demo",
    )
    arguments = parser.parse_args(argv)
    if arguments.test:
        return 0 if run_tests() else 1
    run_demo()
    return 0


if __name__ == "__main__":
    sys.exit(main())
