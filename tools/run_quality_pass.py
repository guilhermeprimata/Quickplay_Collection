from pathlib import Path

path = Path(__file__).with_name('apply_quality_pass.py')
source = path.read_text(encoding='utf-8')
old = '''replace_all("advinhe_o_numero.html", 'let tempoRestante = 180;', 'let tempoRestante = 90;', "timer state 180s → 90s", minimum=2)'''
new = '''replace_all("advinhe_o_numero.html", 'let tempoRestante = 180;', 'let tempoRestante = 90;', "initial timer state 180s → 90s")
replace_all("advinhe_o_numero.html", '      tempoRestante = 180;', '      tempoRestante = 90;', "reset timer state 180s → 90s")'''
if old not in source:
    raise SystemExit('quality wrapper: expected Adivinhe assertion anchor not found')
source = source.replace(old, new, 1)
exec(compile(source, str(path), 'exec'), {'__name__': '__main__', '__file__': str(path)})
