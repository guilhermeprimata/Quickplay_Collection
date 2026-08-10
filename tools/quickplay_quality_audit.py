from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {"index.html", "menu_minigames.html"}

FEATURES = {
    "pause": [r"\bpause\b", r"\bpaused\b", r"pausar", r"pausado"],
    "restart": [r"restart", r"resetar", r"resetgame", r"newgame", r"novo jogo", r"start again"],
    "touch": [r"touchstart", r"touchmove", r"pointerdown", r"pointerup", r"d-pad", r"joystick"],
    "keyboard": [r"keydown", r"keyup", r"arrowup", r"keyw", r"\bwasd\b"],
    "audio": [r"audiocontext", r"webkitAudioContext", r"\bbgm\b", r"\bsfx\b"],
    "storage": [r"localStorage"],
    "i18n": [r"i18n", r"locale", r"languages?", r"pt-BR", r"zh-CN"],
    "about": [r"ppg-about", r"\bsobre\b"],
    "records": [r"ppg-records", r"leaderboard", r"recordes", r"high.?score"],
    "menu": [r"menu_minigames\.html", r"Mini Games"],
    "theme": [r"ppg-theme", r"modo claro", r"dark mode", r"theme"],
    "sound_toggle": [r"ppg-sound", r"Som ON", r"Som OFF", r"mute"],
}

TUNING_RE = re.compile(
    r"(?i)(difficulty|dificuldade|speed|veloc|enemy|inimig|spawn|gravity|gap|lives|vidas|timer|tempo|interval|cooldown|level|fase|target|alvo|score|pontos|ai\b|chance|probab|damage|dano|health|vida|max|min|threshold|combo|bomb|explos|block|obst|supply|reserve|water|fluid)"
)


def has_any(text: str, pats: list[str]) -> bool:
    return any(re.search(p, text, re.I) for p in pats)


def snippets(lines: list[str], limit: int = 14) -> list[str]:
    out: list[str] = []
    for n, line in enumerate(lines, 1):
        s = line.strip()
        if not s or len(s) > 260:
            continue
        if TUNING_RE.search(s) and re.search(r"\d", s):
            out.append(f"L{n}: {s}")
            if len(out) >= limit:
                break
    return out


def ppg_version(text: str) -> str:
    if "ppg_platform_prefs_v2" in text or "ppg_records_v2_" in text:
        return "v2"
    if "ppg-platform-script" in text:
        return "v1"
    return "none"


def native_pause(text: str) -> bool:
    core = text.split('<style id="ppg-platform-style">', 1)[0]
    return has_any(core, FEATURES["pause"])


def native_restart(text: str) -> bool:
    core = text.split('<style id="ppg-platform-style">', 1)[0]
    return has_any(core, FEATURES["restart"])


def native_touch(text: str) -> bool:
    core = text.split('<style id="ppg-platform-style">', 1)[0]
    return has_any(core, FEATURES["touch"])


def main() -> None:
    games = sorted(p for p in ROOT.glob("*.html") if p.name not in EXCLUDE)
    rows = []
    details = []
    for path in games:
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        flags = {k: has_any(text, v) for k, v in FEATURES.items()}
        pv = ppg_version(text)
        np = native_pause(text)
        nr = native_restart(text)
        nt = native_touch(text)
        canvas = "<canvas" in text.lower()
        interactive_keys = flags["keyboard"]
        touch_need = canvas and interactive_keys and not nt
        rows.append(
            (path.name, pv, np, nr, nt, touch_need, flags["audio"], flags["storage"], flags["i18n"], len(text))
        )
        hits = snippets(lines)
        details.append((path.name, hits))

    out = []
    out.append("# Quickplay Collection — automated quality audit\n")
    out.append("Generated from the repository contents. Heuristics are intentionally conservative; false positives are preferable to silently missing a control path.\n")
    out.append("| Game | Platform | Native pause | Native restart | Native touch | Touch gap? | Audio | Storage | i18n signal | Bytes |")
    out.append("|---|---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|")
    for r in rows:
        name, pv, np, nr, nt, gap, audio, storage, i18n, size = r
        yn = lambda x: "✅" if x else "—"
        out.append(f"| `{name}` | {pv} | {yn(np)} | {yn(nr)} | {yn(nt)} | {'⚠️' if gap else '—'} | {yn(audio)} | {yn(storage)} | {yn(i18n)} | {size} |")

    out.append("\n## Automated findings\n")
    old = [r[0] for r in rows if r[1] != "v2"]
    no_pause = [r[0] for r in rows if not r[2]]
    no_restart = [r[0] for r in rows if not r[3]]
    touch_gaps = [r[0] for r in rows if r[5]]
    out.append(f"- Platform layer not v2: {', '.join(f'`{x}`' for x in old) or 'none'}")
    out.append(f"- No native pause signal: {', '.join(f'`{x}`' for x in no_pause) or 'none'}")
    out.append(f"- No native restart/new-game signal: {', '.join(f'`{x}`' for x in no_restart) or 'none'}")
    out.append(f"- Canvas + keyboard but no native touch signal: {', '.join(f'`{x}`' for x in touch_gaps) or 'none'}")

    out.append("\n## Balance/tuning candidates\n")
    out.append("These are the first numeric lines in each game touching difficulty-related concepts, to make the manual balancing pass faster.\n")
    for name, hits in details:
        out.append(f"### `{name}`")
        if hits:
            out.extend(f"- `{h.replace('`', "'")}`" for h in hits)
        else:
            out.append("- No compact numeric tuning line detected by the heuristic.")
        out.append("")

    report = ROOT / "QUALITY_AUDIT_AUTOMATED.md"
    report.write_text("\n".join(out), encoding="utf-8")
    print(f"AUDIT_OK games={len(rows)} report={report.name}")


if __name__ == "__main__":
    main()
