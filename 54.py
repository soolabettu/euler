from collections import Counter

RANKS = {r: i for i, r in enumerate("..23456789TJQKA")}  # 2..A → 2..14
# Category order (bigger is better)
# Royal flush is treated as a straight flush with high=14.
CAT = {
    "HIGH": 1,
    "PAIR": 2,
    "TWO_PAIR": 3,
    "TRIPS": 4,
    "STRAIGHT": 5,
    "FLUSH": 6,
    "FULL_HOUSE": 7,
    "QUADS": 8,
    "STRAIGHT_FLUSH": 9,
}


def parse_hand(hand: str):
    """
    Input like '5H 5C 6S 7S KD' or '10H JD QS KC AH'.
    Returns list of (rank_val, suit) where rank_val is 2..14.
    """
    out = []
    for tok in hand.split():
        tok = tok.strip().upper()
        if len(tok) < 2:
            raise ValueError(f"Bad card: {tok}")
        rank = tok[:-1]
        suit = tok[-1]
        if rank == "10":
            rank = "T"
        if rank not in RANKS or suit not in "CDHS":
            raise ValueError(f"Bad card: {tok}")
        out.append((RANKS[rank], suit))
    if len(out) != 5:
        raise ValueError("Hand must have 5 cards")
    return out


def straight_high(values):
    """Return high card value of straight, handling A-low; else None."""
    uniq = sorted(set(values))
    if len(uniq) != 5:
        return None
    # A-low wheel: {14,2,3,4,5} counts as straight with high=5
    if uniq == [2, 3, 4, 5, 14]:
        return 5
    if max(uniq) - min(uniq) == 4:
        return max(uniq)
    return None


def evaluate(hand: str):
    """
    Return a tuple for sorting/comparison:
      (category, tiebreakers...)
    Higher tuple wins with default Python tuple comparison.
    """
    cards = parse_hand(hand)
    vals = [v for v, s in cards]
    suits = [s for v, s in cards]
    counts = Counter(vals)  # e.g., {5:2, 6:1, 7:1, 13:1}
    by_freq = (
        counts.most_common()
    )  # list of (val, freq) sorted by freq desc then val desc
    by_freq.sort(key=lambda x: (x[1], x[0]), reverse=True)

    is_flush = len(set(suits)) == 1
    s_hi = straight_high(vals)
    is_straight = s_hi is not None

    if is_flush and is_straight:
        return (CAT["STRAIGHT_FLUSH"], s_hi)

    if by_freq[0][1] == 4:
        quad = by_freq[0][0]
        kicker = max(v for v in vals if v != quad)
        return (CAT["QUADS"], quad, kicker)

    if by_freq[0][1] == 3 and by_freq[1][1] == 2:
        trips = by_freq[0][0]
        pair = by_freq[1][0]
        return (CAT["FULL_HOUSE"], trips, pair)

    if is_flush:
        return (CAT["FLUSH"],) + tuple(sorted(vals, reverse=True))

    if is_straight:
        return (CAT["STRAIGHT"], s_hi)

    if by_freq[0][1] == 3:
        trips = by_freq[0][0]
        kickers = sorted((v for v in vals if v != trips), reverse=True)
        return (CAT["TRIPS"], trips, *kickers)

    if by_freq[0][1] == 2 and by_freq[1][1] == 2:
        pair_high = max(by_freq[0][0], by_freq[1][0])
        pair_low = min(by_freq[0][0], by_freq[1][0])
        kicker = max(v for v in vals if v not in (pair_high, pair_low))
        return (CAT["TWO_PAIR"], pair_high, pair_low, kicker)

    if by_freq[0][1] == 2:
        pair = by_freq[0][0]
        kickers = sorted((v for v in vals if v != pair), reverse=True)
        return (CAT["PAIR"], pair, *kickers)

    return (CAT["HIGH"],) + tuple(sorted(vals, reverse=True))


def compare_hands(h1: str, h2: str):
    """
    Return 1 if h1 wins, -1 if h2 wins, 0 if tie.
    """
    e1, e2 = evaluate(h1), evaluate(h2)
    print(e1, e2)
    return (e1 > e2) - (e1 < e2)


def hand_key(hand: str):
    """Key function for sorting hands from weakest→strongest (reverse=True for strongest first)."""
    return evaluate(hand)


def label(hand: str):
    """Human-readable label for the best category."""
    cat = evaluate(hand)[0]
    inv = {v: k for k, v in CAT.items()}
    name = inv[cat]
    if name == "STRAIGHT_FLUSH" and evaluate(hand)[1] == 14:
        return "Royal Flush"
    pretty = {
        "HIGH": "High Card",
        "PAIR": "One Pair",
        "TWO_PAIR": "Two Pair",
        "TRIPS": "Three of a Kind",
        "STRAIGHT": "Straight",
        "FLUSH": "Flush",
        "FULL_HOUSE": "Full House",
        "QUADS": "Four of a Kind",
        "STRAIGHT_FLUSH": "Straight Flush",
    }
    return pretty[name]


def deal_two_players(cards_str: str):
    """Split ten card tokens into two five-card hands."""
    cards = cards_str.split()
    if len(cards) != 10:
        raise ValueError("Expected 10 cards (5 each for two players)")
    player1 = " ".join(cards[:5])
    player2 = " ".join(cards[5:])
    return player1, player2


import mytimeit

ans = 0
with mytimeit.MyTimer() as t:
    with open("poker.txt") as f:
        lines = f.readlines()
        for line in lines:
            h1, h2 = deal_two_players(line.strip())
            if compare_hands(h1, h2) == 1:
                ans += 1

        print(ans)
