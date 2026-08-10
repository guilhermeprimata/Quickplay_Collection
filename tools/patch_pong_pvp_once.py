from pathlib import Path
import re

p=Path('pong.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label):
    global s
    if old not in s:
        raise SystemExit(f'{label}: target not found')
    s=s.replace(old,new,1)

def sub(pattern,repl,label,flags=0):
    global s
    s2,n=re.subn(pattern,repl,s,count=1,flags=flags)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 replacement, got {n}')
    s=s2

rep('<header><div class="brand">NEON PONG // PIXEL ARENA</div><div class="hint">↑ ↓ ou W S • mouse/toque • P pausa • M som</div></header>',
    '<header><div class="brand">NEON PONG // PIXEL ARENA</div><div class="hint" id="controlHint">1P: W/S, ↑↓ ou mouse • 2P: P1 W/S • P2 ↑↓ • P pausa • M som</div></header>',
    'header hint')
rep('<div class="controls"><button id="pauseBtn" class="secondary">PAUSAR</button><button id="restartBtn">REINICIAR</button><button id="soundBtn" class="secondary">SOM: LIGADO</button><button id="difficultyBtn">IA: ESTRATEGISTA</button></div>',
    '<div class="controls"><button id="pauseBtn" class="secondary">PAUSAR</button><button id="restartBtn">REINICIAR</button><button id="soundBtn" class="secondary">SOM: LIGADO</button><button id="modeBtn" class="secondary">MODO: 1P vs IA</button><button id="difficultyBtn">IA: ESTRATEGISTA</button></div>',
    'mode button')
rep("let arcadeScore=0,centerCombo=0,comboPeak=0,powerup=null,powerupTimer=6.5,slowmoTimer=0,tripleTimer=0,labelSerial=0,pointerTarget=null;",
    "let arcadeScore=0,centerCombo=0,comboPeak=0,p2ArcadeScore=0,p2CenterCombo=0,p2ComboPeak=0,powerup=null,powerupTimer=6.5,slowmoTimer=0,tripleTimer=0,labelSerial=0,pointerTarget=null,gameMode='ai';",
    'mode state')

# Reset PvP score/combo state too.
rep("elapsed=0;arcadeScore=0;centerCombo=0;comboPeak=0;pointerTarget=null;",
    "elapsed=0;arcadeScore=0;centerCombo=0;comboPeak=0;p2ArcadeScore=0;p2CenterCombo=0;p2ComboPeak=0;pointerTarget=null;",
    'reset p2 state')

# Game-over wording and summary adapt to PvP.
rep("oTitle.textContent=win?'VOCÊ VENCEU!':'CPU VENCEU';oText.innerHTML=`Placar ${player.score} × ${ai.score}<br>Tempo: ${elapsed.toFixed(1)}s<br>Arcade: ${arcadeScore.toLocaleString('pt-BR')} • Melhor combo: ${comboPeak}x`;",
    "oTitle.textContent=win?(gameMode==='pvp'?'PLAYER 1 VENCEU!':'VOCÊ VENCEU!'):(gameMode==='pvp'?'PLAYER 2 VENCEU!':'CPU VENCEU');oText.innerHTML=gameMode==='pvp'?`Placar ${player.score} × ${ai.score}<br>Tempo: ${elapsed.toFixed(1)}s<br>P1 Arcade: ${arcadeScore.toLocaleString('pt-BR')} • Combo ${comboPeak}x<br>P2 Arcade: ${p2ArcadeScore.toLocaleString('pt-BR')} • Combo ${p2ComboPeak}x`:`Placar ${player.score} × ${ai.score}<br>Tempo: ${elapsed.toFixed(1)}s<br>Arcade: ${arcadeScore.toLocaleString('pt-BR')} • Melhor combo: ${comboPeak}x`;",
    'end wording')

# Add mirrored combo logic for Player 2.
anchor="function hitBoost(side){return effects[side].smash>0?1.30:1}"
insert="""function p2ComboMultiplier(n=p2CenterCombo){return Math.min(5,1+Math.floor(Math.max(0,n-1)/2)*.5)}
function cashP2Combo(reason='BREAK'){if(p2CenterCombo>=2){const mult=p2ComboMultiplier(p2CenterCombo),bonus=Math.round(p2CenterCombo*mult*35);p2ArcadeScore+=bonus;label(`${reason} • P2 COMBO ${p2CenterCombo}x = +${bonus}`,W/2,H*.39,'#ffd34d',22,1.25);burst(W/2,H*.41,'#ffd34d',16,150)}p2CenterCombo=0}
function registerP2Zone(zone,x,y){if(zone===1){p2CenterCombo++;p2ComboPeak=Math.max(p2ComboPeak,p2CenterCombo);const mult=p2ComboMultiplier(),pts=Math.round(50*mult);p2ArcadeScore+=pts;const col=p2CenterCombo>=7?'#ff4d8d':p2CenterCombo>=4?'#ffd84d':'#8cff72';label(`P2 CENTER ${p2CenterCombo}x • ×${mult.toFixed(mult%1?1:0)} • +${pts}`,x-90,y,col,17+Math.min(8,p2CenterCombo),.9);if(p2CenterCombo===3||p2CenterCombo===6||p2CenterCombo===9){shake=Math.max(shake,10);flash=.07;burst(x,y,col,20)}}else{cashP2Combo('CASHOUT');p2ArcadeScore+=20;label('P2 EDGE +20',x-65,y,'#d8c3ff',15,.65)}}
"""+anchor
rep(anchor,insert,'p2 combo funcs')

# Collision: P2 gets its own center combo, AI memory/fatigue only in AI mode.
old="if(side==='player'){registerPlayerZone(zone,b.x,b.y);rememberPlayerShot()}ai.rallyHits++;return true"
new="if(side==='player'){registerPlayerZone(zone,b.x,b.y);if(gameMode==='ai')rememberPlayerShot()}else if(gameMode==='pvp'){registerP2Zone(zone,b.x,b.y)}if(gameMode==='ai')ai.rallyHits++;return true"
rep(old,new,'collision pvp combo')

# Difficulty button becomes inert in PvP; add mode switch UI.
sub(r"function cycleDifficulty\(\)\{difficultyIndex=\(difficultyIndex\+1\)%difficulties\.length;.*?\}\nconst POWERUPS=", """function refreshModeUI(){const pvp=gameMode==='pvp',modeBtn=document.querySelector('#modeBtn'),diffBtn=document.querySelector('#difficultyBtn'),hint=document.querySelector('#controlHint');modeBtn.textContent=pvp?'MODO: 2P LOCAL':'MODO: 1P vs IA';diffBtn.disabled=pvp;diffBtn.style.opacity=pvp?'.45':'1';diffBtn.textContent=pvp?'IA: —':`IA: ${difficulties[difficultyIndex].name}`;hint.textContent=pvp?'2P LOCAL • P1: W/S • P2: ↑/↓ • P pausa • M som':'1P vs IA • W/S, ↑/↓ ou mouse/toque • P pausa • M som'}
function cycleMode(){gameMode=gameMode==='ai'?'pvp':'ai';ai.fatigue=0;ai.fatigueNotice=0;ai.mode=gameMode==='pvp'?'human':'recover';pointerTarget=null;refreshModeUI();tone(gameMode==='pvp'?760:560,.08,'square',.045);if(state==='playing'||state==='paused')reset()}
function cycleDifficulty(){if(gameMode==='pvp')return;difficultyIndex=(difficultyIndex+1)%difficulties.length;document.querySelector('#difficultyBtn').textContent=`IA: ${difficulties[difficultyIndex].name}`;tone(520+difficultyIndex*90,.07);if(state==='playing'){ai.fatigue=Math.min(ai.fatigue,difficulties[difficultyIndex].fatigueCap);serve(ball.vx<0?-1:1)}}
const POWERUPS=""", 'mode functions', re.S)

# Human controller shared by both paddles. In 1P, mouse remains available to left paddle.
pattern=r"function update\(dt\)\{updateLabelsAndParticles\(dt\);if\(state!=='playing'\)return;elapsed\+=dt;music\(dt\);updatePowerups\(dt\);\s*const input=.*?\n updateAI\(dt\);"
replacement="""function updateHumanPaddle(p,input,dt,side,allowPointer=false){const jam=effects[side].jam>0?.84:1,over=effects[side].overdrive>0?1.22:1,keyMax=900*jam*over,keyAccel=6800*jam*over;if(input){if(side==='player')pointerTarget=null;const desired=input*keyMax,delta=clamp(desired-p.vy,-keyAccel*dt,keyAccel*dt);p.vy+=delta;p.y=clamp(p.y+p.vy*dt,0,H-p.h)}else if(side==='player'&&allowPointer&&pointerTarget!=null){const center=p.y+p.h/2,diff=pointerTarget-center,followRate=30*jam*over,follow=1-Math.exp(-followRate*dt),oldY=p.y,nextY=clamp(p.y+diff*follow,0,H-p.h);p.y=nextY;p.vy=dt>0?clamp((nextY-oldY)/dt,-1450*jam*over,1450*jam*over):0;if(Math.abs(diff)<.7){p.y=clamp(pointerTarget-p.h/2,0,H-p.h);p.vy=0}}else{p.vy*=Math.exp(-11*dt);if(Math.abs(p.vy)<2)p.vy=0;p.y=clamp(p.y+p.vy*dt,0,H-p.h)}}
function update(dt){updateLabelsAndParticles(dt);if(state!=='playing')return;elapsed+=dt;music(dt);updatePowerups(dt);
 const leftInput=(keys.has('w')?-1:0)+(keys.has('s')?1:0)+(gameMode==='ai'?((keys.has('arrowup')?-1:0)+(keys.has('arrowdown')?1:0)):0);
 updateHumanPaddle(player,leftInput,dt,'player',gameMode==='ai');
 if(gameMode==='pvp'){const rightInput=(keys.has('arrowup')?-1:0)+(keys.has('arrowdown')?1:0);updateHumanPaddle(ai,rightInput,dt,'ai',false);ai.fatigue=0;ai.fatigueNotice=0;ai.mode='human'}else updateAI(dt);"""
sub(pattern,replacement,'shared human controller',re.S)

# Mouse is deliberately 1P-only for competitive fairness.
rep("function setPointer(e){if(state!=='playing')return;", "function setPointer(e){if(state!=='playing'||gameMode==='pvp')return;", 'pointer pvp guard')

# HUD status line adapts; show P2 combo/arcade on right in PvP.
old="const fat=Math.round(ai.fatigue*100);pixelText(`IA ${difficulties[difficultyIndex].name} • FADIGA ${fat}% • ${ai.mode==='intercept'?'PREVENDO':'REPOSICIONANDO'}`,480,70,11,'center',fat>25?'#ff6978':fat>15?'#ffc15f':'#72f1b8');if(centerCombo>0)pixelText(`CENTER COMBO ${centerCombo}x • ×${comboMultiplier().toFixed(comboMultiplier()%1?1:0)}`,W*.23,92,14,'left','#ff76dc');"
new="const fat=Math.round(ai.fatigue*100);if(gameMode==='pvp')pixelText(`2P LOCAL • P1 W/S • P2 ↑↓`,480,70,11,'center','#8cffd0');else pixelText(`IA ${difficulties[difficultyIndex].name} • FADIGA ${fat}% • ${ai.mode==='intercept'?'PREVENDO':'REPOSICIONANDO'}`,480,70,11,'center',fat>25?'#ff6978':fat>15?'#ffc15f':'#72f1b8');if(centerCombo>0)pixelText(`CENTER COMBO ${centerCombo}x • ×${comboMultiplier().toFixed(comboMultiplier()%1?1:0)}`,W*.23,92,14,'left','#ff76dc');if(gameMode==='pvp'&&p2CenterCombo>0)pixelText(`P2 CENTER ${p2CenterCombo}x • ×${p2ComboMultiplier().toFixed(p2ComboMultiplier()%1?1:0)}`,W*.77,92,14,'right','#ffd34d');"
rep(old,new,'hud mode')

# Power-up owner labels: human-readable P2 instead of CPU in PvP.
s=s.replace("owner==='player'?'VOCÊ':'CPU'", "owner==='player'?'P1':(gameMode==='pvp'?'P2':'CPU')")

# Wire mode button and initialize UI.
old="document.querySelector('#startBtn').onclick=reset;document.querySelector('#restartBtn').onclick=reset;document.querySelector('#pauseBtn').onclick=togglePause;document.querySelector('#soundBtn').onclick=toggleSound;document.querySelector('#difficultyBtn').onclick=cycleDifficulty;document.querySelector('#soundBtn').textContent=`SOM: ${soundEnabled?'LIGADO':'DESLIGADO'}`;serve();requestAnimationFrame(loop);"
new="document.querySelector('#startBtn').onclick=reset;document.querySelector('#restartBtn').onclick=reset;document.querySelector('#pauseBtn').onclick=togglePause;document.querySelector('#soundBtn').onclick=toggleSound;document.querySelector('#modeBtn').onclick=cycleMode;document.querySelector('#difficultyBtn').onclick=cycleDifficulty;document.querySelector('#soundBtn').textContent=`SOM: ${soundEnabled?'LIGADO':'DESLIGADO'}`;refreshModeUI();serve();requestAnimationFrame(loop);"
rep(old,new,'wire mode')

# About/help text mentions both control schemes.
s=s.replace('Mova a raquete com W/S, setas, mouse ou toque. O primeiro a 10 pontos vence.', 'No modo 1P, mova a raquete com W/S, setas, mouse ou toque. No modo 2P local, Player 1 usa W/S e Player 2 usa ↑/↓. O primeiro a 10 pontos vence.')

p.write_text(s,encoding='utf-8')
print('PONG_PVP_PATCH_OK')
