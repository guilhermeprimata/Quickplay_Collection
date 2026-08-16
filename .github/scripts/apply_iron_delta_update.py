from __future__ import annotations

import base64
import gzip
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "iron_delta.html"
INDEX = ROOT / "index.html"
PATCH_FILES = sorted((ROOT / ".github" / "scripts").glob("iron_delta_patch_*.txt"))

OLD_SHA256 = "685da105f78571dcdabb7ca9a382465e161460a7468462df6015b72fbe06e2c6"
NEW_SHA256 = "85fd620548bf96b195af7e1593836f1ef170b4caabb167356c4e4e58e4e6d4c4"
NEW_GIT_BLOB = "a7537cd55e2f5018050a2e6e5b30e6ec0a4aa611"

OLD_CARD = "{file:'iron_delta.html',id:'iron_delta',name:'IRON DELTA',emoji:'✈️',desc:'Ataque em baixa altitude sobre rios procedurais: gerencie combustível, destrua pontes, inimigos e chefes e sobreviva ao delta.',new:true},"
NEW_CARD = "{file:'iron_delta.html',id:'iron_delta',name:'IRON DELTA',emoji:'✈️',desc:'Combate aéreo procedural sobre rios hostis: combustível, upgrades, bosses, checkpoints, desafio diário e rotas para dominar.',new:true},"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if len(PATCH_FILES) != 6:
    raise SystemExit(f"Expected 6 patch fragments, found {len(PATCH_FILES)}")

if sha256(TARGET) != OLD_SHA256:
    raise SystemExit(f"Unexpected source iron_delta.html SHA-256: {sha256(TARGET)}")

payload = "".join(p.read_text(encoding="utf-8").strip() for p in PATCH_FILES)
patch_bytes = gzip.decompress(base64.b64decode(payload))
patch_path = ROOT / ".github" / "scripts" / "iron_delta_update.patch"
patch_path.write_bytes(patch_bytes)

subprocess.run(["git", "apply", "--check", str(patch_path)], cwd=ROOT, check=True)
subprocess.run(["git", "apply", str(patch_path)], cwd=ROOT, check=True)

actual_sha = sha256(TARGET)
if actual_sha != NEW_SHA256:
    raise SystemExit(f"Patched IRON DELTA SHA mismatch: {actual_sha}")

blob = subprocess.check_output(["git", "hash-object", "iron_delta.html"], cwd=ROOT, text=True).strip()
if blob != NEW_GIT_BLOB:
    raise SystemExit(f"Patched IRON DELTA git blob mismatch: {blob}")

index = INDEX.read_text(encoding="utf-8")
if OLD_CARD not in index:
    if NEW_CARD not in index:
        raise SystemExit("IRON DELTA hub card signature not found")
else:
    index = index.replace(OLD_CARD, NEW_CARD, 1)
    INDEX.write_text(index, encoding="utf-8")

print("IRON DELTA canonical polished build reconstructed and hub card refreshed.")
print("SHA-256:", actual_sha)
print("Git blob:", blob)
