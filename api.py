from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent

LANGUAGE_SUFFIXES = {
    "python": ".py",
    "cpp": ".cpp",
    "c": ".c",
    "go": ".go",
}


class Implementation(BaseModel):
    file_name: str
    language: str
    code: str


class ProblemCodeResponse(BaseModel):
    problem_number: int
    implementations: list[Implementation]


app = FastAPI(title="Project Euler Code API")


def render_homepage() -> str:
    language_options = "\n".join(
        f'<option value="{language}">{language}</option>'
        for language in LANGUAGE_SUFFIXES
    )
    return rf"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Project Euler Code Lookup</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f5efe2;
      --panel: #fffaf0;
      --ink: #1f2937;
      --muted: #5b6472;
      --accent: #0f766e;
      --accent-strong: #115e59;
      --line: #d6cfc2;
      --code-bg: #111827;
      --code-ink: #f9fafb;
      --code-muted: #94a3b8;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", serif;
      background:
        radial-gradient(circle at top, rgba(15, 118, 110, 0.12), transparent 28%),
        linear-gradient(180deg, #efe4cf 0%, var(--bg) 38%, #efe8db 100%);
      color: var(--ink);
      min-height: 100vh;
    }}

    main {{
      max-width: 980px;
      margin: 0 auto;
      padding: 48px 20px 64px;
    }}

    h1 {{
      margin: 0 0 12px;
      font-size: clamp(2.2rem, 4vw, 4.4rem);
      line-height: 0.95;
      letter-spacing: -0.04em;
    }}

    p {{
      margin: 0;
      max-width: 48rem;
      color: var(--muted);
      font-size: 1.05rem;
    }}

    form {{
      display: grid;
      grid-template-columns: minmax(0, 2fr) minmax(160px, 1fr) auto;
      gap: 12px;
      margin: 28px 0 20px;
      padding: 18px;
      background: rgba(255, 250, 240, 0.88);
      border: 1px solid var(--line);
      border-radius: 18px;
      backdrop-filter: blur(10px);
    }}

    label {{
      display: block;
      font-size: 0.9rem;
      color: var(--muted);
      margin-bottom: 6px;
    }}

    input,
    select,
    button {{
      width: 100%;
      border-radius: 12px;
      border: 1px solid var(--line);
      padding: 12px 14px;
      font: inherit;
    }}

    button {{
      align-self: end;
      background: var(--accent);
      color: white;
      border-color: var(--accent);
      font-weight: 700;
      cursor: pointer;
    }}

    button:hover {{
      background: var(--accent-strong);
    }}

    #status {{
      min-height: 1.5em;
      margin: 10px 2px 18px;
      color: var(--muted);
      font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
    }}

    .card {{
      background: rgba(255, 250, 240, 0.9);
      border: 1px solid var(--line);
      border-radius: 18px;
      overflow: hidden;
      margin-top: 18px;
      box-shadow: 0 18px 40px rgba(17, 24, 39, 0.08);
    }}

    .card header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      padding: 14px 18px;
      border-bottom: 1px solid var(--line);
      background: rgba(15, 118, 110, 0.08);
      font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
    }}

    .card-meta {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .copy-button {{
      width: auto;
      padding: 8px 12px;
      border-radius: 999px;
      background: white;
      color: var(--accent-strong);
      border: 1px solid rgba(15, 118, 110, 0.25);
      font: 0.85rem "IBM Plex Sans", "Segoe UI", sans-serif;
      font-weight: 700;
    }}

    .copy-button:hover {{
      background: #f0fdfa;
    }}

    pre {{
      margin: 0;
      padding: 20px;
      overflow-x: auto;
      background: var(--code-bg);
      color: var(--code-ink);
      font: 0.95rem/1.5 "IBM Plex Mono", "SFMono-Regular", monospace;
    }}

    code {{
      font: inherit;
    }}

    .language-badge {{
      color: var(--code-muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-size: 0.75rem;
      font-weight: 700;
    }}

    @media (max-width: 720px) {{
      form {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <h1>Project Euler<br>Code Lookup</h1>
    <p>Enter a Project Euler problem number and this service will return the implementation from this repository if one exists.</p>
    <form id="lookup-form">
      <div>
        <label for="problem-number">Problem number</label>
        <input id="problem-number" name="problem-number" type="number" min="1" required placeholder="8">
      </div>
      <div>
        <label for="language">Language</label>
        <select id="language" name="language">
          <option value="">Any available language</option>
          {language_options}
        </select>
      </div>
      <button type="submit">Show code</button>
    </form>
    <div id="status"></div>
    <section id="results"></section>
  </main>
  <script>
    const form = document.getElementById("lookup-form");
    const status = document.getElementById("status");
    const results = document.getElementById("results");

    function escapeHtml(value) {{
      return value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
    }}

    async function copyCode(code, button) {{
      try {{
        await navigator.clipboard.writeText(code);
        const original = button.textContent;
        button.textContent = "Copied";
        setTimeout(() => {{
          button.textContent = original;
        }}, 1200);
      }} catch (_error) {{
        button.textContent = "Copy failed";
      }}
    }}

    form.addEventListener("submit", async (event) => {{
      event.preventDefault();
      results.innerHTML = "";
      status.textContent = "Loading...";

      const problemNumber = document.getElementById("problem-number").value;
      const language = document.getElementById("language").value;
      const query = language ? `?language=${{encodeURIComponent(language)}}` : "";

      try {{
        const response = await fetch(`/problems/${{encodeURIComponent(problemNumber)}}${{query}}`);
        const payload = await response.json();

        if (!response.ok) {{
          throw new Error(payload.detail || "Request failed.");
        }}

        status.textContent = `Found ${{payload.implementations.length}} implementation(s) for problem ${{payload.problem_number}}.`;
        results.innerHTML = payload.implementations.map((implementation) => `
          <article class="card">
            <header>
              <div class="card-meta">
                <strong>${{escapeHtml(implementation.file_name)}}</strong>
                <span class="language-badge">${{escapeHtml(implementation.language)}}</span>
              </div>
              <button
                class="copy-button"
                type="button"
                data-code="${{escapeHtml(implementation.code)}}"
              >
                Copy
              </button>
            </header>
            <pre><code>${{escapeHtml(implementation.code)}}</code></pre>
          </article>
        `).join("");
        document.querySelectorAll(".copy-button").forEach((button) => {{
          button.addEventListener("click", () => copyCode(button.dataset.code, button));
        }});
      }} catch (error) {{
        status.textContent = error.message;
      }}
    }});
  </script>
</body>
</html>
"""


def find_implementations(
    problem_number: int,
    language: str | None = None,
) -> list[Implementation]:
    if language is not None and language not in LANGUAGE_SUFFIXES:
        supported_languages = ", ".join(LANGUAGE_SUFFIXES)
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported language '{language}'. "
                f"Use one of: {supported_languages}."
            ),
        )

    requested_languages = [language] if language else list(LANGUAGE_SUFFIXES)
    implementations: list[Implementation] = []

    for current_language in requested_languages:
        suffix = LANGUAGE_SUFFIXES[current_language]
        path = ROOT / f"{problem_number}{suffix}"
        if not path.exists():
            continue

        implementations.append(
            Implementation(
                file_name=path.name,
                language=current_language,
                code=path.read_text(encoding="utf-8"),
            )
        )

    return implementations


@app.get("/", response_class=HTMLResponse)
def homepage() -> HTMLResponse:
    return HTMLResponse(render_homepage())


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/problems/{problem_number}", response_model=ProblemCodeResponse)
def get_problem_code(
    problem_number: int,
    language: str | None = Query(
        default=None,
        description="Optional language filter: python, cpp, c, or go.",
    ),
) -> ProblemCodeResponse:
    implementations = find_implementations(problem_number, language)
    if not implementations:
        raise HTTPException(
            status_code=404,
            detail=f"No implementation found for Project Euler problem {problem_number}.",
        )

    return ProblemCodeResponse(
        problem_number=problem_number,
        implementations=implementations,
    )
