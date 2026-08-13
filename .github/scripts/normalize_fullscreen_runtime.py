from pathlib import Path
import importlib.util

src=Path('.github/scripts/apply_fullscreen_landscape.py')
spec=importlib.util.spec_from_file_location('ppg_apply',src)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def normalize(path, marker, runtime):
    s=path.read_text(encoding='utf-8')
    token='<!-- '+marker+' -->'
    # Remove every previous injected block, wherever it landed.
    while token in s:
        start=s.find(token)
        end=s.find('</script>',start)
        if end<0:
            s=s[:start]
            break
        s=s[:start]+s[end+9:]
    # Reinsert inside the document, immediately before </body> when possible.
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
print('NORMALIZE_DONE')
