from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GAMES = [
    "advinhe_o_numero.html", "bow_and_arrow.html", "campo_minado.html", "click_speed.html",
    "corrida_de_cavalos.html", "dropworks.html", "foguetinho.html", "idle_trader.html",
    "jogo_da_forca.html", "jogo_da_velha.html", "kombo_blocks.html", "leaping_into_life.html",
    "memory_genius.html", "pixel_bomberman.html", "pong.html", "salve_os_gatinhos.html",
    "sudoku.html", "the_worm.html", "torre_de_hanoi.html", "tron.html",
]
PAUSE_NATIVE = {"dropworks.html", "kombo_blocks.html", "pong.html"}
RESTART_NATIVE = {
    "advinhe_o_numero.html", "campo_minado.html", "idle_trader.html", "jogo_da_forca.html",
    "jogo_da_velha.html", "memory_genius.html", "pong.html", "torre_de_hanoi.html", "tron.html",
    "dropworks.html", "kombo_blocks.html",
}

changes: dict[str, list[str]] = {g: [] for g in GAMES}
notes: dict[str, list[str]] = {g: [] for g in GAMES}


def load(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def save(name: str, text: str) -> None:
    (ROOT / name).write_text(text, encoding="utf-8")


def replace_all(name: str, old: str, new: str, label: str, *, minimum: int = 1) -> int:
    text = load(name)
    count = text.count(old)
    if count < minimum:
        raise RuntimeError(f"{name}: expected at least {minimum} occurrence(s) for {label}, found {count}")
    text = text.replace(old, new)
    save(name, text)
    changes[name].append(f"{label} ({count} replacement{'s' if count != 1 else ''})")
    return count


def replace_once(name: str, old: str, new: str, label: str) -> None:
    text = load(name)
    if old not in text:
        raise RuntimeError(f"{name}: anchor missing for {label}")
    save(name, text.replace(old, new, 1))
    changes[name].append(label)


def regex_once(name: str, pattern: str, replacement: str, label: str, flags: int = re.S) -> None:
    text = load(name)
    new, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f"{name}: regex expected 1 match for {label}, got {count}")
    save(name, new)
    changes[name].append(label)


# ---------------------------------------------------------------------------
# Standard pause layer. This is injected before game scripts, so requestAnimationFrame,
# setInterval, setTimeout, performance.now and Date.now all observe frozen gameplay time.
# It deliberately does not replace a game's native pause when one already exists.
# ---------------------------------------------------------------------------
PAUSE_LAYER = r'''
<style id="ppg-quality-controls-style">
#ppg-quality-pause-overlay{position:fixed;z-index:2147483635;inset:0;display:none;place-items:center;padding:18px;background:rgba(4,6,16,.82);backdrop-filter:blur(9px);font-family:Inter,"Segoe UI",system-ui,sans-serif;color:#fff}#ppg-quality-pause-overlay.open{display:grid}.ppg-quality-pause-card{width:min(440px,94vw);padding:24px;border:1px solid rgba(255,255,255,.18);border-radius:22px;background:linear-gradient(145deg,#17192d,#090b17);box-shadow:0 30px 100px #000a;text-align:center}.ppg-quality-pause-card h2{margin:0 0 8px;font-size:clamp(25px,5vw,38px);color:#e8dcff}.ppg-quality-pause-card p{margin:0 0 18px;color:#bcc2d8;line-height:1.45}.ppg-quality-pause-actions{display:grid;gap:9px}.ppg-quality-pause-actions button,.ppg-quality-pause-actions a{display:block;width:100%;padding:12px 14px;border:1px solid #ffffff22;border-radius:12px;background:#242941;color:#fff;font:800 14px/1.2 Inter,"Segoe UI",system-ui,sans-serif;text-decoration:none;cursor:pointer}.ppg-quality-pause-actions button:first-child{background:linear-gradient(135deg,#6d5cff,#27d9c0);color:#081016}.ppg-quality-pause-actions :is(button,a):hover{filter:brightness(1.13)}#ppg-quality-pause,#ppg-quality-restart{white-space:nowrap}.ppg-quality-paused body{overflow:hidden!important}
</style>
<script id="ppg-quality-controls-runtime">
(()=>{'use strict';
const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;
const ADD_RESTART=__ADD_RESTART__;
const realPerfNow=performance.now.bind(performance),realDateNow=Date.now.bind(Date),nativeRAF=window.requestAnimationFrame.bind(window),nativeSetInterval=window.setInterval.bind(window),nativeSetTimeout=window.setTimeout.bind(window);
let paused=false,pausePerf=0,pauseDate=0,perfOffset=0,dateOffset=0;
const gamePerfNow=()=>{const n=realPerfNow();return n-perfOffset-(paused?n-pausePerf:0)};
const gameDateNow=()=>{const n=realDateNow();return n-dateOffset-(paused?n-pauseDate:0)};
try{Object.defineProperty(performance,'now',{value:gamePerfNow,configurable:true})}catch{}
try{Date.now=gameDateNow}catch{}
window.requestAnimationFrame=cb=>nativeRAF(function gate(){if(paused)return nativeRAF(gate);cb(gamePerfNow())});
window.setInterval=(fn,ms,...args)=>typeof fn==='function'?nativeSetInterval(()=>{if(!paused)fn(...args)},ms):nativeSetInterval(fn,ms,...args);
window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};
const L={
 en:{pause:'Pause',paused:'Paused',desc:'Gameplay time and controls are frozen.',resume:'Resume game',restart:'New game',exit:'Exit to Mini Games'},
 'pt-BR':{pause:'Pausar',paused:'Pausado',desc:'O tempo e os controles da partida estão congelados.',resume:'Continuar jogo',restart:'Novo jogo',exit:'Sair para Mini Games'},
 es:{pause:'Pausa',paused:'En pausa',desc:'El tiempo y los controles están congelados.',resume:'Continuar',restart:'Nueva partida',exit:'Salir a Mini Games'},
 fr:{pause:'Pause',paused:'En pause',desc:'Le temps et les contrôles sont figés.',resume:'Reprendre',restart:'Nouvelle partie',exit:'Quitter vers Mini Games'},
 de:{pause:'Pause',paused:'Pausiert',desc:'Spielzeit und Steuerung sind angehalten.',resume:'Fortsetzen',restart:'Neues Spiel',exit:'Zu Mini Games'},
 it:{pause:'Pausa',paused:'In pausa',desc:'Tempo e controlli di gioco sono fermi.',resume:'Riprendi',restart:'Nuova partita',exit:'Esci ai Mini Games'},
 tr:{pause:'Duraklat',paused:'Duraklatıldı',desc:'Oyun süresi ve kontroller donduruldu.',resume:'Devam et',restart:'Yeni oyun',exit:"Mini Games'e çık"},
 ru:{pause:'Пауза',paused:'Игра на паузе',desc:'Игровое время и управление остановлены.',resume:'Продолжить',restart:'Новая игра',exit:'В Mini Games'},
 ja:{pause:'一時停止',paused:'一時停止中',desc:'ゲーム時間と操作を停止しています。',resume:'再開',restart:'新しいゲーム',exit:'ミニゲームへ'},
 ko:{pause:'일시정지',paused:'일시정지됨',desc:'게임 시간과 조작이 멈췄습니다.',resume:'계속',restart:'새 게임',exit:'미니게임으로'},
 'zh-CN':{pause:'暂停',paused:'已暂停',desc:'游戏时间和操作已冻结。',resume:'继续',restart:'新游戏',exit:'返回小游戏菜单'}
};
function lang(){const raw=(document.documentElement.lang||navigator.language||'en').replace('_','-');if(/^pt/i.test(raw))return'pt-BR';if(/^zh/i.test(raw))return'zh-CN';const k=raw.split('-')[0];return L[k]?k:'en'}function t(k){return(L[lang()]||L.en)[k]||L.en[k]}
let overlay,pauseBtn,restartBtn;
function refresh(){if(pauseBtn)pauseBtn.textContent='⏸ '+t('pause');if(restartBtn)restartBtn.textContent='↻ '+t('restart');if(!overlay)return;overlay.querySelector('h2').textContent=t('paused');overlay.querySelector('p').textContent=t('desc');overlay.querySelector('[data-act=resume]').textContent='▶ '+t('resume');overlay.querySelector('[data-act=restart]').textContent='↻ '+t('restart');overlay.querySelector('[data-act=exit]').textContent='↩ '+t('exit')}
function releaseKeys(){for(const key of ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','w','a','s','d','W','A','S','D',' '])document.dispatchEvent(new KeyboardEvent('keyup',{key,bubbles:true}))}
function setPaused(next){next=!!next;if(next===paused)return;if(next){releaseKeys();pausePerf=realPerfNow();pauseDate=realDateNow();paused=true}else{perfOffset+=realPerfNow()-pausePerf;dateOffset+=realDateNow()-pauseDate;paused=false}window.__PPG_PAUSED__=paused;document.documentElement.classList.toggle('ppg-quality-paused',paused);overlay?.classList.toggle('open',paused);document.dispatchEvent(new CustomEvent(paused?'ppg:pause':'ppg:resume'));if(!paused)nativeSetTimeout(()=>document.activeElement?.blur?.(),0)}
function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}
function mount(){if(document.getElementById('ppg-quality-pause-overlay'))return;overlay=document.createElement('div');overlay.id='ppg-quality-pause-overlay';overlay.innerHTML='<div class="ppg-quality-pause-card" role="dialog" aria-modal="true"><h2></h2><p></p><div class="ppg-quality-pause-actions"><button data-act="resume"></button><button data-act="restart"></button><a data-act="exit" href="menu_minigames.html"></a></div></div>';document.body.appendChild(overlay);overlay.querySelector('[data-act=resume]').onclick=()=>setPaused(false);overlay.querySelector('[data-act=restart]').onclick=restart;const toolbar=document.getElementById('ppg-toolbar');if(toolbar){pauseBtn=document.createElement('button');pauseBtn.id='ppg-quality-pause';pauseBtn.type='button';pauseBtn.onclick=()=>setPaused(!paused);const menu=toolbar.querySelector('a[href*="menu_minigames"]');toolbar.insertBefore(pauseBtn,menu||null);if(ADD_RESTART){restartBtn=document.createElement('button');restartBtn.id='ppg-quality-restart';restartBtn.type='button';restartBtn.onclick=restart;toolbar.insertBefore(restartBtn,menu||null)}}refresh();new MutationObserver(refresh).observe(document.documentElement,{attributes:true,attributeFilter:['lang']})}
document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(document.querySelector('.ppg-modal.open,dialog[open],.modal.open')&&!paused)return;e.preventDefault();e.stopImmediatePropagation();setPaused(!paused);return}if(paused){e.preventDefault();e.stopImmediatePropagation()}},true);for(const ev of ['pointerdown','mousedown','touchstart','click'])document.addEventListener(ev,e=>{if(paused&&!e.target.closest('#ppg-quality-pause-overlay')){e.preventDefault();e.stopImmediatePropagation()}},true);
window.PPGQualityControls={pause:()=>setPaused(true),resume:()=>setPaused(false),toggle:()=>setPaused(!paused),restart,get paused(){return paused}};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount);else mount();
})();
</script>
'''


def inject_pause(name: str) -> None:
    text = load(name)
    if "ppg-quality-controls-runtime" in text:
        return
    if "</head>" not in text:
        raise RuntimeError(f"{name}: no </head> for pause injection")
    layer = PAUSE_LAYER.replace("__ADD_RESTART__", "true" if name not in RESTART_NATIVE else "false")
    save(name, text.replace("</head>", layer + "\n</head>", 1))
    changes[name].append("standard pause (Esc + modal with resume/new game/menu)" + (" + toolbar New Game" if name not in RESTART_NATIVE else ""))


# ---------------------------------------------------------------------------
# Pixel Bomber: replace the prototype-grade core with a complete, fairer arena loop.
# ---------------------------------------------------------------------------
BOMBER_CORE = r'''<script id="pixel-bomber-core">
const canvas=document.getElementById('game'),ctx=canvas.getContext('2d'),tileSize=32,cols=canvas.width/tileSize,rows=canvas.height/tileSize;
const MAX_LIVES=3,MAX_BOMBS=2;let map=[],bombs=[],flames=[],enemies=[],score=0,lives=MAX_LIVES,level=1,enemyMoveTimer=0,framesSinceDamage=0,invulnerable=0,transitionFrames=0,gameOver=false;
const player={x:0,y:0};
const hud=document.getElementById('hud'),status=document.getElementById('bomber-status');
const spritePlayer=[[0,1,0],[1,1,1],[1,0,1]],spriteEnemy=[[1,1,1],[1,0,1],[1,1,1]],spriteBlock=[[1,1,1],[1,0,1],[1,1,1]],spriteWall=[[1,0,1],[0,1,0],[1,0,1]];
function sfx(f,d=.045){try{window.PPGPlatform?.sfx?.(f,d)}catch{}}
function safeStart(x,y){return x>=0&&y>=0&&x+y<=2}
function tileOpen(x,y){return !!map[y]&&map[y][x]==='empty'}
function bombAt(x,y){return bombs.some(b=>b.x===x&&b.y===y)}
function canWalk(x,y){return tileOpen(x,y)&&!bombAt(x,y)}
function drawPixelArt(x,y,color,pattern){const cell=8,ox=x*tileSize+(tileSize-pattern[0].length*cell)/2,oy=y*tileSize+(tileSize-pattern.length*cell)/2;ctx.fillStyle=color;for(let i=0;i<pattern.length;i++)for(let j=0;j<pattern[i].length;j++)if(pattern[i][j])ctx.fillRect(ox+j*cell,oy+i*cell,cell,cell)}
function initMap(){map=[];const blockChance=Math.min(.245,.155+(level-1)*.012);for(let y=0;y<rows;y++){map[y]=[];for(let x=0;x<cols;x++){if(safeStart(x,y))map[y][x]='empty';else if(y%2===1&&x%2===1)map[y][x]='wall';else map[y][x]=Math.random()<blockChance?'block':'empty'}}enemies=[];const target=Math.min(8,2+level);let guard=0;while(enemies.length<target&&guard++<4000){let ex=(Math.random()*cols)|0,ey=(Math.random()*rows)|0;if(tileOpen(ex,ey)&&ex+ey>=6&&!enemies.some(e=>e.x===ex&&e.y===ey))enemies.push({x:ex,y:ey})}player.x=0;player.y=0;enemyMoveTimer=0;transitionFrames=0;status.textContent=`Fase ${level}: elimine ${enemies.length} inimigos.`}
function draw(){ctx.fillStyle='#161821';ctx.fillRect(0,0,canvas.width,canvas.height);for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){ctx.strokeStyle='rgba(255,255,255,.035)';ctx.strokeRect(x*tileSize+.5,y*tileSize+.5,tileSize-1,tileSize-1);if(map[y][x]==='wall'){ctx.fillStyle='#3e4355';ctx.fillRect(x*tileSize+2,y*tileSize+2,tileSize-4,tileSize-4);drawPixelArt(x,y,'#777f97',spriteWall)}else if(map[y][x]==='block'){ctx.fillStyle='#5e351f';ctx.fillRect(x*tileSize+3,y*tileSize+3,tileSize-6,tileSize-6);drawPixelArt(x,y,'#c47a3b',spriteBlock)}}for(const b of bombs){ctx.fillStyle='#171717';ctx.beginPath();ctx.arc((b.x+.5)*tileSize,(b.y+.5)*tileSize,10,0,Math.PI*2);ctx.fill();ctx.fillStyle=b.timer<22&&Math.floor(b.timer/4)%2?'#fff':'#ff5a54';ctx.fillRect((b.x+.5)*tileSize-2,b.y*tileSize+6,4,7)}for(const f of flames){ctx.fillStyle=f.timer%6<3?'#ffd166':'#ff6b35';ctx.fillRect(f.x*tileSize+5,f.y*tileSize+5,tileSize-10,tileSize-10)}for(const e of enemies)drawPixelArt(e.x,e.y,'#77ee79',spriteEnemy);if(!invulnerable||Math.floor(invulnerable/6)%2===0)drawPixelArt(player.x,player.y,'#5ee7ff',spritePlayer);if(gameOver){ctx.fillStyle='rgba(0,0,0,.62)';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#fff';ctx.textAlign='center';ctx.font='900 32px system-ui';ctx.fillText('FIM DE JOGO',canvas.width/2,canvas.height/2-8);ctx.font='700 16px system-ui';ctx.fillText('Espaço / BOMBA para reiniciar',canvas.width/2,canvas.height/2+24)}}
function updateHud(){hud.textContent=`Fase: ${level} | Vidas: ${'♥'.repeat(lives)}${'·'.repeat(MAX_LIVES-lives)} | Inimigos: ${enemies.length} | Pontos: ${score}`}
function restartGame(){score=0;lives=MAX_LIVES;level=1;framesSinceDamage=0;invulnerable=0;gameOver=false;bombs=[];flames=[];initMap();updateHud();sfx(520,.07)}window.PPGGameRestart=restartGame;
function hurtPlayer(reason){if(gameOver||invulnerable>0)return;lives--;framesSinceDamage=0;invulnerable=95;sfx(120,.16);if(lives<=0){gameOver=true;bombs=[];flames=[];status.textContent=`Fim de jogo — ${score} pontos. Use Novo Jogo, Enter ou BOMBA.`;updateHud();return}player.x=0;player.y=0;bombs=[];flames=[];status.textContent=`${reason} Você reapareceu com breve proteção.`;updateHud()}
function placeBomb(){if(gameOver){restartGame();return}if(transitionFrames||bombs.length>=MAX_BOMBS||bombAt(player.x,player.y))return;bombs.push({x:player.x,y:player.y,timer:80});sfx(240,.045)}
function flameCell(x,y){if(!map[y]||map[y][x]==='wall')return false;flames.push({x,y,timer:24});if(map[y][x]==='block'){map[y][x]='empty';score+=15;return false}const chained=bombs.find(b=>b.x===x&&b.y===y&&b.timer>2);if(chained)chained.timer=1;return true}
function explodeBomb(b){const before=enemies.length;flameCell(b.x,b.y);for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]])flameCell(b.x+dx,b.y+dy);const hot=new Set(flames.map(f=>f.x+','+f.y));enemies=enemies.filter(e=>!hot.has(e.x+','+e.y));const killed=before-enemies.length;if(killed){score+=killed*100;status.textContent=killed>1?`Combo explosivo: ${killed} inimigos!`:'Inimigo eliminado!'}if(hot.has(player.x+','+player.y))hurtPlayer('Sua própria explosão acertou você.');sfx(90,.13)}
function movePlayer(dx,dy){if(gameOver||transitionFrames||window.__PPG_PAUSED__)return;const nx=player.x+dx,ny=player.y+dy;if(dx||dy){if(canWalk(nx,ny)){player.x=nx;player.y=ny}else sfx(170,.02)}}
function updateEnemies(){enemyMoveTimer++;const interval=Math.max(28,58-(level-1)*3);if(enemyMoveTimer%interval!==0)return;const chase=Math.min(.55,.17+(level-1)*.05);for(const e of enemies){const opts=[[1,0],[-1,0],[0,1],[0,-1]].map(([dx,dy])=>({dx,dy,x:e.x+dx,y:e.y+dy})).filter(p=>canWalk(p.x,p.y)&&!enemies.some(o=>o!==e&&o.x===p.x&&o.y===p.y));if(opts.length){let pick;if(Math.random()<chase){opts.sort((a,b)=>(Math.abs(a.x-player.x)+Math.abs(a.y-player.y))-(Math.abs(b.x-player.x)+Math.abs(b.y-player.y)));pick=opts[0]}else pick=opts[(Math.random()*opts.length)|0];e.x=pick.x;e.y=pick.y}if(e.x===player.x&&e.y===player.y)hurtPlayer('Um inimigo encostou em você.')}}
function update(){if(gameOver){updateHud();return}framesSinceDamage++;if(invulnerable>0)invulnerable--;if(lives<MAX_LIVES&&framesSinceDamage>=2400){lives++;framesSinceDamage=0;status.textContent='♥ Vida recuperada por sobrevivência.';sfx(660,.08)}for(const b of bombs)b.timer--;const exploding=bombs.filter(b=>b.timer<=0);bombs=bombs.filter(b=>b.timer>0);for(const b of exploding)explodeBomb(b);for(const f of flames)f.timer--;flames=flames.filter(f=>f.timer>0);if(flames.some(f=>f.x===player.x&&f.y===player.y))hurtPlayer('Você entrou nas chamas.');if(!transitionFrames)updateEnemies();if(!enemies.length&&!transitionFrames){transitionFrames=70;score+=200*level;status.textContent=`Arena limpa! +${200*level} pontos. Próxima fase...`;sfx(760,.12)}if(transitionFrames>0&&--transitionFrames===0){level++;if(level%2===0&&lives<MAX_LIVES)lives++;bombs=[];flames=[];initMap()}updateHud()}
document.addEventListener('keydown',e=>{const k=e.key.toLowerCase();if(['arrowup','arrowdown','arrowleft','arrowright','w','a','s','d',' ','enter'].includes(k))e.preventDefault();if(k==='arrowup'||k==='w')movePlayer(0,-1);else if(k==='arrowdown'||k==='s')movePlayer(0,1);else if(k==='arrowleft'||k==='a')movePlayer(-1,0);else if(k==='arrowright'||k==='d')movePlayer(1,0);else if(k===' '||k==='enter')placeBomb()});
function bindButton(sel,fn){const el=document.querySelector(sel);if(!el)return;el.addEventListener('pointerdown',e=>{e.preventDefault();fn();el.setPointerCapture?.(e.pointerId)})}bindButton('[data-move=up]',()=>movePlayer(0,-1));bindButton('[data-move=down]',()=>movePlayer(0,1));bindButton('[data-move=left]',()=>movePlayer(-1,0));bindButton('[data-move=right]',()=>movePlayer(1,0));bindButton('#bomber-bomb',placeBomb);bindButton('#bomber-pause',()=>window.PPGQualityControls?.toggle());
function loop(){update();draw();requestAnimationFrame(loop)}restartGame();loop();
</script>'''

text = load("pixel_bomberman.html")
text = text.replace(
    '<p id="hud">Vidas: 3 | Pontos: 0</p>\n<script>',
    '<p id="hud">Fase: 1 | Vidas: ♥♥♥ | Inimigos: 3 | Pontos: 0</p>\n<p id="bomber-status" aria-live="polite">Destrua blocos, abra rotas e elimine os inimigos.</p>\n<div id="bomber-controls" aria-label="Controles móveis"><div class="bomber-dpad"><span></span><button data-move="up" aria-label="Cima">▲</button><span></span><button data-move="left" aria-label="Esquerda">◀</button><button data-move="down" aria-label="Baixo">▼</button><button data-move="right" aria-label="Direita">▶</button></div><div class="bomber-actions"><button id="bomber-bomb">💣 BOMBA</button><button id="bomber-pause">⏸ PAUSA</button></div></div>\n<script>',
    1,
)
if "bomber-controls" not in text:
    raise RuntimeError("pixel_bomberman.html: failed to insert mobile controls")
text = text.replace(
    '    canvas { background: #222; display: block; margin: auto; }',
    '    canvas { background: #222; display: block; width:min(92vw,480px); height:auto; margin:auto; image-rendering:pixelated; touch-action:none; border:1px solid #ffffff18; box-shadow:0 18px 55px #0008; }\n    #hud{margin:9px auto 4px;font-weight:800}#bomber-status{min-height:1.4em;margin:4px auto 9px;color:#b9c2d6;font-size:14px}#bomber-controls{display:flex;justify-content:center;align-items:center;gap:18px;margin:8px auto 12px;user-select:none;-webkit-user-select:none}.bomber-dpad{display:grid;grid-template-columns:repeat(3,48px);grid-template-rows:repeat(2,44px);gap:4px}.bomber-dpad button,.bomber-actions button{border:1px solid #ffffff28;border-radius:10px;background:#272c3d;color:#fff;font-weight:900;touch-action:manipulation}.bomber-dpad button:active,.bomber-actions button:active{transform:translateY(1px);filter:brightness(1.25)}.bomber-actions{display:grid;gap:7px}.bomber-actions button{min-width:105px;min-height:44px}#bomber-bomb{background:#8d3d39}#bomber-pause{background:#354e72}@media(pointer:fine) and (min-width:760px){#bomber-controls{opacity:.72}}@media(max-height:720px){h2{margin:5px}#bomber-controls{margin:4px auto;transform:scale(.9);transform-origin:top center}#bomber-status{display:none}}',
    1,
)
core_pattern = r'<script>\s*const canvas = document\.getElementById\("game"\);.*?</script>'
text, n = re.subn(core_pattern, BOMBER_CORE, text, count=1, flags=re.S)
if n != 1:
    raise RuntimeError(f"pixel_bomberman.html: core replacement expected 1 match, got {n}")
save("pixel_bomberman.html", text)
changes["pixel_bomberman.html"].extend([
    "complete gameplay core rebuild: safe spawn, fair bombs, collision invulnerability, level progression and meaningful scoring",
    "visible mobile D-pad + Bomb + Pause controls",
    "difficulty curve now scales enemies, pursuit and destructible density gradually",
])


# ---------------------------------------------------------------------------
# Targeted balance + correctness changes. Games already in a good place are left alone.
# ---------------------------------------------------------------------------
# Adivinhe: 0..1000 needs pressure, but 3 minutes was excessive; 90 s still allows deliberate binary-search play.
replace_all("advinhe_o_numero.html", '<p id="tempoRestante">180</p>', '<p id="tempoRestante">90</p>', "timer HUD 180s → 90s")
replace_all("advinhe_o_numero.html", 'let tempoRestante = 180;', 'let tempoRestante = 90;', "timer state 180s → 90s", minimum=2)
replace_all("advinhe_o_numero.html", '(tempo / 180)', '(tempo / 90)', "timer ring normalized to 90s")
replace_once("advinhe_o_numero.html", '<input type="number" id="palpite" placeholder="Seu palpite" />', '<input type="number" id="palpite" min="0" max="1000" step="1" placeholder="Seu palpite" />', "input constrained to the documented 0–1000 range")
replace_once("advinhe_o_numero.html", "      const historico = document.getElementById('historico');\n\n      if (tentativas === 0) {", "      const historico = document.getElementById('historico');\n      if (!Number.isInteger(palpite) || palpite < 0 || palpite > 1000) {\n        mensagem.textContent = '⚠️ Digite um número inteiro entre 0 e 1000.';\n        return;\n      }\n\n      if (tentativas === 0) {", "invalid guesses no longer consume attempts or start the timer")

# Bow: late targets/weather were spiking too sharply. Preserve 10-stage identity, trim the nastiest outliers.
replace_all("bow_and_arrow.html", "rocket:{name:'Foguete',points:145,r:24,hp:2,speed:71,material:'dense'}", "rocket:{name:'Foguete',points:145,r:24,hp:2,speed:66,material:'dense'}", "rocket speed 71 → 66")
replace_all("bow_and_arrow.html", "meteor:{name:'Meteoro',points:100,r:30,hp:2,speed:60,material:'dense'}", "meteor:{name:'Meteoro',points:100,r:30,hp:2,speed:57,material:'dense'}", "meteor speed 60 → 57")
replace_all("bow_and_arrow.html", "dragon:{name:'Dragão',points:350,r:44,hp:5,speed:44,material:'dense'}", "dragon:{name:'Dragão',points:350,r:44,hp:4,speed:44,material:'dense'}", "dragon HP 5 → 4")
replace_all("bow_and_arrow.html", "windBase:43,windSwing:52", "windBase:39,windSwing:46", "storm wind softened without removing weather challenge")

# Click Speed: the old shield felt like the mouse was being punished rather than the player being challenged.
replace_all("click_speed.html", "until=performance.now()+1350", "until=performance.now()+750", "post-click lockout 1350ms → 750ms")

# Foguetinho: make high multipliers dangerous without reaching unreadable rock spam.
replace_all("foguetinho.html", "spawn=Math.max(.24,.78-difficulty*.42)", "spawn=Math.max(.28,.82-difficulty*.40)", "obstacle spawn floor/pacing softened")

# Velha 4x4: random AI was far too weak; add tactical win/block plus imperfect strategic play.
VELHA_AI = r'''function lineCells() {
      const lines=[];
      for(let r=0;r<size;r++) lines.push(Array.from({length:size},(_,c)=>[r,c]));
      for(let c=0;c<size;c++) lines.push(Array.from({length:size},(_,r)=>[r,c]));
      lines.push(Array.from({length:size},(_,i)=>[i,i]));
      lines.push(Array.from({length:size},(_,i)=>[i,size-1-i]));
      return lines;
    }

    function immediateMove(mark) {
      for (const line of lineCells()) {
        const vals=line.map(([r,c])=>board[r][c]), empty=vals.findIndex(v=>v==='');
        if (empty>=0 && vals.filter(v=>v===mark).length===size-1) return line[empty];
      }
      return null;
    }

    function strategicScore(r,c) {
      let value = ((r===1||r===2)&&(c===1||c===2)) ? 4 : 1;
      for (const line of lineCells()) {
        if (!line.some(([rr,cc])=>rr===r&&cc===c)) continue;
        const vals=line.map(([rr,cc])=>board[rr][cc]), own=vals.filter(v=>v==='O').length, opp=vals.filter(v=>v==='X').length;
        if (!opp) value += [1,4,13,48][own] || 0;
        if (!own) value += [0,3,10,38][opp] || 0;
      }
      return value + Math.random()*2.5;
    }

    function aiMove() {
      if (gameOver) return;
      const empty=[];
      for(let r=0;r<size;r++)for(let c=0;c<size;c++)if(board[r][c]==='')empty.push([r,c]);
      if (!empty.length) return;
      let move=immediateMove('O') || immediateMove('X');
      if (!move) {
        const ranked=empty.map(([r,c])=>({r,c,s:strategicScore(r,c)})).sort((a,b)=>b.s-a.s);
        if (Math.random()<.80) {
          const roll=Math.random(),pick=roll<.68?0:roll<.90?1:2;
          const m=ranked[Math.min(pick,ranked.length-1)]; move=[m.r,m.c];
        } else move=empty[(Math.random()*empty.length)|0];
      }
      const [r,c]=move; board[r][c]='O'; drawBoard();
      if (checkWinner('O')) endGame('IA venceu!');
      else if (isFull()) endGame('Empate!');
    }

    function handleClick'''
regex_once("jogo_da_velha.html", r"function aiMove\(\) \{.*?\n    function handleClick", VELHA_AI, "4×4 AI upgraded from random to tactical-but-beatable")
replace_all("jogo_da_velha.html", "score += 10;", "score = Math.max(10, 100 - timer * 2);", "win score now rewards speed")
replace_once("jogo_da_velha.html", "      timer = 0;\n      timerDisplay.textContent = timer;", "      timer = 0;\n      score = 0;\n      timerDisplay.textContent = timer;\n      scoreDisplay.textContent = score;", "score resets cleanly each round")
regex_once("jogo_da_velha.html", r"function endGame\(message\) \{.*?\n    \}\n\n    function resetGame", "function endGame(message) {\n      gameOver = true;\n      clearInterval(timerInterval);\n      setTimeout(() => {\n        if (score > 0) {\n          const name = prompt(`${message}\\nDigite seu nome para salvar no ranking:`);\n          if (name) saveScore(name, score);\n        }\n        resetGame();\n      }, 900);\n    }\n\n    function resetGame", "losses/draws no longer pollute the leaderboard")
replace_all("jogo_da_velha.html", 'const scores = JSON.parse(localStorage.getItem("bbvelha_scores") || "[]");', 'const scores = JSON.parse(localStorage.getItem("velha_quantica_scores") || localStorage.getItem("bbvelha_scores") || "[]");', "record storage migrated away from legacy branded key", minimum=2)
replace_all("jogo_da_velha.html", 'localStorage.setItem("bbvelha_scores", JSON.stringify(scores.slice(0, 5)));', 'localStorage.setItem("velha_quantica_scores", JSON.stringify(scores.slice(0, 5)));', "new records use neutral storage key")

# Kombo Blocks: old .88 exponential curve reached twitch-only speeds too quickly.
replace_all("kombo_blocks.html", "function dropInterval(){let base=settings.difficulty==='easy'?1100:settings.difficulty==='hard'?650:900,min=settings.difficulty==='easy'?120:settings.difficulty==='hard'?30:50;return Math.max(min,Math.floor(base*Math.pow(.88,Math.max(0,stats.level-1))))}", "function dropInterval(){let base=settings.difficulty==='easy'?1120:settings.difficulty==='hard'?670:910,min=settings.difficulty==='easy'?160:settings.difficulty==='hard'?50:80;return Math.max(min,Math.floor(base*Math.pow(.90,Math.max(0,stats.level-1))))}", "drop curve softened: .88 → .90 with saner minimum intervals")

# Genius: easier onboarding, still accelerates into a genuine memory test; four mistakes rather than exactly three.
replace_all("memory_genius.html", "                }, 500); // Velocidade da sequência, ajuste conforme necessário (era 600)", "                }, Math.max(360, 620 - (level - 1) * 13)); // ritmo adaptativo: claro no início, mais rápido nos níveis altos", "sequence playback now adapts 620ms → 360ms")
replace_all("memory_genius.html", "life = Math.max(0, life - 34);", "life = Math.max(0, life - 30);", "mistake damage 34 → 30")
replace_all("memory_genius.html", "if(level % 5 === 0) life = Math.min(100, life + 12);", "if(level % 5 === 0) life = Math.min(100, life + 15);", "milestone recovery +12 → +15")
replace_all("memory_genius.html", "setTimeout(() => showSequence(0), 650);", "setTimeout(() => showSequence(0), 850);", "mistake recovery pause 650ms → 850ms")

# Pong: medium/master should read as smart, not clairvoyant.
replace_all("pong.html", "{name:'ESTRATEGISTA',reaction:.115,error:30,maxSpeed:445,accel:2050,lookAhead:1,adapt:.45}", "{name:'ESTRATEGISTA',reaction:.125,error:34,maxSpeed:430,accel:1900,lookAhead:1,adapt:.42}", "Strategist AI given slightly more human reaction/error")
replace_all("pong.html", "{name:'MESTRE',reaction:.072,error:15,maxSpeed:525,accel:2700,lookAhead:1,adapt:.75}", "{name:'MESTRE',reaction:.080,error:18,maxSpeed:505,accel:2450,lookAhead:1,adapt:.72}", "Master AI remains hard but less robotic")

# Sudoku: random deletion could create ambiguous puzzles, especially at 60 blanks. Keep only removals that preserve a unique solution.
SUDOKU_GENERATOR = r'''function sudokuSolutionCount(board, limit = 2) {
      let best = null, bestCandidates = null;
      for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) if (board[r][c] === '') {
        const used = new Set();
        for (let i = 0; i < 9; i++) { if (board[r][i] !== '') used.add(board[r][i]); if (board[i][c] !== '') used.add(board[i][c]); }
        const br=Math.floor(r/3)*3,bc=Math.floor(c/3)*3;for(let rr=br;rr<br+3;rr++)for(let cc=bc;cc<bc+3;cc++)if(board[rr][cc] !== '')used.add(board[rr][cc]);
        const candidates=[];for(let n=1;n<=9;n++)if(!used.has(n))candidates.push(n);
        if (!candidates.length) return 0;
        if (!bestCandidates || candidates.length < bestCandidates.length) { best=[r,c]; bestCandidates=candidates; if(candidates.length===1) break; }
      }
      if (!best) return 1;
      let total=0;const [r,c]=best;for(const n of bestCandidates){board[r][c]=n;total+=sudokuSolutionCount(board,limit-total);board[r][c]='';if(total>=limit)return total}return total;
    }

    function generateBoard(level) {
      const baseBoard = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
      ];
      for (let i = 0; i < 9; i += 3) { shuffle(baseBoard, i, i + 2); shuffle(baseBoard, i, i + 2, true); }
      const board=baseBoard.map(row=>row.slice()),target=level==='easy'?30:level==='medium'?40:50;
      const cells=Array.from({length:81},(_,i)=>i).sort(()=>Math.random()-.5);let removed=0,attempts=0;
      for (const pos of cells) {
        if (removed>=target || attempts++>81) break;
        const r=Math.floor(pos/9),c=pos%9,keep=board[r][c];board[r][c]='';
        const probe=board.map(row=>row.slice());if(sudokuSolutionCount(probe,2)===1)removed++;else board[r][c]=keep;
      }
      return board;
    }

    function shuffle'''
regex_once("sudoku.html", r"function generateBoard\(level\) \{.*?\n    function shuffle", SUDOKU_GENERATOR, "Sudoku generator now preserves a unique solution; difficulty targets 30/40/50 blanks")

# These systems already contain tuned difficulty directors or mathematically natural difficulty. Don't perturb them merely to make a diff.
notes["campo_minado.html"].append("classic minefield rules and current pacing retained; no gratuitous probability change")
notes["corrida_de_cavalos.html"].append("horse variance/odds already bounded; economy retained to avoid converting fair randomness into hidden house bias")
notes["dropworks.html"].append("40-stage moving-container/supply system was recently tuned; native pause/restart retained")
notes["idle_trader.html"].append("long-form economy/prestige curve retained; arbitrary rebalance would invalidate existing saves")
notes["jogo_da_forca.html"].append("gameplay pacing retained; repository still contains the stale pre-i18n banking dictionary and needs promotion of the already-approved 320-concept File Library version")
notes["leaping_into_life.html"].append("Pond/Marsh/Storm gap-speed matrix is progressive and readable; retained")
notes["salve_os_gatinhos.html"].append("existing difficulty director already spaces spawns, adds wind gradually and includes life recovery; retained")
notes["the_worm.html"].append("Calm/Groove/Frenzy speed, wrap and poison matrix is already well separated; retained")
notes["torre_de_hanoi.html"].append("difficulty is naturally determined by 3–8 discs; no artificial timing pressure added")
notes["tron.html"].append("speed progression, life regeneration and AI randomness already form a controlled curve; retained")

# Add the standard pause layer after gameplay patches so it remains independent and easy to audit.
for game in GAMES:
    if game not in PAUSE_NATIVE:
        inject_pause(game)

# ---------------------------------------------------------------------------
# Validation: every game remains a single standalone HTML and key pass invariants hold.
# ---------------------------------------------------------------------------
for game in GAMES:
    text=load(game)
    if not re.search(r"<!doctype html",text,re.I) or "</html>" not in text.lower():
        raise RuntimeError(f"{game}: malformed HTML envelope")
    if game not in PAUSE_NATIVE and text.count("ppg-quality-controls-runtime") != 1:
        raise RuntimeError(f"{game}: pause layer not injected exactly once")

bomber=load("pixel_bomberman.html")
for token in ["bomber-controls", "PPGGameRestart", "MAX_BOMBS=2", "safeStart", "transitionFrames"]:
    if token not in bomber: raise RuntimeError(f"pixel_bomberman.html: missing {token}")
if "cellsToRemove = 60" in load("sudoku.html"):
    raise RuntimeError("sudoku.html: legacy ambiguous 60-blank generator survived")
if "until=performance.now()+1350" in load("click_speed.html"):
    raise RuntimeError("click_speed.html: legacy 1350ms cooldown survived")

# Generate a concise, human-readable one-by-one record of this pass.
DISPLAY = {
 "advinhe_o_numero.html":"Adivinhe o Número", "bow_and_arrow.html":"Arqueiro do Vale", "campo_minado.html":"Toxic Stench",
 "click_speed.html":"Click Speed", "corrida_de_cavalos.html":"Hipódromo Estelar", "dropworks.html":"DROPWORKS",
 "foguetinho.html":"Cosmo Crash", "idle_trader.html":"Império Financeiro 8-bit", "jogo_da_forca.html":"Forca Neon",
 "jogo_da_velha.html":"Velha Quântica", "kombo_blocks.html":"Kombo Blocks", "leaping_into_life.html":"Leaping Into Life",
 "memory_genius.html":"Pulso Genius", "pixel_bomberman.html":"Pixel Bomber", "pong.html":"Neon Pong",
 "salve_os_gatinhos.html":"Salve os Gatinhos!", "sudoku.html":"Zen Sudoku", "the_worm.html":"The Worm",
 "torre_de_hanoi.html":"Torre de Hanói", "tron.html":"Tron: Domínio",
}
lines=["# Primata Web Quickplay — quality & balance pass", "", "Automated repository pass applied in-place while preserving one self-contained HTML per game.", ""]
for i,g in enumerate(GAMES,1):
    lines += [f"## {i}. {DISPLAY[g]} — `{g}`"]
    if changes[g]: lines += [f"- ✅ {x}" for x in changes[g]]
    else: lines.append("- ✅ Reviewed; no source change needed.")
    lines += [f"- ℹ️ {x}" for x in notes[g]]
    lines.append("")
lines += ["## Global checks", "", f"- Games audited: **{len(GAMES)}**", f"- Standard pause added where missing: **{len(GAMES)-len(PAUSE_NATIVE)}**", "- Native pause preserved without duplication: **DROPWORKS, Kombo Blocks, Neon Pong**", "- Pixel Bomber now has keyboard + visible touch controls, staged difficulty and a complete restart flow.", "- All changes stay inside each game's own HTML; no external runtime dependency was introduced.", "- Known integration debt: **Forca Neon on GitHub is not the approved 320-concept everyday-language build already present in File Library.** This pass flags it rather than pretending the stale banking dictionary is correct."]
(ROOT/"QUALITY_PASS_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"QUALITY_PASS_OK games={len(GAMES)} pause_added={len(GAMES)-len(PAUSE_NATIVE)}")
