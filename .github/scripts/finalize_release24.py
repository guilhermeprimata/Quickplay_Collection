from pathlib import Path
import hashlib, lzma, struct, re, sys, zipfile, tempfile, subprocess

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.')
DELTA=Path(sys.argv[2] if len(sys.argv)>2 else 'release24.qpd.xz')

EXPECTED_GIT={
'advinhe_o_numero.html':'f5e05120cf1a185ee3e4cfc8d81bf42dac884535',
'alien_threat.html':'14d9d3a06cdb118b102097e9e55051354ba84a24',
'bow_and_arrow.html':'7736dbc9bd9a172de7a184734b35f1079393bd9b',
'brain_matrix.html':'abc67a5ec60a0e7d15cc5a1214f510f3094804b6',
'campo_minado.html':'b710adc83fb5156b6cfad25365642d379db597e2',
'click_speed.html':'63c24ed14c205b75f9c4c2716a495328546a62bc',
'corrida_de_cavalos.html':'7f7e9dcc8d160fcc2f5dd7d86cfbbb4f0fbedd82',
'domination_wars.html':'9f6b28120775e30d2f16449a0802d4d0d9a89746',
'dropworks.html':'a22611858f903e2cb1bbb67900896b5b63a44574',
'foguetinho.html':'fd7a9c11139920cbd8c0c8cb2a8eab2ff3448fb5',
'jogo_da_forca.html':'f645ee49a1df583ef6922731f19ee83a9c21e795',
'jogo_da_velha.html':'374febf2ca7639894061684d52c4a94f4e8c20e0',
'kombo_blocks.html':'6870660f706d5d22fc8bd965074a2e2c1b1d4b71',
'memory_genius.html':'3bee3db9091e67860991fef5c0587c6369d6255c',
'pixel_bomberman.html':'a7323a09735c1e2eaa828bb2da15572654a763ba',
'pixel_joust.html':'5399d5180f8bbabb22209810b6ba8f1221f5119a',
'pong.html':'9ef6e3bbaa4498336a37d236717437a38b57bcff',
'rift_run.html':'1bf19771b39343c8fad8f2bde7e59293d1c42d28',
'salve_os_gatinhos.html':'521ae6da5dc3712d8cb6608811dcf1c73befcd56',
'snowball_avalanche.html':'3b317e4d66ad6a2b8dc0517d5c1b0256e6a9e19d',
'sudoku.html':'f3d60a47e9786f9c1fbdae19b4b05fe26e824c2d',
'the_worm.html':'3b0fed2df19d38f3b3d28ac0057605032aa5ea2e',
'torre_de_hanoi.html':'c128f159dfb12c0573130e48264fca520939412f',
'atomic_raid.html':'55756941d06eab3dc29e0cb07799bbdf70aebeb2',
}

def git_blob_sha(data):
    return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()

def parse_qpd(raw,endian):
    if raw[:4]!=b'QPD1': raise ValueError('bad magic')
    pos=4
    count=struct.unpack_from(endian+'H',raw,pos)[0]; pos+=2
    if not 1<=count<=100: raise ValueError('bad count')
    entries=[]
    for _ in range(count):
        nl=struct.unpack_from(endian+'H',raw,pos)[0]; pos+=2
        if not 1<=nl<=4096: raise ValueError('bad name length')
        name=raw[pos:pos+nl].decode(); pos+=nl
        srcsha=raw[pos:pos+32]; pos+=32
        dstsha=raw[pos:pos+32]; pos+=32
        nops=struct.unpack_from(endian+'I',raw,pos)[0]; pos+=4
        if nops>2000000: raise ValueError('bad op count')
        ops=[]
        for _ in range(nops):
            typ=raw[pos:pos+1]; pos+=1
            if typ==b'C':
                off,ln=struct.unpack_from(endian+'II',raw,pos); pos+=8
                ops.append(('C',off,ln))
            elif typ==b'L':
                ln=struct.unpack_from(endian+'I',raw,pos)[0]; pos+=4
                lit=raw[pos:pos+ln]; pos+=ln
                ops.append(('L',lit))
            else: raise ValueError('bad op')
        entries.append((name,srcsha,dstsha,ops))
    if pos!=len(raw): raise ValueError('trailing bytes')
    return entries

def apply_delta():
    raw=lzma.decompress(DELTA.read_bytes())
    entries=None; errors=[]
    for endian in ('<','>'):
        try:
            cand=parse_qpd(raw,endian)
            for name,srcsha,_,_ in cand:
                p=ROOT/name; src=p.read_bytes() if p.exists() else b''
                if hashlib.sha256(src).digest()!=srcsha: raise ValueError('source '+name)
            entries=cand; break
        except Exception as e: errors.append(str(e))
    if entries is None: raise SystemExit('QPD source validation failed: '+' | '.join(errors))
    for name,_,dstsha,ops in entries:
        p=ROOT/name; src=p.read_bytes() if p.exists() else b''; out=bytearray()
        for op in ops:
            if op[0]=='C':
                _,off,ln=op
                if off+ln>len(src): raise SystemExit('copy outside source '+name)
                out.extend(src[off:off+ln])
            else: out.extend(op[1])
        out=bytes(out)
        if hashlib.sha256(out).digest()!=dstsha: raise SystemExit('target hash '+name)
        p.write_bytes(out)
    print('Applied QPD entries:',len(entries))

def patch_hub():
    p=ROOT/'index.html'; s=p.read_text('utf-8')
    gs=s.index('const GAMES=['); ts=s.index('const TIERS=',gs); ge=s.rfind('];',gs,ts)
    if ge<0: raise SystemExit('GAMES closing bracket missing')
    block=s[gs:ge+2]
    def edit_desc(block,gid,new):
        for m in re.finditer(r'\{[^{}]*\}',block,re.S):
            obj=m.group(0)
            if re.search(r"\bid\s*:\s*['\"]"+re.escape(gid)+r"['\"]",obj):
                q=re.search(r"\bdesc\s*:\s*(['\"])(.*?)\1",obj,re.S)
                if not q: raise SystemExit('desc missing '+gid)
                quote=q.group(1); escaped=new.replace('\\','\\\\').replace(quote,'\\'+quote)
                obj2=obj[:q.start(2)]+escaped+obj[q.end(2):]
                return block[:m.start()]+obj2+block[m.end():]
        raise SystemExit('hub id missing '+gid)
    block=edit_desc(block,'domination_wars','Guerra territorial orgânica com curvas contínuas, trilhas vulneráveis, power-ups e IA agressiva.')
    block=edit_desc(block,'neon_pong','Pong hyper-arcade com combos, supers, power-ups, arenas caóticas e IA em três níveis.')
    block=edit_desc(block,'forca_neon','Forca neon com dicas progressivas, streak, pontuação e ranking local por idioma.')
    if not re.search(r"\bid\s*:\s*['\"]atomic_raid['\"]",block):
        atomic="{id:'atomic_raid',name:'ATOMIC RAID',emoji:'☢️',file:'atomic_raid.html',desc:'Arcade shooter procedural autocontido: pilote, combata, gerencie combustível e evolua sua nave.',new:true}"
        close=block.rfind(']'); before=block[:close].rstrip(); sep='' if before.endswith(('[',',')) else ','
        block=before+sep+'\n  '+atomic+'\n'+block[close:]
    s=s[:gs]+block+s[ge+2:]
    ts=s.index('const TIERS=',gs)
    m=re.search(r"\bA\s*:\s*\[([^\]]*)\]",s[ts:],re.S)
    if not m: raise SystemExit('Tier A missing')
    inner=m.group(1)
    if not re.search(r"['\"]atomic_raid['\"]",inner):
        trimmed=inner.rstrip(); add=("," if trimmed and not trimmed.endswith(',') else '')+"'atomic_raid'"
        newinner=trimmed+add+inner[len(trimmed):]
        a=ts+m.start(1); b=ts+m.end(1); s=s[:a]+newinner+s[b:]
    p.write_text(s,'utf-8')

def validate():
    bad=[]
    for name,exp in EXPECTED_GIT.items():
        p=ROOT/name
        if not p.is_file(): bad.append('missing '+name); continue
        got=git_blob_sha(p.read_bytes())
        if got!=exp: bad.append(name+': '+got+' != '+exp)
        txt=p.read_text('utf-8',errors='replace').lstrip().lower()
        if '<!doctype html' not in txt[:300] or '</html>' not in txt[-500:]: bad.append('html envelope '+name)
    if bad: raise SystemExit('Canonical validation failed:\n'+'\n'.join(bad))
    hub=(ROOT/'index.html').read_text('utf-8'); gs=hub.index('const GAMES=['); ts=hub.index('const TIERS=',gs)
    objs=re.findall(r'\{[^{}]*\}',hub[gs:ts],re.S); ids=[]; files=[]
    for obj in objs:
        mi=re.search(r"\bid\s*:\s*(['\"])(.*?)\1",obj,re.S); mf=re.search(r"\bfile\s*:\s*(['\"])(.*?)\1",obj,re.S)
        if mi and mf: ids.append(mi.group(2)); files.append(mf.group(2))
    if len(ids)!=30: raise SystemExit('Expected 30 hub games, found '+str(len(ids)))
    if len(set(ids))!=len(ids): raise SystemExit('Duplicate hub IDs')
    if ids.count('atomic_raid')!=1: raise SystemExit('Atomic card count != 1')
    missing=[f for f in files if not (ROOT/f).is_file()]
    if missing: raise SystemExit('Broken hub targets: '+', '.join(missing))
    tiers=[]; tier_text=hub[ts:]
    for _,inner in re.findall(r"\b([ABCD])\s*:\s*\[([^\]]*)\]",tier_text,re.S): tiers+=re.findall(r"['\"]([^'\"]+)['\"]",inner)
    if set(tiers)!=set(ids): raise SystemExit('Tier IDs differ from hub IDs')
    ma=re.search(r"\bA\s*:\s*\[([^\]]*)\]",tier_text,re.S)
    if not ma or 'atomic_raid' not in ma.group(1): raise SystemExit('Atomic not in Tier A')
    with tempfile.TemporaryDirectory() as td:
        n=0
        for name in EXPECTED_GIT:
            text=(ROOT/name).read_text('utf-8',errors='replace')
            for attrs,body in re.findall(r'<script\b([^>]*)>(.*?)</script\s*>',text,re.I|re.S):
                if re.search(r'\bsrc\s*=',attrs,re.I): continue
                mt=re.search(r'\btype\s*=\s*["\']([^"\']+)',attrs,re.I)
                if mt and mt.group(1).lower() in {'application/json','application/ld+json','importmap','speculationrules'}: continue
                if not body.strip(): continue
                f=Path(td)/('s'+str(n)+'.js'); n+=1; f.write_text(body,'utf-8')
                r=subprocess.run(['node','--check',str(f)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                if r.returncode: raise SystemExit('JS syntax failed '+name+'\n'+r.stderr)
        print('JS syntax blocks checked:',n)

def rebuild_zip():
    z=ROOT/'Quickplay_Collection_COMPLETE.zip'; sf=ROOT/'Quickplay_Collection_COMPLETE.zip.sha256'
    if z.exists(): z.unlink()
    inc=[]
    for p in ROOT.iterdir():
        if not p.is_file() or p.name in {z.name,sf.name}: continue
        if p.suffix.lower() in {'.html','.md','.txt'} or p.name=='.nojekyll': inc.append(p)
    inc.sort(key=lambda p:p.name.lower())
    with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
        for p in inc: zz.write(p,p.name)
    digest=hashlib.sha256(z.read_bytes()).hexdigest(); sf.write_text(digest+'  '+z.name+'\n','ascii')
    print('ZIP rebuilt:',z.stat().st_size,'bytes',digest)

apply_delta(); patch_hub(); validate(); rebuild_zip(); print('FINALIZE_RELEASE24_OK')
