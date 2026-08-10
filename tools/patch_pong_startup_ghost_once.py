from pathlib import Path

p=Path('pong.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label):
    global s
    if old not in s:
        raise SystemExit(f'{label}: target not found')
    s=s.replace(old,new,1)

rep("#overlay{position:absolute;inset:0;display:grid;place-items:center;background:#02091ad9;backdrop-filter:blur(4px);padding:18px;text-align:center;z-index:10}",
    "#overlay{position:absolute;inset:0;display:grid;place-items:center;background:#02091a88;backdrop-filter:blur(1.5px);padding:18px;text-align:center;z-index:10}",
    'overlay attract visibility')

rep("const particles=[],msgs=[],history=[],replay={active:false,frames:[],i:0,t:0,after:null};",
    "const particles=[],msgs=[],history=[],replay={active:false,frames:[],i:0,t:0,after:null};\nconst attract={left:{x:70,y:H/2-55,w:14,h:110,vy:0},right:{x:W-84,y:H/2-55,w:14,h:110,vy:0},ball:{x:W/2,y:H/2,vx:390,vy:185,r:8},spark:0};",
    'attract state')

old_audio="function audioInit(){if(ac)return;ac=new (window.AudioContext||window.webkitAudioContext)();master=ac.createGain();musicBus=ac.createGain();sfxBus=ac.createGain();master.gain.value=.85;musicBus.gain.value=.23;sfxBus.gain.value=.42;musicBus.connect(master);sfxBus.connect(master);master.connect(ac.destination);noise=ac.createBuffer(1,ac.sampleRate*.15,ac.sampleRate);const d=noise.getChannelData(0);for(let i=0;i<d.length;i++)d[i]=(Math.random()*2-1)*(1-i/d.length)}"
new_audio="function audioInit(){if(ac)return true;try{const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return false;ac=new AC();master=ac.createGain();musicBus=ac.createGain();sfxBus=ac.createGain();master.gain.value=.85;musicBus.gain.value=.23;sfxBus.gain.value=.42;musicBus.connect(master);sfxBus.connect(master);master.connect(ac.destination);noise=ac.createBuffer(1,ac.sampleRate*.15,ac.sampleRate);const d=noise.getChannelData(0);for(let i=0;i<d.length;i++)d[i]=(Math.random()*2-1)*(1-i/d.length);return true}catch(err){console.warn('Neon Pong audio unavailable:',err);ac=master=musicBus=sfxBus=noise=null;return false}}"
rep(old_audio,new_audio,'safe audio init')

rep("function osc(f,d=.07,type='square',v=.12,when=0,bus=sfxBus){if(!soundOn)return;audioInit();const t=ac.currentTime+when,o=ac.createOscillator(),g=ac.createGain();",
    "function osc(f,d=.07,type='square',v=.12,when=0,bus=sfxBus){if(!soundOn||!audioInit())return;const t=ac.currentTime+when,o=ac.createOscillator(),g=ac.createGain();",
    'safe osc')
rep("function noiseHit(v=.05,when=0){if(!soundOn)return;audioInit();const t=ac.currentTime+when,s=ac.createBufferSource(),hp=ac.createBiquadFilter(),g=ac.createGain();",
    "function noiseHit(v=.05,when=0){if(!soundOn||!audioInit())return;const t=ac.currentTime+when,s=ac.createBufferSource(),hp=ac.createBiquadFilter(),g=ac.createGain();",
    'safe noise')
rep("function kick(){if(!soundOn)return;audioInit();const t=ac.currentTime,o=ac.createOscillator(),g=ac.createGain();",
    "function kick(){if(!soundOn||!audioInit())return;const t=ac.currentTime,o=ac.createOscillator(),g=ac.createGain();",
    'safe kick')
rep("function acid(f,accent=false){if(!soundOn)return;audioInit();const t=ac.currentTime,o=ac.createOscillator(),fil=ac.createBiquadFilter(),g=ac.createGain();",
    "function acid(f,accent=false){if(!soundOn||!audioInit())return;const t=ac.currentTime,o=ac.createOscillator(),fil=ac.createBiquadFilter(),g=ac.createGain();",
    'safe acid')
rep("function music(dt){if(!soundOn||state!=='playing')return;audioInit();morphClock-=dt;",
    "function music(dt){if(!soundOn||state!=='playing'||!audioInit())return;morphClock-=dt;",
    'safe music')

old_start="function startMatch(){p1.setWins=p2.setWins=0;p1.score=p2.score=0;p1.y=p2.y=H/2-BASE_H/2;p1.vy=p2.vy=0;p1.fatigue=p2.fatigue=0;p2.notice=0;elapsed=0;powerup=null;powerTimer=rnd(5,8);modifier=null;modifierTimer=rnd(12,18);resetEffects();resetStats();sudden=false;state='playing';document.querySelector('#overlay').classList.add('hidden');audioInit();ac?.resume();last=performance.now();musicStep=(Math.random()*512)|0;serve()}"
new_start="function startMatch(){p1.setWins=p2.setWins=0;p1.score=p2.score=0;p1.y=p2.y=H/2-BASE_H/2;p1.vy=p2.vy=0;p1.fatigue=p2.fatigue=0;p2.notice=0;elapsed=0;powerup=null;powerTimer=rnd(5,8);modifier=null;modifierTimer=rnd(12,18);resetEffects();resetStats();sudden=false;state='playing';document.querySelector('#overlay').classList.add('hidden');last=performance.now();musicStep=(Math.random()*512)|0;serve();try{if(soundOn&&audioInit())ac?.resume?.().catch?.(()=>{})}catch(err){console.warn('Audio resume ignored:',err)}}"
rep(old_start,new_start,'start independent from audio')

anchor="function snapshot(){history.push({b:balls.map(q=>({x:q.x,y:q.y,r:q.r,primary:q.primary})),p1:{y:p1.y,h:p1.h},p2:{y:p2.y,h:p2.h}});if(history.length>100)history.shift()}"
attract_code=anchor+"\nfunction resetAttract(){attract.left.y=H/2-attract.left.h/2;attract.right.y=H/2-attract.right.h/2;attract.left.vy=attract.right.vy=0;attract.ball.x=W/2;attract.ball.y=H/2;attract.ball.vx=(Math.random()<.5?-1:1)*rnd(330,430);attract.ball.vy=rnd(-230,230)}\nfunction updateAttract(dt){const a=attract,b=a.ball;for(const pad of[a.left,a.right]){const target=b.y-pad.h/2+Math.sin((elapsed+pad.x)*.01)*18,diff=target-pad.y,push=clamp(diff*5.5,-520,520);pad.vy+=(push-pad.vy)*Math.min(1,dt*7);pad.y=clamp(pad.y+pad.vy*dt,88,H-pad.h-18)}b.x+=b.vx*dt;b.y+=b.vy*dt;if(b.y-b.r<88&&b.vy<0){b.y=88+b.r;b.vy*=-1}if(b.y+b.r>H-18&&b.vy>0){b.y=H-18-b.r;b.vy*=-1}const hit=(pad,dir)=>{if(Math.sign(b.vx)!==dir)return false;if(b.x+b.r<pad.x||b.x-b.r>pad.x+pad.w||b.y+b.r<pad.y||b.y-b.r>pad.y+pad.h)return false;const rel=clamp((b.y-(pad.y+pad.h/2))/(pad.h/2),-1,1),sp=Math.min(620,Math.hypot(b.vx,b.vy)*1.018+2);b.vx=Math.cos(rel*.9)*sp*-dir;b.vy=Math.sin(rel*.9)*sp+pad.vy*.11;b.x=dir<0?pad.x+pad.w+b.r:pad.x-b.r;return true};hit(a.left,-1)||hit(a.right,1);if(b.x<-40||b.x>W+40)resetAttract();a.spark-=dt;if(a.spark<=0){a.spark=rnd(.65,1.3);if(Math.random()<.45)burst(b.x,b.y,Math.random()<.5?'#52e7ff':'#ff67dc',4,70)}}\nfunction drawAttract(){const a=attract;X.save();X.globalAlpha=.30+.07*Math.sin(performance.now()*.002);for(const [pad,col] of[[a.left,'#52e7ff'],[a.right,'#ff67dc']]){X.shadowBlur=20;X.shadowColor=col;X.fillStyle=col;X.fillRect(pad.x,pad.y,pad.w,pad.h);X.fillStyle='#ffffffaa';X.fillRect(pad.x,pad.y+pad.h*.4,pad.w,pad.h*.2)}X.shadowBlur=24;X.shadowColor='#fff';X.fillStyle='#ffffff';X.fillRect(a.ball.x-a.ball.r,a.ball.y-a.ball.r,a.ball.r*2,a.ball.r*2);X.shadowBlur=0;pixel('GHOST PLAYERS',W/2,H-34,13,'center','#bfeaff',.62);X.restore()}"
rep(anchor,attract_code,'attract functions')

rep("if(state==='replay'){updateReplay(dt);return}if(state!=='playing')return;",
    "if(state==='replay'){updateReplay(dt);return}if(state==='menu'||state==='gameover'){updateAttract(dt);return}if(state!=='playing')return;",
    'attract update idle')

rep("drawModifier();if(replay.active)drawReplay();else{drawPaddle(p1);drawPaddle(p2);drawPower();for(const b of balls)drawBall(b)}",
    "drawModifier();if(state==='menu'||state==='gameover')drawAttract();else if(replay.active)drawReplay();else{drawPaddle(p1);drawPaddle(p2);drawPower();for(const b of balls)drawBall(b)}",
    'draw attract idle')

old_set="function setSound(v){soundOn=!!v;prefs.sound=soundOn;try{localStorage.setItem('ppg_platform_prefs_v1',JSON.stringify(prefs))}catch{}document.querySelector('#soundBtn').textContent=`SOM: ${soundOn?'LIGADO':'DESLIGADO'}`;document.querySelector('#soundTop').textContent=soundOn?'🔊 Som':'🔇 Som';if(soundOn){audioInit();ac?.resume();osc(440,.06)}}"
new_set="function setSound(v,unlock=true){soundOn=!!v;prefs.sound=soundOn;try{localStorage.setItem('ppg_platform_prefs_v1',JSON.stringify(prefs))}catch{}document.querySelector('#soundBtn').textContent=`SOM: ${soundOn?'LIGADO':'DESLIGADO'}`;document.querySelector('#soundTop').textContent=soundOn?'🔊 Som':'🔇 Som';if(soundOn&&unlock){try{if(audioInit()){ac?.resume?.().catch?.(()=>{});osc(440,.06)}}catch(err){console.warn('Sound unlock ignored:',err)}}}"
rep(old_set,new_set,'safe setSound')

rep("document.querySelector('#themeTop').textContent=document.body.classList.contains('light')?'🌙 Escuro':'☀️ Claro';setSound(soundOn);refreshUI();serve();requestAnimationFrame(loop);",
    "document.querySelector('#themeTop').textContent=document.body.classList.contains('light')?'🌙 Escuro':'☀️ Claro';setSound(soundOn,false);refreshUI();serve();resetAttract();requestAnimationFrame(loop);",
    'bootstrap no audio unlock')

# Add a visible runtime safety net so catastrophic JS errors do not leave a dead-looking screen.
rep("'use strict';\nconst C=document.querySelector('#game')",
    "'use strict';\nwindow.addEventListener('error',e=>{console.error('Neon Pong runtime error:',e.error||e.message);const ov=document.querySelector('#overlay');if(ov&&document.querySelector('#overlayTitle')){document.querySelector('#overlayTitle').textContent='ERRO DE EXECUÇÃO';document.querySelector('#overlayText').textContent='O jogo encontrou um erro inesperado. Recarregue a página; o problema foi registrado no console.';ov.classList.remove('hidden')}});\nconst C=document.querySelector('#game')",
    'runtime safety net')

p.write_text(s,encoding='utf-8')
print('PONG_STARTUP_GHOST_PATCH_OK')
