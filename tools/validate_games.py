from __future__ import annotations

import html
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {"index.html", "menu_minigames.html"}
GAMES = sorted(p for p in ROOT.glob("*.html") if p.name not in EXCLUDE)
SCRIPT_RE = re.compile(r"<script\b(?P<attrs>[^>]*)>(?P<body>.*?)</script\s*>", re.I | re.S)
REMOTE_RE = re.compile(r"\b(?:src|href)\s*=\s*([\"'])(https?://[^\"']+)\1", re.I)
BRAND_PATTERNS = [
    re.compile(r"Banco\s+do\s+Brasil", re.I),
    re.compile(r"BB\s+Estilo", re.I),
    re.compile(r"(?:logo|marca)[-_ ]?bb\b", re.I),
    re.compile(r"bb\.com\.br", re.I),
]

failures: list[str] = []
warnings: list[str] = []
rows: list[tuple[str, int, int, int, int]] = []


def js_type(attrs: str) -> str | None:
    m = re.search(r"\btype\s*=\s*([\"'])(.*?)\1", attrs, re.I | re.S)
    return m.group(2).strip().lower() if m else None


def has_src(attrs: str) -> str | None:
    m = re.search(r"\bsrc\s*=\s*([\"'])(.*?)\1", attrs, re.I | re.S)
    return m.group(2).strip() if m else None


def node_check(code: str, suffix: str, label: str) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=suffix, delete=False) as f:
        f.write(code)
        temp = Path(f.name)
    try:
        result = subprocess.run(["node", "--check", str(temp)], text=True, capture_output=True)
        if result.returncode:
            detail = (result.stderr or result.stdout).strip().replace(str(temp), label)
            failures.append(f"{label}: JavaScript syntax error\n{detail}")
    finally:
        temp.unlink(missing_ok=True)


for path in GAMES:
    text = path.read_text(encoding="utf-8", errors="strict")
    low = text.lower()
    if len(re.findall(r"<!doctype\s+html", text, re.I)) != 1:
        failures.append(f"{path.name}: expected exactly one HTML doctype")
    if "</html>" not in low:
        failures.append(f"{path.name}: missing closing </html>")

    inline_count = 0
    external_js = 0
    for idx, match in enumerate(SCRIPT_RE.finditer(text), 1):
        attrs = match.group("attrs") or ""
        src = has_src(attrs)
        if src:
            external_js += 1
            failures.append(f"{path.name}: external script dependency violates standalone rule: {src}")
            continue
        typ = js_type(attrs)
        if typ and typ not in {"text/javascript", "application/javascript", "module"}:
            continue
        inline_count += 1
        suffix = ".mjs" if typ == "module" else ".js"
        node_check(match.group("body"), suffix, f"{path.name} script#{idx}")

    remote_refs = [u for _, u in REMOTE_RE.findall(text)]
    remote_non_js = [u for u in remote_refs if not re.search(r"\.js(?:[?#]|$)", u, re.I)]
    if remote_non_js:
        warnings.append(f"{path.name}: remote non-JS assets: {', '.join(remote_non_js[:6])}")

    brand_hits = 0
    for pattern in BRAND_PATTERNS:
        found = pattern.findall(text)
        brand_hits += len(found)
    if brand_hits:
        failures.append(f"{path.name}: direct Banco do Brasil branding signal(s) detected: {brand_hits}")

    pause = int("ppg-quality-controls-runtime" in text or bool(re.search(r"\bpause\b|\bpaused\b|pausar|pausado", text, re.I)))
    restart = int(bool(re.search(r"restart|resetar|resetgame|newgame|novo jogo|start again", text, re.I)))
    rows.append((path.name, inline_count, external_js, pause, restart))

report = [
    "# Quickplay Collection — standalone validation",
    "",
    "Validation executed with Node.js syntax checking for every inline JavaScript block in every game HTML.",
    "",
    "| Game | Inline JS blocks | External JS | Pause signal | Restart/New Game signal |",
    "|---|---:|---:|:---:|:---:|",
]
for name, inline_count, external_js, pause, restart in rows:
    report.append(f"| `{name}` | {inline_count} | {external_js} | {'✅' if pause else '—'} | {'✅' if restart else '—'} |")
report += [
    "",
    "## Result",
    "",
    f"- Games checked: **{len(GAMES)}**",
    f"- JavaScript syntax failures: **{sum('JavaScript syntax error' in x for x in failures)}**",
    f"- External JavaScript dependencies: **{sum('external script dependency' in x for x in failures)}**",
    f"- Direct Banco do Brasil branding signals: **{sum('branding signal' in x for x in failures)}**",
    f"- Remote non-JS asset warnings: **{len(warnings)}**",
]
if warnings:
    report += ["", "## Warnings", ""] + [f"- {html.escape(w)}" for w in warnings]
if failures:
    report += ["", "## Failures", ""] + [f"- {html.escape(f).replace(chr(10), '<br>')}" for f in failures]
(ROOT / "QUALITY_VALIDATION.md").write_text("\n".join(report) + "\n", encoding="utf-8")

if failures:
    print(f"VALIDATION_FAIL games={len(GAMES)} failures={len(failures)} warnings={len(warnings)}")
    for failure in failures:
        print("FAIL:", failure)
    raise SystemExit(1)
print(f"VALIDATION_OK games={len(GAMES)} inline_scripts={sum(r[1] for r in rows)} warnings={len(warnings)}")
