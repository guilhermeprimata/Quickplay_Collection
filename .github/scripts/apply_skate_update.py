from pathlib import Path
import base64
import gzip
import hashlib

EXPECTED_B64_LEN = 98404
EXPECTED_SHA256 = "fd49ee6d6fab9dd79178170bdce111dca35101878cbd6863515cb1b28638c06b"

parts = []
for i in range(5):
    parts.append(Path(f".github/scripts/skate_payload_{i:02d}.txt").read_text(encoding="utf-8").strip())
for i in range(7):
    parts.append(Path(f".github/scripts/skate_tail_{i:02d}.txt").read_text(encoding="utf-8").strip())

payload = "".join(parts)
if len(payload) != EXPECTED_B64_LEN:
    raise SystemExit(f"Payload length mismatch: {len(payload)} != {EXPECTED_B64_LEN}")

data = gzip.decompress(base64.b64decode(payload))
actual = hashlib.sha256(data).hexdigest()
if actual != EXPECTED_SHA256:
    raise SystemExit(f"SHA-256 mismatch: {actual} != {EXPECTED_SHA256}")

Path("skate_or_die.html").write_bytes(data)
print(f"Wrote skate_or_die.html ({len(data)} bytes, sha256={actual})")
