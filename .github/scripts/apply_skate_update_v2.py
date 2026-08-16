from pathlib import Path
import base64, gzip, hashlib

EXPECTED_SHA256 = 'fd49ee6d6fab9dd79178170bdce111dca35101878cbd6863515cb1b28638c06b'
EXPECTED_B64_LEN = 98404
EXPECTED_GIT_BLOB = 'aebe83d8103f58911e9f8a0c2752fec9f48c1f02'

# Exact ordered chunks from the locally approved build.
# The first four cover bytes 0..43999 of the base64 stream; tails cover the remainder.
ORDERED_BLOB_SHA1 = [
    '781c5cdd64df6a96b76693f6a063b274ecd9ec1d',
    'c82c3995ba90dcce68046996158d6196ae342aea',
    '2495db22f13b3b458048505aea5c2f2bfe5887b9',
    'b75a05d40b1b761d5b768aabf031af9a07dfc8d7',
    'b102b296784bd965e67267a3cb10678ce18c7f8e',
    'cbe5257ee558526f248fedd1f973e0c152874810',
    'a6fa142a96c5d08893a1c7a1b556198a7919dda8',
    'a48d9303b596182328967f8ce5e3060fe870f06d',
    '43f13f3711f32e1671a0db980aadab0cb9f3d2ce',
    '0868d74cb5ca7dde62dad16373e24d991ddbcb05',
    '4f067df50cfe7ece7baa3804340a7a37e4cc8539',
]

def git_blob_sha(data: bytes) -> str:
    header = f'blob {len(data)}\0'.encode()
    return hashlib.sha1(header + data).hexdigest()

candidates = {}
for p in sorted(Path('.github/scripts').glob('*.txt')):
    raw = p.read_bytes().strip()
    sha = git_blob_sha(raw)
    candidates.setdefault(sha, []).append((p, raw))

parts = []
for sha in ORDERED_BLOB_SHA1:
    matches = candidates.get(sha)
    if not matches:
        available = '\n'.join(f'{k}  {v[0][0]}' for k, v in sorted(candidates.items()))
        raise SystemExit(f'Missing exact fragment {sha}. Available fragments:\n{available}')
    p, raw = matches[0]
    print(f'Using {sha} from {p} ({len(raw)} chars)')
    parts.append(raw)

payload = b''.join(parts)
if len(payload) != EXPECTED_B64_LEN:
    raise SystemExit(f'Payload length mismatch: {len(payload)} != {EXPECTED_B64_LEN}')

data = gzip.decompress(base64.b64decode(payload, validate=True))
sha256 = hashlib.sha256(data).hexdigest()
blob = git_blob_sha(data)
if sha256 != EXPECTED_SHA256:
    raise SystemExit(f'SHA-256 mismatch: {sha256} != {EXPECTED_SHA256}')
if blob != EXPECTED_GIT_BLOB:
    raise SystemExit(f'Git blob mismatch: {blob} != {EXPECTED_GIT_BLOB}')

Path('skate_or_die.html').write_bytes(data)
print(f'OK: wrote skate_or_die.html ({len(data)} bytes, sha256={sha256}, blob={blob})')
