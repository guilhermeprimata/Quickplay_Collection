from pathlib import Path
import importlib.util

src=Path('.github/scripts/apply_fullscreen_landscape.py')
spec=importlib.util.spec_from_file_location('ppg_apply',src)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def normalize(path, marker, runtime):
    s=path.read_text(encoding='utf-8')
    token='<!-- '+marker+' -->'
    start=s.find(token)
    if start>=0:
        end=s.find('</script>',start)
        if end>=0:
            s=s[:start]+s[end+9:]
    pos=s.lower().rfind('</body>')
    if pos>=0:
        s=s[:pos]+runtime+'\n'+s[pos:]
    else:
        pos=s.lower().rfind('</html>')
        s=s[:pos]+runtime+'\n'+s[pos:] if pos>=0 else s+runtime
    path.write_text(s,encoding='utf-8')

idx=Path('index.html')
normalize(idx,mod.MENU_MARK,mod.menu_runtime)
for p in sorted(Path('.').glob('*.html')):
    if p.name.lower() in ('index.html','menu_minigames.html'):
        continue
    s=p.read_text(encoding='utf-8')
    if mod.GAME_MARK in s:
        normalize(p,mod.GAME_MARK,mod.game_runtime)

# Structural gate: marker must precede </body>, never trail </html>.
for p in [idx]+[x for x in Path('.').glob('*.html') if x.name.lower() not in ('index.html','menu_minigames.html')]:
    s=p.read_text(encoding='utf-8')
    marker=mod.MENU_MARK if p.name=='index.html' else mod.GAME_MARK
    if marker not in s:
        continue
    m=s.find(marker); body=s.lower().rfind('</body>'); html=s.lower().rfind('</html>')
    assert body<0 or m<body, f'{p}: runtime after body close'
    assert html<0 or m<html, f'{p}: runtime after html close'
print('PLACEMENT_PASS')
