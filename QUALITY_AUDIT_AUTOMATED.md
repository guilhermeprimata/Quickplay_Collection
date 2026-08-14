# Quickplay Collection — automated quality audit

Generated from the repository contents. Heuristics are intentionally conservative; false positives are preferable to silently missing a control path.

| Game | Platform | Native pause | Native restart | Native touch | Touch gap? | Audio | Storage | i18n signal | Bytes |
|---|---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|
| `advinhe_o_numero.html` | v1 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 25496 |
| `alien_threat.html` | none | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 348000 |
| `bow_and_arrow.html` | v2 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 55300 |
| `campo_minado.html` | v1 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 69630 |
| `click_speed.html` | v2 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 35680 |
| `corrida_de_cavalos.html` | v1 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 48077 |
| `dropworks.html` | none | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 144991 |
| `foguetinho.html` | v2 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 39582 |
| `idle_trader.html` | v1 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 63644 |
| `jogo_da_forca.html` | v2 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 61874 |
| `jogo_da_velha.html` | v1 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 28964 |
| `kombo_blocks.html` | none | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 118942 |
| `leaping_into_life.html` | v2 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 33490 |
| `memory_genius.html` | v2 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 55024 |
| `pixel_bomberman.html` | v2 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 35170 |
| `pong.html` | none | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 51921 |
| `salve_os_gatinhos.html` | v2 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 37842 |
| `snowball_avalanche.html` | none | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 207925 |
| `sudoku.html` | v1 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 31323 |
| `the_worm.html` | v2 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 34279 |
| `torre_de_hanoi.html` | v1 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 42925 |
| `tron.html` | v2 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 46674 |

## Automated findings

- Platform layer not v2: `advinhe_o_numero.html`, `alien_threat.html`, `campo_minado.html`, `corrida_de_cavalos.html`, `dropworks.html`, `idle_trader.html`, `jogo_da_velha.html`, `kombo_blocks.html`, `pong.html`, `snowball_avalanche.html`, `sudoku.html`, `torre_de_hanoi.html`
- No native pause signal: none
- No native restart/new-game signal: none
- Canvas + keyboard but no native touch signal: none

## Per-game controls and balance candidates

### `advinhe_o_numero.html`
**Control flow signals**
- `L49: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
- `L142: function resetarJogo() {`
- `L156: document.getElementById('palpite').addEventListener('keydown', function(event) {`
**Gameplay tuning signals**
- `L20: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L30: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L75: let tentativas = 0;`
- `L76: let tempoRestante = 90;`
- `L84: if (tempoRestante <= 0) {`
- `L96: const anguloFinal = (tempo / 90) * 2 * Math.PI;`
- `L120: if (tentativas === 0) {`
- `L144: tentativas = 0;`
- `L145: tempoRestante = 90;`

### `alien_threat.html`
**Control flow signals**
- `L274: function resumeAudio(){let ctx=ensureAudio();if(!ctx)return Promise.resolve(null);if(ctx.state==='running')return Promise.resolve(ctx);if(audioResumePromise)return audioResumePromise;audioResumePromise=ctx.resume().catch(()=>null).then(()=>{audioResumePromise=null;return ctx.state==='running'?ctx:null});return audioResumePromise}`
- `L276: function startCue(){if(!cfg.sound)return;duckMusic(.48,.7);alienPulseSfx(.8);tone(63,.42,'sine',.055,'sfx');tone(91,.28,'sawtooth',.022,'sfx',.12)}`
- `L300: function beginRunAudio(withCue=true){if(!cfg.sound)return;let token=++runAudioToken,ctx=ensureAudio();if(!ctx)return;resumeAudio().then(ok=>{if(!ok||token!==runAudioToken||state!=='play'||!cfg.sound)return;if(withCue)startCue();setTimeout(()=>{if(token===runAudioToken&&state==='play'&&cfg.sound)music()},withCue?430:0)})}`
- `L301: function unlockAudioFromGesture(){if(!cfg.sound)return;resumeAudio().then(ok=>{if(ok&&state==='play'&&!seqTimer)music(musicKind||'normal')})}`
- `L314: function music(kind='normal'){if(seqTimer){clearTimeout(seqTimer);seqTimer=null}let token=++musicToken;if(kind==='off'||!cfg.sound)return;musicKind=kind;musicStep=0;let ctx=ensureAudio();if(!ctx)return;if(ctx.state==='running')scheduleMusic(token);else resumeAudio().then(ok=>{if(ok&&token===musicToken&&cfg.sound&&state==='play')scheduleMusic(token)})}`
- `L318: let input={x:0,y:-1,keys:{},jump:false,trick:false,gpj:false,gpp:false},state='menu',world=[],biomass=[],fx=[],trail=[],marks=[],absorptionFx=[],santa=null,ufo=null,beast=null,deathCrash=null,nextSanta=210,nextUfo=95,mode='survival',time=0,dist=0,score=0,style=0,gates=0,miss=0,cam=0,shake=0,buried=0,life=100,timeLimit=60,terrainNotice=0;`
- `L395: addEventListener('keydown',e=>{input.keys[e.code]=true;if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space'].includes(e.code))e.preventDefault();if(e.code==='Escape')pause();if(e.code==='F2'&&state==='play')reset(mode);if(e.code==='KeyH')$('#hud').classList.toggle('hidden')});addEventListener('keyup',e=>input.keys[e.code]=false);`
- `L396: cv.addEventListener('mousemove',e=>{if(state!=='play')return;let r=cv.getBoundingClientRect(),sx=(e.clientX-r.left)/r.width*W,sy=(e.clientY-r.top)/r.height*H,m=screenToWorld(sx,sy);input.x=clamp((m.x-p.x)/92,-1,1);input.y=clamp((m.y-p.y)/115,-1,1);pointerSteerUntil=performance.now()+320});cv.oncontextmenu=e=>e.preventDefault();`
- `L513: if(state==='crash'&&deathCrash?.shattered)return;`
- `L646: function startIncidentIntro(modeName){installCommercialOverlay();commercialV3.seen.clear();commercialV3.intro={t:0,mode:modeName};commercialV3.skipArmed=true;state='intro';let d=document.getElementById('incidentCinema');d.classList.add('intro');document.getElementById('skipCinema').style.display='block';music('off');}`
- `L649: function reset(m='survival'){startIncidentIntro(m)}`
- `L659: function drawCommercialV3(){if(state==='intro'){drawIncidentIntro();return}if(state!=='play'&&state!=='pause')return;let s=worldToScreen(p.x,p.y),r=Math.max(18,p.r*camera.finalZoom),pulse=1+Math.sin(time*5.2)*.06;g.save();g.globalCompositeOperation='screen';`
**Gameplay tuning signals**
- `L119: const IS_MOBILE=matchMedia('(pointer: coarse)').matches,MIN_ZOOM=IS_MOBILE?.32:.34,MAX_ZOOM=1,MAX_RADIUS=600,DEBUG_CAMERA=false,MAX_SPAWN_PER_UPDATE=IS_MOBILE?4:7,MAX_ENTITIES=IS_MOBILE?125:170,MAX_PARTICLES=IS_MOBILE?280:450,MAX_MARKS=IS_MOBILE?220:350,MAX_TRAIL=500;`
- `L120: const camera={x:W/2,y:H/2,zoom:1,targetZoom:1,impactZoom:1,growthZoom:1,lookAheadX:0,lookAheadY:0,offsetY:0,finalZoom:1,bounds:null};`
- `L121: const ISLAND_RADIUS=7600,COAST_WIDTH=520,CHUNK_WIDTH=720,CHUNK_HEIGHT=620,MAX_CHUNKS_GENERATED_PER_UPDATE=IS_MOBILE?1:2,REBASE_DISTANCE=50000,WORLD_SEED=0x5a17c9d3;`
- `L124: const CONTAM_CELL=24,MAX_CONTAM_PER_CHUNK=220;let contaminationStore=new Map(),contaminationStep=0;`
- `L125: const deluxe={weather:'clear',weatherStrength:0,targetWeatherStrength:0,lastBiome:'alpine',combo:0,comboTimer:0,bestCombo:0,variety:new Set(),districtScore:0,eventBonus:0,wind:0,oneShotBiome:true};`
- `L130: function updateCombo(type,value){deluxe.combo=Math.min(99,deluxe.combo+1);deluxe.comboTimer=2.8;deluxe.bestCombo=Math.max(deluxe.bestCombo,deluxe.combo);deluxe.variety.add(type);let varietyBonus=Math.min(2.5,1+deluxe.variety.size*.08),multi=1+Math.min(3,deluxe.combo*.035);return Math.round(value*varietyBonus*multi)}`
- `L153: return{key:chunkKey(cx,cy),x:cx,y:cy,seed,biome,district:biome,urbanity:biome==='downtown'?1:biome==='commercial'?.82:biome==='industrial'?.7:biome==='residential'?.48:biome==='village'?.2:.05,difficulty:Math.min(1,Math.max(0,cy/80)),density:.9+random()*.35,corridor:0,roadWidth:avenueX||avenueY?88:54,avenueX,avenueY,events:[],entities:[],loaded:false};`
- `L158: if(b==='frozen')return r<.24?'dog':r<.37?'bear':r<.43?'villager':r<.54?'rock':r<.65?'hydrant':r<.74?'skatePark':r<.82?'cityBlock':r<.90?'tourist':r<.97?'truck':'waterTower';`
- `L159: if(b==='industrial')return r<.13?'warehouse':r<.24?'factory':r<.33?'garage':r<.42?'parking':r<.50?'train':r<.57?'maintenance':r<.64?'truck':r<.71?'fireTruck':r<.77?'car':r<.84?'waterTower':r<.90?'billboard':r<.96?'powerPlant':r<.985?'villager':'monsterTruck';`
- `L165: const STRUCTURE_COMBO_WINDOW=2.2;let structureCombo={count:0,lastAt:-99,expires:0,mult:1,best:0,lastTier:0};`
- `L176: function featureEntity(chunk,type,x,y,extra={}){let st=OBJECT_STATS[type]||[10,10];return pushChunkEntity(chunk,{type,x,y,w:st[0]*1.2,h:st[0],size:st[0],value:st[1],variant:0,phase:0,hit:false,gone:false,chunkKey:chunk.key,biome:chunk.biome,material:materialFor(type),hp:1,maxHp:1,...extra})}`
- `L179: function makeRiverPoints(random,height=CHUNK_HEIGHT*1.18,turns=7){let pts=[],phase=random()*TAU,amp=35+random()*90,drift=(random()-.5)*60;for(let i=0;i<turns;i++){let t=i/(turns-1),yy=-height/2+t*height,xx=Math.sin(phase+t*(2.2+random()*2.2)*Math.PI)*amp+(t-.5)*drift;pts.push([xx,yy])}return pts}`
- `L200: if(random()<.045)featureEntity(chunk,'lake',cx,cy,{w:100+random()*170,h:60+random()*100,size:0,terrainHazard:true,decorative:true,waterPower:.5});`
- `L201: if(random()<.035)featureEntity(chunk,'river',cx,cy,{w:18+random()*20,h:CHUNK_HEIGHT*1.2,size:0,terrainHazard:true,decorative:true,points:makeRiverPoints(random),waterPower:.45});chunk.loaded=true;return`
- `L203: let pool=cityBuildingPool(d),roadX=chunk.avenueX?88:54,roadY=chunk.avenueY?78:48,sidewalk=14,marginX=roadX*.5+sidewalk+12,marginY=roadY*.5+sidewalk+12,blocks=[[-1,-1],[1,-1],[-1,1],[1,1]],blockW=CHUNK_WIDTH*.5-marginX-18,blockH=CHUNK_HEIGHT*.5-marginY-18;`
- `L220: function canOverrun(e){if(!e||e.terrainHazard||e.decorative)return false;let ballSpan=Math.max(p.r,p.targetR*.96)*2,objectSpan=Math.max(4,e.size||Math.max(e.w||0,e.h||0)*.5),need=overrunRequirement(e);return ballSpan>=objectSpan*need}`
- `L221: function overrunImpact(e){let beforeSpeed=p.speed,beforeMass=p.mass;bury(e);p.speed=Math.max(beforeSpeed,p.speed,p.speedPeak||0);p.speedPeak=Math.max(p.speedPeak||0,p.speed);p.vx*=.985;camera.impactZoom=Math.max(camera.impactZoom,.985);shake=Math.min(shake,Math.max(1.2,(e.size||8)*.035));return p.mass>beforeMass}`
- `L224: function clamp(v,a,b){return Math.max(a,Math.min(b,v))}function lerp(a,b,t){return a+(b-a)*clamp(t,0,1)}`
- `L225: function radiusFromMass(mass){let raw=Math.sqrt(Math.max(0,mass));if(raw<=80)return raw;if(raw<=160)return 80+(raw-80)*.7;return Math.min(MAX_RADIUS,136+(raw-160)*.45)}`
- `L226: function calculateTargetZoom(r){let z;if(r<=40)z=1;else if(r<=75)z=lerp(1,.9,(r-40)/35);else if(r<=130)z=lerp(.9,.79,(r-75)/55);else if(r<=180)z=lerp(.79,.70,(r-130)/50);else if(r<=300)z=lerp(.70,.58,(r-180)/120);else if(r<=450)z=lerp(.58,.46,(r-300)/150);else z=lerp(.46,IS_MOBILE?.35:.37,(r-450)/150);return clamp(z,MIN_ZOOM,MAX_ZOOM)}`
- `L230: function getTargetEntityCount(){let factor=1/(camera.zoom*camera.zoom),raw=46*DIFF[cfg.dif].density*Math.min(2.8,factor);return clamp(Math.round(raw),40,MAX_ENTITIES)}`
- `L261: const PREVIEW=new URLSearchParams(location.search).get('preview')==='1',GAME_ID='alien_threat',SHARED_STATS='ppg_minigames_stats_v1';let statActive=false,statLast=performance.now();`
- `L265: function flushShared(){if(PREVIEW||!statActive)return;let now=performance.now(),delta=Math.min(10,Math.max(0,(now-statLast)/1000));statLast=now;if(delta<.05)return;let all=sharedRead(),s=all[GAME_ID]||{};s.totalSeconds=(s.totalSeconds||0)+delta;all[GAME_ID]=s;sharedWrite(all)}`
- `L270: let ac,seqTimer=null,musicToken=0,musicStep=0,musicKind='normal',noiseBuffer=null,windBuffer=null,crowdAudioTimer=0,windAudioTimer=0,bgmBus=null,bgmTone=null,sfxBus=null,masterBus=null,masterComp=null,audioResumePromise=null,runAudioToken=0,musicRecoveryCooldown=0,lastMusicBeat=0,crawlAudioTimer=0,growthAudioRadius=9;const MUSIC_GAIN=1.9;`
- `L273: function duckMusic(amount=.58,duration=.34){let ctx=ensureAudio();if(!ctx||!bgmBus)return;let now=ctx.currentTime,target=Math.max(.24,Math.min(1.06,amount));bgmBus.gain.cancelScheduledValues(now);bgmBus.gain.setTargetAtTime(target,now,.025);bgmBus.gain.setTargetAtTime(1.06,now+Math.max(.08,duration),.08)}`
- `L281: function crawlSfx(){if(!cfg.sound||state!=='play')return;let size=clamp(p.r/300,0,1),speed=clamp(p.speed/260,0,1),base=48-size*15;filteredNoise(.12+.08*size,'lowpass',135+speed*95,.009+.014*size);tone(base,.09+.07*size,'sine',.01+.012*size,'sfx');if(size>.45)tone(base*.66,.16,'triangle',.006+.008*size,'sfx',.025)}`
- `L311: function windGust(intensity=.5){alienPulseSfx(.3+intensity*.5)}`
- `L312: function updateEnvironmentalAudio(dt){if(!cfg.sound||state!=='play')return;crawlAudioTimer-=dt;crowdAudioTimer-=dt;if(crawlAudioTimer<=0){crawlSfx();crawlAudioTimer=clamp(.48-p.speed*.0007-p.r*.00035,.17,.48)}if(crowdAudioTimer<=0){let danger=musicTension();if(Math.random()<.18+danger*.2)alienPulseSfx(.25+danger*.55);crowdAudioTimer=rnd(2.4,4.8)}}`

### `bow_and_arrow.html`
**Control flow signals**
- `L43: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
- `L99: function audio(){if(!audioOn)return;if(!AC){const A=window.AudioContext||window.webkitAudioContext;if(A)AC=new A()}if(AC&&AC.state==='suspended')AC.resume()}`
- `L108: function reset(){score=0;combo=0;lives=LIVES_MAX;phase=1;totalTime=0;phaseTime=35;spawnTimer=.5;arrows.length=0;targets.length=0;particles.length=0;rainDrops.length=0;charging=false;charge=0;tripleShotTime=0;screenShake=0;lightning=0;chooseWeather(1);hud();showBanner('FASE 1 • '+currentWeather.name)}`
- `L109: function start(){if(running)return;audio();reset();running=true;$('menu').className='menu hidden';startMusic()}`
- `L115: canvas.addEventListener('mousedown',down);addEventListener('mousemove',move);addEventListener('mouseup',up);canvas.addEventListener('touchstart',down,{passive:false});canvas.addEventListener('touchmove',move,{passive:false});canvas.addEventListener('touchend',up,{passive:false});`
**Gameplay tuning signals**
- `L14: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L24: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L59: const PREVIEW=new URLSearchParams(location.search).get('preview')==='1';`
- `L61: let W=800,H=600,DPR=1,last=performance.now(),running=false,charging=false,charge=0,score=0,combo=0,lives=12,phase=1,totalTime=0,phaseTime=35,spawnTimer=.55,bannerTime=0;`
- `L62: const LIVES_MAX=12,aim={x:600,y:250},arrows=[],targets=[],particles=[],rainDrops=[];`
- `L63: let audioOn=!PREVIEW,AC=null,musicTimer=null,musicStep=0,currentWeather=null,tripleShotTime=0,screenShake=0,lightning=0,frameErrors=0;`
- `L64: const wind={value:0,target:0,change:0};`
- `L67: balloon:{name:'Balão',points:10,r:31,hp:1,speed:25,material:'soft'},`
- `L68: bird:{name:'Pássaro',points:25,r:21,hp:1,speed:54,material:'soft'},`
- `L69: kite:{name:'Pipa',points:40,r:29,hp:1,speed:39,material:'soft'},`
- `L70: drone:{name:'Drone',points:70,r:30,hp:3,speed:28,material:'dense'},`
- `L71: ghost:{name:'Fantasma',points:85,r:27,hp:1,speed:37,material:'soft'},`
- `L72: meteor:{name:'Meteoro',points:100,r:30,hp:2,speed:57,material:'dense'},`
- `L73: saucer:{name:'Disco',points:120,r:30,hp:2,speed:50,material:'dense'},`
- `L74: rocket:{name:'Foguete',points:145,r:24,hp:2,speed:66,material:'dense'},`
- `L75: boss:{name:'Mini-chefe',points:200,r:40,hp:4,speed:33,material:'dense'},`
- `L76: dragon:{name:'Dragão',points:350,r:44,hp:4,speed:44,material:'dense'},`
- `L77: gift:{name:'Presente',points:0,r:33,hp:1,speed:18,material:'soft',power:true}`
- `L81: {name:'Sol aberto',key:'sunny',clouds:3,rain:0,storm:false,windBase:12,windSwing:18,skyTop:'#3e96ef',skyMid:'#83d1ff',skyBot:'#ffe0a2'},`
- `L82: {name:'Poucas nuvens',key:'fair',clouds:6,rain:0,storm:false,windBase:18,windSwing:24,skyTop:'#5088db',skyMid:'#9bd8f5',skyBot:'#f7d8a5'},`
- `L83: {name:'Nublado',key:'cloudy',clouds:10,rain:0,storm:false,windBase:23,windSwing:30,skyTop:'#69798e',skyMid:'#b4c2cf',skyBot:'#d9c8ad'},`
- `L84: {name:'Chuva',key:'rain',clouds:13,rain:60,storm:false,windBase:31,windSwing:38,skyTop:'#536272',skyMid:'#8095a9',skyBot:'#b9bea8'},`
- `L85: {name:'Tempestade',key:'storm',clouds:16,rain:88,storm:true,windBase:39,windSwing:46,skyTop:'#2e3d57',skyMid:'#556273',skyBot:'#777665'}`
- `L89: if(hudLeft&&!$('weatherLabel')){const a=document.createElement('span');a.className='weather-chip';a.innerHTML='Clima <b id="weatherLabel">—</b>';hudLeft.appendChild(a);const b=document.createElement('span');b.className='wind-chip';b.innerHTML='Vento <b id="windLabel">↔ 0</b>';hudLeft.appendChild(b)}`
- `L91: const intro=$('menu').querySelector('p');if(intro)intro.innerHTML='Sobreviva a 10 fases com <b>'+LIVES_MAX+' vidas</b>. Mire, tensione e solte. Clima e vento alteram a física; presentes carregados por balões liberam poderes.';`
- `L94: function showError(msg){frameErrors++;const box=$('errorBox');box.textContent='Falha recuperável: '+msg;box.style.display='block';clearTimeout(showError.t);showError.t=setTimeout(()=>box.style.display='none',3500)}`
- `L96: function resize(){DPR=Math.min(devicePixelRatio||1,2);W=Math.max(320,innerWidth);H=Math.max(240,innerHeight);canvas.width=Math.round(W*DPR);canvas.height=Math.round(H*DPR);ctx.setTransform(DPR,0,0,DPR,0,0);if(currentWeather)seedClouds(false)}`
- `L98: function archer(){return{x:Math.max(92,W*.11),y:H*.72}}`

### `campo_minado.html`
**Control flow signals**
- `L357: window.Tone={Synth,PolySynth,NoiseSynth,start:async()=>{const A=get();if(A.state==='suspended')await A.resume()},now:()=>get().currentTime,get context(){return get()}};`
- `L398: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
- `L489: if (audioCtx.state === 'suspended') await audioCtx.resume();`
- `L523: function playGameOverSound() {`
- `L1002: function startTimer() {`
- `L1060: canvas.addEventListener('click', (event) => {`
- `L1095: newGameBtn.addEventListener('click', initGame);`
- `L1097: resetAllBtn.addEventListener('click', () => {`
- `L1101: confirmResetBtn.addEventListener('click', async () => {`
- `L1106: cancelResetBtn.addEventListener('click', () => {`
- `L1110: darkModeBtn.addEventListener('click', () => {`
- `L1115: backBtn.addEventListener('click', () => {`
**Gameplay tuning signals**
- `L369: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L379: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L500: if (endFreq) osc.frequency.exponentialRampToValueAtTime(Math.max(25, endFreq), t + duration);`
- `L501: gain.gain.setValueAtTime(Math.max(0.0001, volume), t);`
- `L557: this.radius = Math.random() * 3 + 1;`
- `L567: this.alpha -= 1 / this.life;`
- `L575: ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);`
- `L611: const availableWidth = Math.min(600, window.innerWidth - padding);`
- `L614: const canvasMaxWidth = Math.min(availableWidth, 560);`
- `L624: while (bombsToPlace > 0) {`
- `L663: if (nr >= 0 && nr < GRID_SIZE && nc >= 0 && nc < GRID_SIZE && board[nr][nc].isBomb) {`
- `L701: createExplosionParticles(col * cellSize + cellSize / 2, row * cellSize + cellSize / 2);`
- `L716: if (board[row][col].adjacentBombs === 0) {`
- `L834: } else if (cell.adjacentBombs > 0) {`
- `L839: ctx.fillText(cell.adjacentBombs.toString(), x + cellSize / 2, y + cellSize / 2 + 2);`
- `L887: ctx.lineWidth = Math.max(1.4, cellSize * 0.04);`
- `L903: ctx.shadowBlur = Math.max(3, cellSize * 0.10);`
- `L907: ctx.lineWidth = Math.max(1.2, cellSize * 0.03);`
- `L945: ctx.shadowBlur = Math.max(8, cellSize * 0.18);`
- `L951: ctx.lineWidth = Math.max(1.2, cellSize * 0.03);`
- `L957: ctx.lineWidth = Math.max(2, cellSize * 0.06);`
- `L962: ctx.lineWidth = Math.max(1, cellSize * 0.025);`
- `L989: if (particles[i].life <= 0) {`
- `L1026: adjacentBombs: 0,`
- `L1046: timerEl.textContent = 'Tempo: 0s';`
- `L1141: if (scores.length > 0) {`
- `L1143: scores.slice(0, 5).forEach((score, index) => {`
- `L1145: li.textContent = '${index + 1}. ${score.name}: ${score.time}s';`

### `click_speed.html`
**Control flow signals**
- `L54: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
- `L81: clickBtn.addEventListener('pointerdown',e=>{if(!started){startGame();return}registerClick(e)});clickBtn.addEventListener('click',e=>e.preventDefault());`
**Gameplay tuning signals**
- `L25: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L35: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L71: let started=false,clickCount=0,startAt=0,endAt=0,raf=0,cooldown=false;const HK='clickSpeedHistoryV2';let history=(()=>{try{return JSON.parse(localStorage.getItem(HK))||{5:[],10:[],30:[],60:[]}}catch{return{5:[],10:[],30:[],60:[]}}})();for(const k of [5,10,30,60])if(!Array.isArray(history[k]))history[k]=[];`
- `L73: function ppgTone(f,d=.035){try{window.PPGPlatform?.tone(f,d,'square',.07)}catch{}}`
- `L76: function tick(now){if(!started)return;const dur=+durationSelect.value*1000,elapsed=Math.min(dur,now-startAt),remain=dur-elapsed,p=elapsed/dur;barFill.style.width=(100-p)*100+'%';timeReadout.textContent=(elapsed/1000).toFixed(2)+'s';timerBox.classList.toggle('danger',remain<=dur*.2);if(now>=endAt)finish();else raf=requestAnimationFrame(tick)}`
- `L78: function registerClick(e){if(!started)return;clickCount++;countEl.textContent=clickCount+' clique'+(clickCount===1?'':'s');particles(e,5+(clickCount%10===0?6:0));ppgTone(190+Math.min(600,clickCount*2),.018);milestone()}`
- `L80: function beginCooldown(){cooldown=true;shield.classList.add('show');const until=performance.now()+750;function c(n){if(n<until)requestAnimationFrame(c);else{cooldown=false;shield.classList.remove('show');clickBtn.disabled=false}}requestAnimationFrame(c)}`

### `corrida_de_cavalos.html`
**Control flow signals**
- `L139: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
- `L209: function startGame() {`
- `L483: if (audioContext.state === 'suspended') audioContext.resume();`
- `L509: function playStartBugle() {`
- `L524: function startHoofbeats() {`
**Gameplay tuning signals**
- `L110: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L120: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L201: let bank = 1000, bet = 100, raceInProgress = false, animationId = null;`
- `L204: function money(value) { return value.toLocaleString('pt-BR', {style:'currency', currency:'BRL', maximumFractionDigits:0}); }`
- `L223: const speed = 60 + Math.random() * 35;`
- `L224: const stamina = 60 + Math.random() * 35;`
- `L226: const rating = speed * .46 + stamina * .34 + temperament * .20;`
- `L227: return { id: crypto.randomUUID ? crypto.randomUUID() : Date.now() + '-' + i, name, color: horseColors[i], speed, stamina, temperament, rating, odds: 0, x: 62, lane: i, phase: Math.random() * Math.PI * 2, finished: false };`
- `L235: h.odds = Math.max(1.35, Math.min(8.5, fair * .9));`
- `L243: bet = Math.min(100, bank);`
- `L245: document.getElementById('raceStatus').textContent = bank > 0 ? 'Selecione um cavalo e confirme sua aposta.' : 'Sua banca terminou. Recarregue a página para recomeçar.';`
- `L247: updateBank(); showHorseButtons(); updateBetUI(); drawScene(0);`
- `L248: document.getElementById('placeBetBtn').disabled = bank <= 0;`
- `L255: btn.innerHTML = '<span class="horse-color" style="background:${horse.color}"></span><span class="horse-name">${index + 1}. ${horse.name}</span><span class="odds">${horse.odds.toFixed(2)}x</span>';`
- `L268: bet = Number.isFinite(raw) ? Math.max(1, Math.floor(raw)) : 100;`
- `L274: readBet(); bet = Math.max(1, Math.min(bank, bet + delta));`
- `L288: if (bet <= 0 || bet > bank) return setMessage('Valor de aposta inválido.', 'error');`
- `L304: const dt = Math.min(.032, (time - lastTime) / 1000 || .016); lastTime = time;`
- `L309: const fatigue = progress > .7 ? (h.stamina / 100) : 1;`
- `L312: h.x += (52 + h.speed * 1.08) * fatigue * variance * temperamentBurst * dt;`
- `L313: h.phase += dt * (10 + h.speed / 10);`
- `L364: const frame = Math.floor(h.phase / 1.6) % 4;`
- `L456: const steps = Math.max(Math.abs(x2 - x1), Math.abs(y2 - y1));`
- `L470: const r = Math.max(0, Math.min(255, (value >> 16) + amount));`
- `L471: const g = Math.max(0, Math.min(255, ((value >> 8) & 255) + amount));`
- `L472: const b = Math.max(0, Math.min(255, (value & 255) + amount));`
- `L503: gain.gain.exponentialRampToValueAtTime(options.volume || 0.1, start + Math.min(.025, duration / 4));`
- `L537: hoofbeatTimer = setInterval(scheduleGroup, 515);`

### `dropworks.html`
**Control flow signals**
- `L153: const audio=new AudioEngine();document.addEventListener('pointerdown',()=>audio.init(),{once:true});document.addEventListener('keydown',()=>audio.init(),{once:true});`
**Gameplay tuning signals**
- `L62: const rr=Array.isArray(r)?Number(r[0]||0):Number(r||0), q=Math.max(0,Math.min(rr,Math.abs(w)/2,Math.abs(h)/2));`
- `L71: let previewIndex=0, previewSwapAt=0;`
- `L95: I18N[code].preview_hint=I18N[code].preview_hint||'Guide the flow, hit the target, waste as little as possible.';`
- `L97: I18N[code].objective_zero_waste=I18N[code].objective_zero_waste||'Hit every target while keeping waste low.';`
- `L115: pt:{weighted_tip:'Dica de timing',ach_heavy_weight_title:'Mira de Produção',ach_heavy_weight_desc:'Capture 250 partículas em recipientes em movimento.',material_elastic:'🟣 Elástico: Quica com muita energia'},`
- `L116: en:{weighted_tip:'Timing tip',ach_heavy_weight_title:'Production Aim',ach_heavy_weight_desc:'Catch 250 particles in moving containers.',material_elastic:'🟣 Elastic: High-energy bouncing material'},`
- `L117: es:{weighted_tip:'Consejo de timing',ach_heavy_weight_title:'Puntería de Producción',ach_heavy_weight_desc:'Captura 250 partículas en recipientes móviles.',material_elastic:'🟣 Elástico: Rebota con mucha energía'},`
- `L118: fr:{weighted_tip:'Astuce de timing',ach_heavy_weight_title:'Visée de Production',ach_heavy_weight_desc:'Capturez 250 particules dans des récipients mobiles.',material_elastic:'🟣 Élastique : Rebondit avec beaucoup d’énergie'},`
- `L119: de:{weighted_tip:'Timing-Tipp',ach_heavy_weight_title:'Produktionsziel',ach_heavy_weight_desc:'Fange 250 Partikel in bewegten Behältern.',material_elastic:'🟣 Elastisch: Springt mit hoher Energie'},`
- `L120: it:{weighted_tip:'Consiglio di timing',ach_heavy_weight_title:'Mira di Produzione',ach_heavy_weight_desc:'Cattura 250 particelle nei contenitori in movimento.',material_elastic:'🟣 Elastico: Rimbalza con molta energia'},`
- `L129: const SUPPLY_I18N={en:{remaining_supply:'Supply',supply_exhausted:'Supply exhausted',supply_failed:'The supply ran out before every target was completed.',supply_tip:'Each stage has a limited supply. Wasted material is gone for good.'}};for(const code of Object.keys(I18N))Object.assign(I18N[code],SUPPLY_I18N[code]||SUPPLY_I18N.en);`
- `L130: const SUPPLY_VISUAL_I18N={en:{used_supply:'Used',supply_status_ok:'Supply healthy',supply_status_low:'Supply getting low',supply_status_critical:'Critical supply',supply_status_empty:'Supply depleted'}};for(const code of Object.keys(I18N))Object.assign(I18N[code],SUPPLY_VISUAL_I18N[code]||SUPPLY_VISUAL_I18N.en);`
- `L131: const PREVIEW=new URLSearchParams(location.search).get('preview')==='1'; if(PREVIEW)document.body.classList.add('preview');`
- `L133: const PREF_KEY='fluxo_prefs_2026_v2', STATS_KEY='fluxo_player_stats_2026', PORTAL_STATS='ppg_minigames_stats_v1', GAME_ID='fluxo';`
- `L137: function detectLang(){const q=new URLSearchParams(location.search).get('lang'); if(q)return normalizeLang(q); if(window.__PORTAL_LANG__)return normalizeLang(window.__PORTAL_LANG__); if(prefs.lang)return normalizeLang(prefs.lang); for(const x of navigator.languages||[]) {const n=normalizeLang(x);if(I18N[n])return n} return normalizeLang(navigator.language)}`
- `L140: window.PrimataLocale={detect:detectLang,get:()=>lang,set:l=>setLanguage(l),t,available:()=>LANGUAGES.slice(),normalize:normalizeLang,refresh:()=>applyI18n()};`
- `L146: const INITIAL={unlockedLevel:1,levelResults:{},totalStars:0,perfectCount:0,currentStreak3Star:0,bestStreak3Star:0,unlockedAchievements:[],movingCatchesCount:0,materialsUsed:['water'],bestWasteRecordPct:100};`
- `L169: const m=level.containers[0]?.motion||{centerX:50,centerY:62,radiusX:28,radiusY:18,speed:.35,direction:1};`
- `L170: this.rigs=[{id:'wheel_main',type:'wheel',centerX:m.centerX,centerY:m.centerY,radiusX:m.radiusX,radiusY:m.radiusY,speed:m.speed,direction:m.direction||1}];`
- `L172: const tracks=[...new Set(level.containers.map(c=>Math.round((c.motion?.trackY??80)*10)/10))];`
- `L173: this.rigs=tracks.map((trackY,i)=>({id:'belt_'+i,type:'conveyor',baseX:50,railHalf:58,laneY:trackY+13,speed:level.containers.find(c=>Math.abs((c.motion?.trackY??80)-trackY)<.11)?.motion?.speed||8,direction:level.containers.find(c=>Math.abs((c.motion?.trackY??80)-trackY)<.11)?.motion?.direction||1}));`
- `L178: this.particles.push({id:++this.particleIdCounter,x:v.x/100*w+(Math.random()-.5)*8,y:v.y/100*h,vx:(Math.random()-.5)*2,vy:Math.random()*2+1,radius:c.radius,material:v.material,color:c.color,bounce:c.bounce,viscosity:c.viscosity,life:0,settled:false});`
- `L183: const dt=Math.max(0,Math.min(.05,(nowMs-this.lastUpdateMs)/1000));`
- `L188: const start=Number(m.startX??-14),end=Number(m.endX??114),dir=(m.direction||1)>=0?1:-1,speed=Number(m.speed)||18;`
- `L190: const margin=Math.max(2,(Number(c.width)||18)*.55);`
- `L193: cs.currentY=(Number(m.trackY??c.y??80))+Math.sin(this.sceneTime*3+(Number(m.phase)||0)*6.283)*(Number(m.bobAmp)||.6);`
- `L195: cs.angle+=(Number(m.speed)||.65)*((m.direction||1)>=0?1:-1)*dt;`
- `L196: cs.currentX=(Number(m.centerX)||50)+Math.cos(cs.angle)*(Number(m.radiusX)||28);`

### `foguetinho.html`
**Control flow signals**
- `L54: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
- `L99: function startMusic(){stopMusic();musicTimer=setInterval(()=>{if(!playing||muted)return;const notes=[110,138.59,164.81,220,164.81,138.59];tone(notes[beat++%notes.length],.16,'triangle',.08);if(beat%4===0)tone(55,.08,'square',.05)},220)}`
- `L102: function resetRocket(){Object.assign(rocket,{x:W/2,y:H-190,vx:0,vy:0,targetX:W/2,tilt:0})}`
- `L128: canvas.addEventListener('pointerdown',e=>{pointer(e);canvas.setPointerCapture(e.pointerId)});canvas.addEventListener('pointermove',e=>{if(e.buttons||e.pointerType==='touch')pointer(e)});`
- `L129: addEventListener('keydown',e=>{keys[e.key]=true;if(e.code==='Space'){e.preventDefault();playing?cashOut():start()}});addEventListener('keyup',e=>keys[e.key]=false);`
**Gameplay tuning signals**
- `L25: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L35: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L89: const W=480,H=720,ui={bank:document.querySelector('#bank'),best:document.querySelector('#best'),mult:document.querySelector('#multiplier'),status:document.querySelector('#status'),bet:document.querySelector('#bet'),action:document.querySelector('#action'),sound:document.querySelector('#sound'),flash:document.querySelector('#flash')};`
- `L90: let bank=100,best=1,playing=false,over=false,stake=0,mult=1,time=0,last=0,spawn=0,difficulty=0,shake=0,muted=false,animationId,hull=100,lastHullHit=-99,hullInvulnUntil=0,dodges=0;`
- `L92: const rocket={x:W/2,y:H-190,vx:0,vy:0,r:15,targetX:W/2,tilt:0};`
- `L96: let ac,master,musicTimer,beat=0;`
- `L97: function initAudio(){if(ac)return;ac=new (window.AudioContext||window.webkitAudioContext)();master=ac.createGain();master.gain.value=muted?0:.18;master.connect(ac.destination)}`
- `L99: function startMusic(){stopMusic();musicTimer=setInterval(()=>{if(!playing||muted)return;const notes=[110,138.59,164.81,220,164.81,138.59];tone(notes[beat++%notes.length],.16,'triangle',.08);if(beat%4===0)tone(55,.08,'square',.05)},220)}`
- `L102: function resetRocket(){Object.assign(rocket,{x:W/2,y:H-190,vx:0,vy:0,targetX:W/2,tilt:0})}`
- `L104: function updateUI(){ui.bank.textContent=bank.toFixed(2);ui.best.textContent=best.toFixed(2);ui.mult.textContent=mult.toFixed(2)+'x'}`
- `L106: const r=Math.random();return Math.min(12,1.15+(-Math.log(1-r))*1.7)}`
- `L109: function cashOut(){if(!playing)return;bank+=stake*mult;best=Math.max(best,mult);playing=false;ui.action.textContent='Iniciar';ui.action.className='btn primary';ui.bet.disabled=false;setStatus('Resgate concluído: +'+(stake*mult).toFixed(2)+' créditos');tone(523,.1);setTimeout(()=>tone(659,.1),80);setTimeout(()=>tone(784,.25),160);stopMusic();updateUI()}`
- `L112: function burst(x,y,c,n=8){for(let i=0;i<n;i++)particles.push({x,y,vx:(Math.random()-.5)*90,vy:(Math.random()-.5)*90,life:.2+Math.random()*.3,c,s:1+Math.random()*3})}`
- `L114: function update(dt){stars.forEach(s=>{s.y+=s.z*(playing?55+mult*12:16)*dt;if(s.y>H){s.y=0;s.x=Math.random()*W}});particles.forEach(p=>{p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=70*dt;p.life-=dt});for(let i=particles.length-1;i>=0;i--)if(particles[i].life<=0)particles.splice(i,1);if(!playing)return;`
- `L115: time+=dt;if(hull<100&&time-lastHullHit>5)hull=Math.min(100,hull+3*dt);mult=1+time*.115+time*time*.0018;difficulty=Math.min(1,(mult-1)/5);if(mult>=crashAt){explode('Falha crítica no propulsor!');return}`
- `L118: trail.push({x:rocket.x+(Math.random()-.5)*8,y:rocket.y+24,life:.25,s:2+Math.random()*5});if(trail.length>42)trail.shift();trail.forEach(t=>{t.y+=100*dt;t.life-=dt});`
- `L119: spawn-=dt;if(spawn<=0){spawnRock();spawn=Math.max(.28,.82-difficulty*.40)}`
- `L126: function loop(ts){const dt=Math.min(.033,(ts-last)/1000||0);last=ts;update(dt);draw();animationId=requestAnimationFrame(loop)}`

### `idle_trader.html`
**Control flow signals**
- `L147: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
- `L275: const state = {`
- `L422: document.getElementById("saveBtn").addEventListener("click", ()=>save(true));`
- `L423: document.getElementById("resetBtn").addEventListener("click", ()=>{`
- `L428: modeBtn.addEventListener("click", ()=>{`
- `L495: document.getElementById('buy1-${a.key}').addEventListener("click", ()=>buyAsset(a.key,1));`
- `L496: document.getElementById('buy10-${a.key}').addEventListener("click", ()=>buyAsset(a.key,10));`
- `L497: document.getElementById('buyMax-${a.key}').addEventListener("click", ()=>{`
- `L536: document.getElementById('buyUpg-${u.key}').addEventListener("click", ()=>buyUpgrade(u.key));`
- `L637: document.getElementById("prestigeBtn").addEventListener("click", doPrestige);`
- `L639: function softReset(preserveRep=true){`
- `L773: function newCandle(initial=false){`
**Gameplay tuning signals**
- `L118: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L128: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L244: const dpr = window.devicePixelRatio || 1;`
- `L246: const maxW = Math.max(1, Math.floor(r.width * dpr));`
- `L247: const maxH = Math.max(1, Math.floor(r.height * dpr));`
- `L248: const sx = Math.max(1, Math.floor(maxW / BASE_W));`
- `L249: const sy = Math.max(1, Math.floor(maxH / BASE_H));`
- `L250: PP.scale = Math.max(1, Math.min(sx, sy));`
- `L266: if(n<1e3) return (neg?"-":"")+n.toLocaleString("pt-BR",{maximumFractionDigits:2});`
- `L269: return (neg?"-":"")+n.toLocaleString("pt-BR",{maximumFractionDigits:2})+(u>=0?units[u]:"");`
- `L280: prestige: { rep:0, mult:1.00, times:0 },`
- `L295: const IPO_THRESHOLD = 1e9;`
- `L365: const elapsed = Math.min(OFFLINE_CAP_HRS*3600, Math.max(0, (Date.now()- (state.lastSave||Date.now()))/1000));`
- `L377: function getIPS(){ return getIPSBase() * state.ipsMult * state.prestige.mult * (state.market?.multIPS||1); }`
- `L378: function getClickValue(){ return state.click * state.prestige.mult * (state.market?.multClick||1); }`
- `L393: return Math.max(0, Math.floor(Math.log(numerator)/Math.log(r)));`
- `L426: soundTgl.addEventListener("change", (e)=>{ state.sound = e.target.checked; if(state.sound) beep(1200,0.05,"square",0.08); save(); });`
- `L461: prestigeBadge.textContent= (em?"🌟 ":"") + 'Reputação x${state.prestige.mult.toFixed(2)}';`
- `L467: prestigeInfo.textContent = 'A cada IPO: converta patrimônio em Reputação permanente. Ganho atual: +${nextRep.toFixed(2)} Rep. (libera em R$ ${fmt(IPO_THRESHOLD)})';`
- `L491: <button class="btn buy" id="buyMax-${a.key}">Máx<br><small id="costMax-${a.key}">R$ 0</small></button>`
- `L498: const k = maxAffordable(a.key, state.money); if(k>0) buyAsset(a.key, k);`
- `L515: if(btnMax){ btnMax.disabled = kmax<=0; document.getElementById('costMax-${a.key}').textContent = kmax>0?'x${kmax} = R$ ${fmt(cmax)}':"x0 = R$ 0"; }`
- `L560: {key:"primeira_ipo", name:"Primeira IPO", desc:"Realize 1 Prestígio.", test: ()=>state.prestige.times>=1},`
- `L600: const kmax = maxAffordable(key, state.money); k = Math.min(k, kmax); if(k<=0) return;`
- `L604: if(!state.ui.reduced) particleBurst(BASE_W/2, BASE_H/2, 10+Math.min(50,k*2), "#73ffa5");`
- `L605: if(!state.ui.reduced) beep(480+Math.min(1200, k*15), 0.05, "square", 0.08);`
- `L627: function calcRepGain(money){ const base = money/1e6; const rep = Math.cbrt(base) * 0.9; return Math.max(0, rep); }`
- `L632: state.prestige.rep += gain; state.prestige.times += 1;`

### `jogo_da_forca.html`
**Control flow signals**
- `L169: function audio(){if(!ac)ac=new (window.AudioContext||window.webkitAudioContext)();if(ac.state==='suspended')ac.resume();return ac}`
- `L177: function startBgm(){`
- `L185: addEventListener('pointerdown',()=>{if(prefs.sound&&!preview)audio()},{once:true,passive:true});`
- `L231: keyboard.addEventListener('pointerdown',()=>{if(prefs.sound&&!preview)audio()},{passive:true});`
- `L255: function startGame(){`
- `L295: function setPaused(next){`
- `L300: addEventListener('keydown',e=>{`
- `L318: function recordStart(){`
**Gameplay tuning signals**
- `L114: const RECORD_KEY='forca_neon_records_v2', PREF_KEY='ppg_platform_prefs_v2', PREF_OLD='ppg_platform_prefs_v1', STATS_KEY='ppg_minigames_stats_v1';`
- `L176: function sfx(kind){const m={tap:[420,.05,'square',.025],good:[660,.09,'triangle',.045],bad:[150,.12,'sawtooth',.035],win:[880,.18,'triangle',.05],lose:[110,.22,'sawtooth',.04],hint:[520,.09,'sine',.035]};tone(...(m[kind]||m.tap))}`
- `L180: bgmTimer=setInterval(()=>{if(!paused&&!document.hidden){tone(notes[i++%notes.length],.22,'sine',.012);}},780);`
- `L187: let current=-1, word='', guesses=new Set(), wrong=new Set(), hintsUsed=0, gameOver=false, startAt=0, pauseAt=0, pausedTotal=0, paused=false, recent=[];`
- `L209: return Math.max(0,(now-startAt-pausedTotal-frozen)/1000);`
- `L241: if(paused||gameOver||hintsUsed>=3)return;`
- `L243: t('hint1',{category:DATA.categories[locale][ci]}),`
- `L244: t('hint2',{related:DATA.words[locale][ri]}),`
- `L245: t('hint3',{count:chars.length,first:chars[0]||''})`
- `L248: if(hintsUsed>=3)$('#hintBtn').disabled=true;`
- `L256: current=chooseIndex();word=DATA.words[locale][current];guesses=new Set();wrong=new Set();hintsUsed=0;gameOver=false;paused=false;pausedTotal=0;pauseAt=0;startAt=Date.now();`
- `L258: mistakesEl.textContent='0';timeEl.textContent='0.0';msg.textContent='';msg.className='message';hintList.innerHTML='';$('#hintBtn').disabled=false;`
- `L268: for(const r of rows){const li=document.createElement('li');li.innerHTML='<strong>${escapeHtml(r.name)}</strong> · ${Number(r.time).toFixed(1)}s · ${t('hintsUsed')}: ${r.hints} · ${t('mistakes')}: ${r.errors}';ranking.append(li)}`
- `L273: const would=[...arr,candidate].sort((a,b)=>a.time-b.time||a.hints-b.hints||a.errors-b.errors).slice(0,5).includes(candidate);`
- `L276: arr.push(candidate);arr.sort((a,b)=>a.time-b.time||a.hints-b.hints||a.errors-b.errors);all[locale]=arr.slice(0,5);writeJSON(RECORD_KEY,all);renderRanking();`
- `L297: paused=next;if(paused){pauseAt=Date.now();$('#pauseOverlay').classList.add('open');sfx('tap')}else{pausedTotal+=Date.now()-pauseAt;pauseAt=0;$('#pauseOverlay').classList.remove('open')}`
- `L312: recordsBtn.onclick=()=>{const rows=localeRecords();openModal('<h2>${t('recordsTitle')}</h2>${rows.length?'<ol>${rows.map(r=>'<li><strong>${escapeHtml(r.name)}</strong> · ${Number(r.time).toFixed(1)}s · ${t('hintsUsed')}: ${r.hints} · ${t('mistakes')}: ${r.errors}</li>').join('')}</ol>':'<p>${t('noRecords')}</p>'}')};`
- `L320: s.starts=(s.starts||0)+1;const d=today();if(s.lastDay!==d){s.currentStreak=s.lastDay&&dayDiff(d,s.lastDay)===1?(s.currentStreak||0)+1:1;s.longestStreak=Math.max(s.longestStreak||0,s.currentStreak);s.lastDay=d}`
- `L325: const now=performance.now(),dt=(!document.hidden&&!paused)?Math.max(0,(now-statsLast)/1000):0;statsLast=now;if(!dt)return;`
- `L328: setInterval(()=>{if(!paused&&!gameOver)timeEl.textContent=elapsed().toFixed(1);flushStats()},100);`

### `jogo_da_velha.html`
**Control flow signals**
- `L82: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
- `L240: function resetGame() {`
- `L272: canvas.addEventListener("click", handleClick);`
**Gameplay tuning signals**
- `L53: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L63: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L111: let score = 0;`
- `L112: let timer = 0;`
- `L197: const m=ranked[Math.min(pick,ranked.length-1)]; move=[m.r,m.c];`
- `L216: score = Math.max(10, 100 - timer * 2);`
- `L231: if (score > 0) {`
- `L243: timer = 0;`
- `L244: score = 0;`
- `L258: localStorage.setItem("velha_quantica_scores", JSON.stringify(scores.slice(0, 5)));`

### `kombo_blocks.html`
**Control flow signals**
- `L50: function renderDynamicI18n(){renderModeOptions();$('#playerInput').placeholder=t('defaultPlayer');$('#pauseBtn').textContent=gameState==='PAUSED'?t('resume'):t('pause');if($('#leaderMode'))renderLeaderboard();}`
- `L60: const audio=new AudioEngine();addEventListener('pointerdown',()=>audio.init(),{once:true});addEventListener('keydown',()=>audio.init(),{once:true});`
- `L99: function togglePause(){if(gameState==='PLAYING'){gameState='PAUSED';audio.stopMusic();showOverlay(t('paused'),t('restartHint'))}else if(gameState==='PAUSED'){gameState='PLAYING';hideOverlay();lastDrop=performance.now();if(settings.musicEnabled)audio.startMusic()}renderDynamicI18n()}`
- `L101: function getModeStartToast(){return t({classic:'startClassic',fullClassic:'startFullClassic',stackAttack:'startStack',timeAttack:'startTime',zen:'startZen',dailyChallenge:'startDaily',turbo:'startTurbo'}[settings.gameMode]||'startClassic')}`
- `L104: function endGame(timeup=false){if(gameState==='GAMEOVER')return;gameState='GAMEOVER';audio.stopMusic();audio.over();saveLeaderboard();showOverlay(timeup?t('timeUp'):t('gameOver'),t('finalScore',{score:stats.score})+' '+t('restartHint'));updateHUD()}`
- `L105: function home(){gameState='MENU';audio.stopMusic();$('#gameView').classList.add('hidden');$('#menuView').classList.remove('hidden');hideOverlay();renderDynamicI18n()}`
- `L106: function restart(){startGame(settings.gameMode==='fullClassic')}`
- `L109: board.addEventListener('pointerdown',e=>{if(gameState!=='PLAYING'||!settings.allowBoardDragSwap)return;let r=board.getBoundingClientRect(),c=Math.floor((e.clientX-r.left)/r.width*W),rr=Math.floor((e.clientY-r.top)/r.height*H)+BUF;if(!grid[rr]?.[c]){selected=null;return}if(!selected){selected=[rr,c];return}doSwap(selected[0],selected[1],rr,c);selected=null});`
**Gameplay tuning signals**
- `L35: const I=window.KOMBO_I18N, LANGS=['en','pt-BR','es','fr','de','it','tr','ru','ja','ko','zh-CN'], AUT={en:'English','pt-BR':'Português do Brasil',es:'Español',fr:'Français',de:'Deutsch',it:'Italiano',tr:'Türkçe',ru:'Русский',ja:'日本語',ko:'한국어','zh-CN':'简体中文'}, LK='primata_locale_v1';`
- `L47: const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)], PREVIEW=new URLSearchParams(location.search).get('preview')==='1';if(PREVIEW)document.body.classList.add('preview');`
- `L53: const DEFAULTS={gameMode:'classic',enableMatch3:true,colorMode:'multicolor',includeExtendedPieces:true,gravityCascade:true,startingLevel:1,difficulty:'medium',ghostPiece:true,soundEnabled:true,soundVolume:.5,musicEnabled:true,musicVolume:.35,allowBoardDragSwap:true,blockTheme:'modern',theme:'dark'};`
- `L54: let settings=load('kombo_blocks_settings_v2',DEFAULTS);settings={...DEFAULTS,...settings};let playerName=localStorage.getItem('kombo_blocks_player_name')||'';`
- `L62: const W=10,H=20,BUF=2,T=22,CELL=30;const COLORS={blue:'#295bff',cyan:'#2fd8ff',green:'#35d57b',teal:'#82e9e1',yellow:'#ffe15a',orange:'#f29b38',red:'#ef4e62',purple:'#8c5bff',pink:'#ff67b2',lime:'#91ed58',amber:'#f4bd48',violet:'#6e7cff',coral:'#ff7b65'};const ALL=Object.keys(COLORS);`
- `L63: const CLASSIC=[['I','cyan',[[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]]],['J','blue',[[1,0,0],[1,1,1],[0,0,0]]],['L','orange',[[0,0,1],[1,1,1],[0,0,0]]],['O','yellow',[[1,1],[1,1]]],['S','green',[[0,1,1],[1,1,0],[0,0,0]]],['T','purple',[[0,1,0],[1,1,1],[0,0,0]]],['Z','red',[[1,1,0],[0,1,1],[0,0,0]]]];`
- `L64: const EXT=[['PLUS','pink',[[0,1,0],[1,1,1],[0,1,0]]],['MINI_L','lime',[[1,0],[1,1]]],['LONG_5','teal',[[0,0,0,0,0],[0,0,0,0,0],[1,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0]]],['BIG_L','violet',[[1,0,0],[1,0,0],[1,1,1]]],['U_SHAPE','amber',[[1,0,1],[1,1,1],[0,0,0]]],['W_SHAPE','coral',[[1,0,0],[1,1,0],[0,1,1]]],['CORNER_3','green',[[0,1,0],[0,1,1],[0,0,0]]]];`
- `L73: function findHint(g){for(let r=0;r<T;r++)for(let c=0;c<W;c++){if(!g[r][c])continue;for(const[dr,dc]of[[0,1],[1,0]]){let r2=r+dr,c2=c+dc;if(r2<T&&c2<W&&g[r2][c2]){let n=g.map(x=>[...x]);[n[r][c],n[r2][c2]]=[n[r2][c2],n[r][c]];if(matchGroups(n).length)return[[r,c],[r2,c2]]}}}return null}`
- `L74: function dropInterval(){let base=settings.difficulty==='easy'?1120:settings.difficulty==='hard'?670:910,min=settings.difficulty==='easy'?160:settings.difficulty==='hard'?50:80;return Math.max(min,Math.floor(base*Math.pow(.90,Math.max(0,stats.level-1))))}`
- `L78: function themeColor(c){if(settings.blockTheme==='colorblind'){let map={red:'#d55e00',green:'#009e73',blue:'#0072b2',yellow:'#f0e442',orange:'#e69f00',purple:'#cc79a7',cyan:'#56b4e9'};return map[c]||COLORS[c]}return COLORS[c]||'#fff'}`
- `L82: function addParticles(cells,color){for(const[r,c]of cells){if(r<BUF)continue;for(let i=0;i<7;i++)particles.push({x:c*30+15,y:(r-BUF)*30+15,vx:(Math.random()-.5)*5,vy:(Math.random()-.7)*5,life:24+Math.random()*15,color:themeColor(color),s:2+Math.random()*3})}}`
- `L83: function drawParticles(){for(let i=particles.length-1;i>=0;i--){let p=particles[i];ctx.globalAlpha=Math.max(0,p.life/35);ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(p.x,p.y,p.s,0,7);ctx.fill();ctx.globalAlpha=1;p.x+=p.vx;p.y+=p.vy;p.vy+=.15;if(--p.life<=0)particles.splice(i,1)}}`
- `L85: function fmtTime(s){s=Math.max(0,s|0);return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0')}`
- `L86: function toast(msg,type='good'){let d=document.createElement('div');d.className='toast '+type;d.textContent=msg;$('#toasts').appendChild(d);setTimeout(()=>d.remove(),2900)}`
- `L88: function registerElim(){let now=Date.now();elimTimes.push(now);elimTimes=elimTimes.filter(x=>now-x<10000);if(elimTimes.length>=2){stats.level++;toast(t('pacemaker'),'warn');audio.level();elimTimes=[]}}`
- `L89: function spawn(){active=queue.shift()||makePiece();queue.push(makePiece());canHold=true;if(collide(active,grid)){if(settings.gameMode==='zen'){for(let r=T-5;r<T;r++)grid[r]=Array(W).fill(null);grid=gravity(grid);toast(t('zenRelief'),'good');active=makePiece()}else endGame(false)}}`
- `L91: let[n,lines]=clearLines(grid);if(lines){did=true;totalEvent=true;grid=n;let base=[0,100,300,500,800][Math.min(4,lines)]||800,pts=Math.round(base*stats.level*Math.max(1,stats.mult));stats.score+=pts;stats.lines+=lines;audio.line(lines);shake();toast(t('linesToast',{lines,points:pts}),'warn');if(settings.gravityCascade)grid=gravity(grid);chain++}if(!did)break}`
- `L94: function move(dx){if(gameState!=='PLAYING'||!active)return;lastAction=Date.now();hint=null;if(!collide(active,grid,dx,0)){active.x+=dx;audio.move()}}`
- `L95: function soft(){if(gameState!=='PLAYING'||!active)return;lastAction=Date.now();hint=null;if(!collide(active,grid,0,1)){active.y++;stats.score++;audio.move()}else lockAndContinue()}`
- `L96: function hard(){if(gameState!=='PLAYING'||!active)return;lastAction=Date.now();hint=null;let d=0;while(!collide(active,grid,0,1)){active.y++;d++}stats.score+=d*2;lockAndContinue()}`
- `L99: function togglePause(){if(gameState==='PLAYING'){gameState='PAUSED';audio.stopMusic();showOverlay(t('paused'),t('restartHint'))}else if(gameState==='PAUSED'){gameState='PLAYING';hideOverlay();lastDrop=performance.now();if(settings.musicEnabled)audio.startMusic()}renderDynamicI18n()}`
- `L105: function home(){gameState='MENU';audio.stopMusic();$('#gameView').classList.add('hidden');$('#menuView').classList.remove('hidden');hideOverlay();renderDynamicI18n()}`
- `L109: board.addEventListener('pointerdown',e=>{if(gameState!=='PLAYING'||!settings.allowBoardDragSwap)return;let r=board.getBoundingClientRect(),c=Math.floor((e.clientX-r.left)/r.width*W),rr=Math.floor((e.clientY-r.top)/r.height*H)+BUF;if(!grid[rr]?.[c]){selected=null;return}if(!selected){selected=[rr,c];return}doSwap(selected[0],selected[1],rr,c);selected=null});`
- `L113: $$('.touchControls button').forEach(b=>b.onclick=()=>{let a=b.dataset.act;if(a==='left')move(-1);if(a==='right')move(1);if(a==='rotate')rotatePiece(false);if(a==='down')soft();if(a==='drop')hard();if(a==='hold')holdPiece();if(a==='hint')manualHint();if(a==='pause')togglePause()});`
- `L117: ${toggleSetting('enableMatch3','enableMatch3')}${toggleSetting('includeExtendedPieces','extendedPieces')}${toggleSetting('gravityCascade','gravityCascade')}${toggleSetting('ghostPiece','ghostPiece')}${toggleSetting('allowBoardDragSwap','boardSwap')}${toggleSetting('soundEnabled','soundEffects')}${toggleSetting('musicEnabled','music')}`
- `L128: cur=detect();$('#playerInput').value=playerName;$('#difficultySelect').value=settings.difficulty;renderLangPanel();refresh();renderModeOptions();$('#modeSelect').value=settings.gameMode;$('#modeDesc').textContent=t(modeKeys[settings.gameMode][1]);updateToolbar();$('#boardFrame').dataset.theme=settings.blockTheme;console.info('[PrimataLocale]',validate());`
- `L129: if(PREVIEW){settings.soundEnabled=false;settings.musicEnabled=false;settings.gameMode='classic';settings.difficulty='medium';$('#modeSelect').value='classic';$('#difficultySelect').value='medium';setTimeout(()=>startGame(false),80)}`

### `leaping_into_life.html`
**Control flow signals**
- `L54: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
**Gameplay tuning signals**
- `L25: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L35: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L77: let frog={},obstacles=[],particles=[],fireflies=[],score=0,running=false,startAt=0,last=performance.now(),spawnDist=0,shake=0,flash=0,demo=PREVIEW,waterT=0;function fmt(s){s=Math.max(0,Math.floor(s||0));return '${String(Math.floor(s/60)).padStart(2,'0')}:${String(s%60).padStart(2,'0')}'}`
- `L80: function addObstacle(){let m=MODES[diffEl.value],margin=92,water=625,center=margin+Math.random()*(water-margin*2),gap=m.gap+Math.sin(score*.7)*8;center=Math.max(130,Math.min(water-120,center));obstacles.push({x:W+60,w:72,top:center-gap/2,bottom:center+gap/2,passed:false,seed:Math.random()*10});}`
- `L81: function burst(x,y,color,n=12){for(let i=0;i<n;i++){let a=Math.random()*Math.PI*2,sp=25+Math.random()*95;particles.push({x,y,vx:Math.cos(a)*sp,vy:Math.sin(a)*sp,life:.35+Math.random()*.55,size:1.5+Math.random()*4,color})}}`
- `L88: function draw(dt){waterT+=dt;ctx.save();if(shake>0)ctx.translate((Math.random()-.5)*shake,(Math.random()-.5)*shake);sky();effects(dt);for(let o of obstacles)treeObstacle(o);lake(waterT);frogDraw();if(flash>0){ctx.fillStyle='rgba(240,255,210,${flash*.14})';ctx.fillRect(0,0,W,H)}ctx.restore();shake=Math.max(0,shake-dt*24);flash=Math.max(0,flash-dt*2.8)}`
- `L89: function frame(now){let dt=Math.min(.035,(now-last)/1000||0);last=now;update(dt);draw(dt);requestAnimationFrame(frame)}reset();requestAnimationFrame(frame);if(PREVIEW)setTimeout(start,60);`

### `memory_genius.html`
**Control flow signals**
- `L286: window.Tone={Synth,PolySynth,NoiseSynth,start:async()=>{const A=get();if(A.state==='suspended')await A.resume()},now:()=>get().currentTime,get context(){return get()}};`
- `L328: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
- `L475: greenButton.addEventListener('click', () => handleColorClick('green'));`
- `L476: redButton.addEventListener('click', () => handleColorClick('red'));`
- `L477: yellowButton.addEventListener('click', () => handleColorClick('yellow'));`
- `L478: blueButton.addEventListener('click', () => handleColorClick('blue'));`
- `L480: startBtn.addEventListener('click', () => {`
- `L490: soundBtn.addEventListener('click', toggleSound);`
- `L491: resetBtn.addEventListener('click', showResetModal);`
- `L492: darkModeBtn.addEventListener('click', toggleDarkMode);`
- `L493: backBtn.addEventListener('click', goBack);`
- `L494: saveScoreBtn.addEventListener('click', saveScore);`
**Gameplay tuning signals**
- `L299: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L309: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L435: let level = 1;`
- `L436: let score = 0;`
- `L444: let life = 100;`
- `L593: level = 1;`
- `L594: score = 0;`
- `L595: life = 100; lastLifeHit = 0;`
- `L602: timerDisplay.textContent = '00:00';`
- `L623: }, Math.max(360, 620 - (level - 1) * 13)); // ritmo adaptativo: claro no início, mais rápido nos níveis altos`
- `L629: timerInterval = setInterval(updateTimer, 1000);`
- `L637: if (gameActive && life < 100 && Date.now() - lastLifeHit > 5000) life = Math.min(100, life + 1);`
- `L638: const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');`
- `L651: life = Math.max(0, life - 30); lastLifeHit = Date.now();`
- `L652: score = Math.max(0, score - Math.max(2, level * 2)); scoreDisplay.textContent = score;`
- `L654: if (life <= 0) { gameOver(); return; }`
- `L661: score += level * 10;`
- `L662: if(level % 5 === 0) life = Math.min(100, life + 15);`
- `L668: if (level > 20) { // Nível de vitória`
- `L686: const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');`
- `L690: const finalLevelVal = level > 1 ? level -1 : (sequence.length > 0 ? 1: 0) ; // Se perdeu no nível 1, mostra 1, ou 0 se não começou`
- `L718: const currentLevel = level > 1 ? level -1 : (sequence.length > 0 ? 1: 0) ;`
- `L775: // level = 1; score = 0;`
- `L778: // timerDisplay.textContent = '00:00';`

### `pixel_bomberman.html`
**Control flow signals**
- `L46: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
- `L68: function safeStart(x,y){return x>=0&&y>=0&&x+y<=2}`
- `L76: function restartGame(){score=0;lives=MAX_LIVES;level=1;framesSinceDamage=0;invulnerable=0;gameOver=false;bombs=[];flames=[];initMap();updateHud();sfx(520,.07)}window.PPGGameRestart=restartGame;`
**Gameplay tuning signals**
- `L17: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L27: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L63: const MAX_LIVES=3,MAX_BOMBS=2;let map=[],bombs=[],flames=[],enemies=[],score=0,lives=MAX_LIVES,level=1,enemyMoveTimer=0,framesSinceDamage=0,invulnerable=0,transitionFrames=0,gameOver=false;`
- `L66: const spritePlayer=[[0,1,0],[1,1,1],[1,0,1]],spriteEnemy=[[1,1,1],[1,0,1],[1,1,1]],spriteBlock=[[1,1,1],[1,0,1],[1,1,1]],spriteWall=[[1,0,1],[0,1,0],[1,0,1]];`
- `L67: function sfx(f,d=.045){try{window.PPGPlatform?.sfx?.(f,d)}catch{}}`
- `L76: function restartGame(){score=0;lives=MAX_LIVES;level=1;framesSinceDamage=0;invulnerable=0;gameOver=false;bombs=[];flames=[];initMap();updateHud();sfx(520,.07)}window.PPGGameRestart=restartGame;`
- `L78: function placeBomb(){if(gameOver){restartGame();return}if(transitionFrames||bombs.length>=MAX_BOMBS||bombAt(player.x,player.y))return;bombs.push({x:player.x,y:player.y,timer:80});sfx(240,.045)}`
- `L79: function flameCell(x,y){if(!map[y]||map[y][x]==='wall')return false;flames.push({x,y,timer:24});if(map[y][x]==='block'){map[y][x]='empty';score+=15;return false}const chained=bombs.find(b=>b.x===x&&b.y===y&&b.timer>2);if(chained)chained.timer=1;return true}`
- `L81: function movePlayer(dx,dy){if(gameOver||transitionFrames||window.__PPG_PAUSED__)return;const nx=player.x+dx,ny=player.y+dy;if(dx||dy){if(canWalk(nx,ny)){player.x=nx;player.y=ny}else sfx(170,.02)}}`

### `pong.html`
**Control flow signals**
- `L43: let state='menu',last=performance.now(),elapsed=0,serveTimer=.7,mode='ai',difficulty=1,seriesIndex=0,chaos=false,sudden=false,goalPauseTimer=0,goalPending=null;`
- `L91: function resetAttract(){attract.left.y=H/2-attract.left.h/2;attract.right.y=H/2-attract.right.h/2;attract.left.vy=attract.right.vy=0;attract.ball.x=W/2;attract.ball.y=H/2;attract.ball.vx=(Math.random()<.5?-1:1)*rnd(330,430);attract.ball.vy=rnd(-230,230)}`
- `L108: const modal=document.querySelector('#modal'),body=document.querySelector('#modalBody');function openModal(h){body.innerHTML=h;modal.classList.add('open')}function closeModal(){modal.classList.remove('open')}modal.addEventListener('click',e=>{if(e.target===modal||e.target.closest('.close'))closeModal()});`
**Gameplay tuning signals**
- `L41: const W=960,H=540,WIN=10,BASE=400,MAX=965,BASE_H=122;`
- `L42: const clamp=(v,a,b)=>Math.max(a,Math.min(b,v)),rnd=(a,b)=>a+Math.random()*(b-a),pick=a=>a[(Math.random()*a.length)|0],lerp=(a,b,t)=>a+(b-a)*t;`
- `L43: let state='menu',last=performance.now(),elapsed=0,serveTimer=.7,mode='ai',difficulty=1,seriesIndex=0,chaos=false,sudden=false,goalPauseTimer=0,goalPending=null;`
- `L48: const prefs=(()=>{try{return JSON.parse(localStorage.getItem('ppg_platform_prefs_v1'))||{}}catch{return {}}})();let soundOn=prefs.sound!==false,pointerTarget=null;if(prefs.theme==='light')document.body.classList.add('light');`
- `L50: const mkP=(side,x,color,center)=>({side,x,y:H/2-BASE_H/2,w:18,h:BASE_H,vy:0,score:0,setWins:0,shield:0,meter:0,color,center,fatigue:0,reaction:0,target:H/2,notice:0,distance:0});`
- `L53: const combo={p1:0,p2:0},comboPeak={p1:0,p2:0},tech={p1:0,p2:0},hitStreak={p1:0,p2:0};`
- `L54: const stats={p1:{hits:0,perfect:0,center:0,power:0,smart:0,goals:0,shield:0,supers:0,maxCombo:0,maxRally:0,maxSpeed:0},p2:{hits:0,perfect:0,center:0,power:0,smart:0,goals:0,shield:0,supers:0,maxCombo:0,maxRally:0,maxSpeed:0}};`
- `L55: let rally=0,powerup=null,powerTimer=6,modifier=null,modifierTimer=14,slowmo=0,triple=0;`
- `L58: const MODS=[{type:'gravity',name:'GRAVITY WAVE',color:'#ff8ad8',dur:9},{type:'magnet',name:'MAGNET CORE',color:'#5effe4',dur:9},{type:'bumpers',name:'NEON BUMPERS',color:'#ffd34d',dur:10},{type:'blackout',name:'BLACKOUT',color:'#a98cff',dur:8},{type:'narrow',name:'NARROW TUNNEL',color:'#ff765d',dur:9}];`
- `L59: let ac=null,master=null,musicBus=null,sfxBus=null,noise=null,musicStep=0,musicClock=0,morph=.35,morphTarget=.35,morphClock=10;`
- `L61: function osc(f,d=.07,type='square',v=.12,when=0,bus=sfxBus){if(!soundOn||!audioInit())return;const t=ac.currentTime+when,o=ac.createOscillator(),g=ac.createGain();o.type=type;o.frequency.setValueAtTime(f,t);g.gain.setValueAtTime(Math.max(.0001,v),t);g.gain.exponentialRampToValueAtTime(.0001,t+d);o.connect(g).connect(bus||sfxBus);o.start(t);o.stop(t+d)}`
- `L68: let runtimeFaults=0;function safeFx(fn,label='fx'){try{return fn()}catch(err){runtimeFaults++;console.warn('Neon Pong non-critical '+label+' error:',err);return null}}`
- `L69: function mult(side){return Math.min(5,1+Math.floor(Math.max(0,combo[side]-1)/2)*.5)}function score(side,pts,why=''){const m=fx[side].glass>0?2:1;tech[side]+=Math.round(pts*m);if(why&&pts>=150)announce('${side==='p1'?'P1':'P2'} +${Math.round(pts*m)}',why,side==='p1'?'#63edff':'#ffd34d',.7)}`
- `L81: function reflectBounds(b){const top=arenaTop()+b.r,bot=arenaBottom()-b.r;if(b.y<top&&b.vy<0){b.y=top;b.vy*=-1;osc(150+clamp((b.base-BASE)/(MAX-BASE),0,1)*280,.035,'triangle',.07)}if(b.y>bot&&b.vy>0){b.y=bot;b.vy*=-1;osc(150+clamp((b.base-BASE)/(MAX-BASE),0,1)*280,.035,'triangle',.07)}}`

### `salve_os_gatinhos.html`
**Control flow signals**
- `L57: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
- `L79: let state='menu',score=0,lives=3,combo=1,best=0,elapsed=0,spawnTimer=1.2,shake=0,flash=0,muted=false,last=performance.now(),lastLifeLoss=-99,lifeRegenAcc=0,rescueCount=0;`
- `L88: function audioOn(){if(!ac){ac=new (window.AudioContext||window.webkitAudioContext)();master=ac.createGain();master.gain.value=.18;master.connect(ac.destination)}if(ac.state==='suspended')ac.resume();startMusic()}`
- `L91: function startMusic(){if(musicTimer||!ac)return;let n=0;const notes=[220,277,330,440,330,277,247,330];musicTimer=setInterval(()=>{if(state==='play'&&!muted){tone(notes[n++%notes.length],.11,'triangle',.035);if(n%4===1)tone(110,.16,'square',.025,-20)}},240)}`
- `L93: function reset(){score=0;lives=3;combo=1;elapsed=0;spawnTimer=.8;cats=[];particles=[];player.x=433;player.vx=0;lastLifeLoss=-99;lifeRegenAcc=0;rescueCount=0;state='play';ui.overlay.classList.add('hidden');syncUI();audioOn()}`
- `L95: function gameOver(){state='over';best=Math.max(best,score);ui.title.textContent='FIM DO RESGATE';ui.message.innerHTML='Pontuação: <b>${score}</b><br>Recorde desta sessão: <b>${best}</b>';ui.start.textContent='TENTAR NOVAMENTE';ui.overlay.classList.remove('hidden')}`
- `L123: function bindHold(id,key){const el=document.querySelector(id);const on=e=>{e.preventDefault();keys[key]=true;audioOn()},off=e=>{e.preventDefault();keys[key]=false};el.addEventListener('pointerdown',on);el.addEventListener('pointerup',off);el.addEventListener('pointercancel',off);el.addEventListener('pointerleave',off)}`
- `L125: addEventListener('keydown',e=>{if(['ArrowLeft','a','A'].includes(e.key))keys.left=true;if(['ArrowRight','d','D'].includes(e.key))keys.right=true;if([' ','Enter'].includes(e.key)&&state!=='play')reset();if(['ArrowLeft','ArrowRight',' '].includes(e.key))e.preventDefault();audioOn()});`
- `L127: ui.start.addEventListener('click',reset);ui.sound.addEventListener('click',()=>{muted=!muted;ui.sound.textContent=muted?'🔇':'🔊';if(!muted)audioOn()});`
**Gameplay tuning signals**
- `L28: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L38: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L79: let state='menu',score=0,lives=3,combo=1,best=0,elapsed=0,spawnTimer=1.2,shake=0,flash=0,muted=false,last=performance.now(),lastLifeLoss=-99,lifeRegenAcc=0,rescueCount=0;`
- `L81: const player={x:440,y:453,w:94,h:21,vx:0,max:430,acc:1900,drag:9};`
- `L84: for(let b=0;b<6;b++)for(let f=0;f<5;f++)windows.push({x:25+b*158+32+(f%2)*65,y:100+f*64,b,f,lit:Math.random()<.36});`
- `L88: function audioOn(){if(!ac){ac=new (window.AudioContext||window.webkitAudioContext)();master=ac.createGain();master.gain.value=.18;master.connect(ac.destination)}if(ac.state==='suspended')ac.resume();startMusic()}`
- `L90: function sfx(name){if(name==='catch'){tone(520,.08,'square',.16,180);tone(790,.14,'square',.1,80,.07)}if(name==='miss'){tone(150,.32,'sawtooth',.12,-80)}if(name==='spawn')tone(730,.06,'square',.05,-150)}`
- `L91: function startMusic(){if(musicTimer||!ac)return;let n=0;const notes=[220,277,330,440,330,277,247,330];musicTimer=setInterval(()=>{if(state==='play'&&!muted){tone(notes[n++%notes.length],.11,'triangle',.035);if(n%4===1)tone(110,.16,'square',.025,-20)}},240)}`
- `L93: function reset(){score=0;lives=3;combo=1;elapsed=0;spawnTimer=.8;cats=[];particles=[];player.x=433;player.vx=0;lastLifeLoss=-99;lifeRegenAcc=0;rescueCount=0;state='play';ui.overlay.classList.add('hidden');syncUI();audioOn()}`
- `L94: function syncUI(){ui.score.textContent=String(score).padStart(6,'0');ui.combo.textContent='COMBO x'+combo;ui.lives.textContent='♥ '.repeat(lives).trim()||'SEM VIDAS'}`
- `L100: function burst(x,y,color,n=10){for(let i=0;i<n;i++){const a=Math.random()*Math.PI*2,s=30+Math.random()*150;particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s-45,life:.35+Math.random()*.45,max:.8,color,size:2+Math.random()*4})}}`
- `L101: function update(dt){if(state!=='play')return;elapsed+=dt;if(lives<3&&elapsed-lastLifeLoss>12){lifeRegenAcc+=dt;if(lifeRegenAcc>=20){lifeRegenAcc=0;lives++;sfx('catch');syncUI()}}shake=Math.max(0,shake-dt*18);flash=Math.max(0,flash-dt*3);`
- `L102: const axis=(keys.right?1:0)-(keys.left?1:0);player.vx+=axis*player.acc*dt;player.vx*=Math.exp(-player.drag*dt);player.vx=Math.max(-player.max,Math.min(player.max,player.vx));player.x=Math.max(5,Math.min(W-player.w-5,player.x+player.vx*dt));`
- `L103: spawnTimer-=dt;if(spawnTimer<=0){spawnCat();const d=Math.min(1,elapsed/100);spawnTimer=.64+Math.random()*.68+(1-d)*.55}`
- `L104: const wind=Math.sin(elapsed*.73)*12*Math.min(1,elapsed/70);`
- `L105: for(let i=cats.length-1;i>=0;i--){const c=cats[i];c.vy+=390*dt;c.vx+=wind*dt;c.x+=c.vx*dt;c.y+=c.vy*dt;c.rot+=c.spin*dt;`
- `L110: if(caught){score+=100*combo;combo=Math.min(9,combo+1);rescueCount++;if(rescueCount%15===0&&lives<3){lives++;lifeRegenAcc=0}sfx('catch');c.vy=-250;c.vx+=player.vx*.25;burst(c.x,c.y,c.color,16);cats.splice(i,1);shake=4;flash=.3;syncUI();continue}`
- `L111: if(c.y>H+20){cats.splice(i,1);lives--;lastLifeLoss=elapsed;lifeRegenAcc=0;combo=1;shake=12;burst(c.x,GROUND,'#ef476f',18);sfx('miss');syncUI();if(lives<=0)gameOver()}`
- `L113: for(let i=particles.length-1;i>=0;i--){const p=particles[i];p.life-=dt;p.vy+=240*dt;p.x+=p.vx*dt;p.y+=p.vy*dt;if(p.life<=0)particles.splice(i,1)}`
- `L122: function loop(now){const dt=Math.min(.033,(now-last)/1000);last=now;update(dt);draw();requestAnimationFrame(loop)}`

### `snowball_avalanche.html`
**Control flow signals**
- `L217: function resumeAudio(){let ctx=ensureAudio();if(!ctx)return Promise.resolve(null);if(ctx.state==='running')return Promise.resolve(ctx);if(audioResumePromise)return audioResumePromise;audioResumePromise=ctx.resume().catch(()=>null).then(()=>{audioResumePromise=null;return ctx.state==='running'?ctx:null});return audioResumePromise}`
- `L219: function startCue(){if(!cfg.sound)return;duckMusic(.42,.52);tone(392,.055,'square',.055,'sfx',0);tone(523.25,.08,'square',.075,'sfx',.08);tone(659.25,.09,'square',.083,'sfx',.17);tone(783.99,.16,'square',.09,'sfx',.28);tone(130.81,.28,'triangle',.05,'sfx',.28)}`
- `L222: function beginRunAudio(withCue=true){if(!cfg.sound)return;let token=++runAudioToken,ctx=ensureAudio();if(!ctx)return;resumeAudio().then(ok=>{if(!ok||token!==runAudioToken||state!=='play'||!cfg.sound)return;if(withCue)startCue();setTimeout(()=>{if(token===runAudioToken&&state==='play'&&cfg.sound)music()},withCue?430:0)})}`
- `L223: function unlockAudioFromGesture(){if(!cfg.sound)return;resumeAudio().then(ok=>{if(ok&&state==='play'&&!seqTimer)music(musicKind||'normal')})}`
- `L236: function music(kind='normal'){if(seqTimer){clearTimeout(seqTimer);seqTimer=null}let token=++musicToken;if(kind==='off'||!cfg.sound)return;musicKind=kind;musicStep=0;let ctx=ensureAudio();if(!ctx)return;if(ctx.state==='running')scheduleMusic(token);else resumeAudio().then(ok=>{if(ok&&token===musicToken&&cfg.sound&&state==='play')scheduleMusic(token)})}`
- `L239: let input={x:0,y:1,keys:{},jump:false,trick:false,gpj:false,gpp:false},state='menu',world=[],snow=[],fx=[],trail=[],marks=[],santa=null,ufo=null,beast=null,deathCrash=null,nextSanta=210,nextUfo=95,mode='survival',time=0,dist=0,score=0,style=0,gates=0,miss=0,cam=0,shake=0,buried=0,life=100,timeLimit=60,terrainNotice=0;`
- `L298: addEventListener('keydown',e=>{input.keys[e.code]=true;if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space'].includes(e.code))e.preventDefault();if(e.code==='Escape')pause();if(e.code==='F2'&&state==='play')reset(mode);if(e.code==='KeyH')$('#hud').classList.toggle('hidden')});addEventListener('keyup',e=>input.keys[e.code]=false);`
- `L299: cv.addEventListener('mousemove',e=>{if(state!=='play')return;let r=cv.getBoundingClientRect(),sx=(e.clientX-r.left)/r.width*W,sy=(e.clientY-r.top)/r.height*H,m=screenToWorld(sx,sy);input.x=clamp((m.x-p.x)/92,-1,1);input.y=clamp((m.y-p.y)/115,-1,1);pointerSteerUntil=performance.now()+320});cv.oncontextmenu=e=>e.preventDefault();`
- `L393: function pause(){if(state==='play'){state='pause';show('#pauseScreen');updateModeHud();music('off')}else if(state==='pause'){state='play';$$('.screen').forEach(x=>x.classList.add('hidden'));updateModeHud();music()}}`
- `L394: function finish(reason='life'){if(state==='over'||state==='ending')return;fadeToGameOver(reason)}`
**Gameplay tuning signals**
- `L105: const IS_MOBILE=matchMedia('(pointer: coarse)').matches,MIN_ZOOM=IS_MOBILE?.32:.34,MAX_ZOOM=1,MAX_RADIUS=600,DEBUG_CAMERA=false,MAX_SPAWN_PER_UPDATE=IS_MOBILE?4:7,MAX_ENTITIES=IS_MOBILE?125:170,MAX_PARTICLES=IS_MOBILE?280:450,MAX_MARKS=IS_MOBILE?220:350,MAX_TRAIL=500;`
- `L106: const camera={x:W/2,y:H/2,zoom:1,targetZoom:1,impactZoom:1,growthZoom:1,lookAheadX:0,offsetY:30,finalZoom:1,bounds:null};`
- `L107: const CHUNK_WIDTH=720,CHUNK_HEIGHT=620,MAX_CHUNKS_GENERATED_PER_UPDATE=IS_MOBILE?1:2,REBASE_DISTANCE=50000,WORLD_SEED=0x5a17c9d3;`
- `L110: const deluxe={weather:'clear',weatherStrength:0,targetWeatherStrength:0,lastBiome:'alpine',combo:0,comboTimer:0,bestCombo:0,variety:new Set(),districtScore:0,eventBonus:0,wind:0,oneShotBiome:true};`
- `L115: function updateCombo(type,value){deluxe.combo=Math.min(99,deluxe.combo+1);deluxe.comboTimer=2.8;deluxe.bestCombo=Math.max(deluxe.bestCombo,deluxe.combo);deluxe.variety.add(type);let varietyBonus=Math.min(2.5,1+deluxe.variety.size*.08),multi=1+Math.min(3,deluxe.combo*.035);return Math.round(value*varietyBonus*multi)}`
- `L130: if(b==='frozen')return r<.24?'penguin':r<.37?'bear':r<.43?'yeti':r<.54?'rock':r<.65?'snowman':r<.74?'iceRink':r<.82?'eskimoVillage':r<.90?'dogSledHunter':r<.97?'snowPlow':'waterTower';`
- `L131: if(b==='industrial')return r<.13?'warehouse':r<.24?'factory':r<.33?'garage':r<.42?'parking':r<.50?'train':r<.57?'maintenance':r<.64?'snowPlow':r<.71?'fireTruck':r<.77?'snowmobile':r<.84?'waterTower':r<.90?'billboard':r<.96?'powerPlant':r<.985?'villager':'monsterTruck';`
- `L137: const STRUCTURE_COMBO_WINDOW=2.2;let structureCombo={count:0,lastAt:-99,expires:0,mult:1,best:0,lastTier:0};`
- `L148: function featureEntity(chunk,type,x,y,extra={}){let st=OBJECT_STATS[type]||[10,10];return pushChunkEntity(chunk,{type,x,y,w:st[0]*1.2,h:st[0],size:st[0],value:st[1],variant:0,phase:0,hit:false,gone:false,chunkKey:chunk.key,biome:chunk.biome,material:materialFor(type),hp:1,maxHp:1,...extra})}`
- `L151: function makeRiverPoints(random,height=CHUNK_HEIGHT*1.18,turns=7){let pts=[],phase=random()*TAU,amp=35+random()*90,drift=(random()-.5)*60;for(let i=0;i<turns;i++){let t=i/(turns-1),yy=-height/2+t*height,xx=Math.sin(phase+t*(2.2+random()*2.2)*Math.PI)*amp+(t-.5)*drift;pts.push([xx,yy])}return pts}`
- `L163: function canOverrun(e){if(!e||e.terrainHazard||e.decorative)return false;let ballSpan=Math.max(p.r,p.targetR*.96)*2,objectSpan=Math.max(4,e.size||Math.max(e.w||0,e.h||0)*.5),need=overrunRequirement(e);return ballSpan>=objectSpan*need}`
- `L164: function overrunImpact(e){let beforeSpeed=p.speed,beforeMass=p.mass;bury(e);p.speed=Math.max(beforeSpeed,p.speed,p.speedPeak||0);p.speedPeak=Math.max(p.speedPeak||0,p.speed);p.vx*=.985;camera.impactZoom=Math.max(camera.impactZoom,.985);shake=Math.min(shake,Math.max(1.2,(e.size||8)*.035));return p.mass>beforeMass}`
- `L167: function clamp(v,a,b){return Math.max(a,Math.min(b,v))}function lerp(a,b,t){return a+(b-a)*clamp(t,0,1)}`
- `L168: function radiusFromMass(mass){let raw=Math.sqrt(Math.max(0,mass));if(raw<=80)return raw;if(raw<=160)return 80+(raw-80)*.7;return Math.min(MAX_RADIUS,136+(raw-160)*.45)}`
- `L169: function calculateTargetZoom(r){let z;if(r<=40)z=1;else if(r<=75)z=lerp(1,.9,(r-40)/35);else if(r<=130)z=lerp(.9,.79,(r-75)/55);else if(r<=180)z=lerp(.79,.70,(r-130)/50);else if(r<=300)z=lerp(.70,.58,(r-180)/120);else if(r<=450)z=lerp(.58,.46,(r-300)/150);else z=lerp(.46,IS_MOBILE?.35:.37,(r-450)/150);return clamp(z,MIN_ZOOM,MAX_ZOOM)}`
- `L173: function getTargetEntityCount(){let factor=1/(camera.zoom*camera.zoom),raw=46*DIFF[cfg.dif].density*Math.min(2.8,factor);return clamp(Math.round(raw),40,MAX_ENTITIES)}`
- `L204: const PREVIEW=new URLSearchParams(location.search).get('preview')==='1',GAME_ID='snowball_avalanche',SHARED_STATS='ppg_minigames_stats_v1';let statActive=false,statLast=performance.now();`
- `L208: function flushShared(){if(PREVIEW||!statActive)return;let now=performance.now(),delta=Math.min(10,Math.max(0,(now-statLast)/1000));statLast=now;if(delta<.05)return;let all=sharedRead(),s=all[GAME_ID]||{};s.totalSeconds=(s.totalSeconds||0)+delta;all[GAME_ID]=s;sharedWrite(all)}`
- `L213: let ac,seqTimer=null,musicToken=0,musicStep=0,musicKind='normal',noiseBuffer=null,windBuffer=null,crowdAudioTimer=0,windAudioTimer=0,bgmBus=null,bgmTone=null,sfxBus=null,masterBus=null,masterComp=null,audioResumePromise=null,runAudioToken=0,musicRecoveryCooldown=0,lastMusicBeat=0;const MUSIC_GAIN=2.52;`
- `L216: function duckMusic(amount=.58,duration=.34){let ctx=ensureAudio();if(!ctx||!bgmBus)return;let now=ctx.currentTime,target=Math.max(.24,Math.min(1.06,amount));bgmBus.gain.cancelScheduledValues(now);bgmBus.gain.setTargetAtTime(target,now,.025);bgmBus.gain.setTargetAtTime(1.06,now+Math.max(.08,duration),.08)}`
- `L236: function music(kind='normal'){if(seqTimer){clearTimeout(seqTimer);seqTimer=null}let token=++musicToken;if(kind==='off'||!cfg.sound)return;musicKind=kind;musicStep=0;let ctx=ensureAudio();if(!ctx)return;if(ctx.state==='running')scheduleMusic(token);else resumeAudio().then(ok=>{if(ok&&token===musicToken&&cfg.sound&&state==='play')scheduleMusic(token)})}`
- `L237: const DIFF={easy:{base:126,density:.78,beast:66,accel:.62,lifeLoss:.82},normal:{base:148,density:1,beast:79,accel:.82,lifeLoss:1},hard:{base:170,density:1.22,beast:94,accel:1.05,lifeLoss:1.18}};`
- `L239: let input={x:0,y:1,keys:{},jump:false,trick:false,gpj:false,gpp:false},state='menu',world=[],snow=[],fx=[],trail=[],marks=[],santa=null,ufo=null,beast=null,deathCrash=null,nextSanta=210,nextUfo=95,mode='survival',time=0,dist=0,score=0,style=0,gates=0,miss=0,cam=0,shake=0,buried=0,life=100,timeLimit=60,terrainNotice=0;`
- `L241: let p={x:320,y:220,vx:0,speed:0,speedPeak:0,r:9,targetR:9,mass:81,roll:0,boost:100,growthPulse:0,trailTick:0,heading:0,rollDir:1,bloodiness:0};`
- `L245: let sessionStats=freshSessionStats(),zenHudLast=-1,endFadeTimer=0;`
- `L246: function formatDuration(sec){sec=Math.max(0,Math.floor(sec||0));let m=Math.floor(sec/60),s=sec%60;return m+':'+String(s).padStart(2,'0')}`
- `L254: function msg(s){let e=$('#msg');e.textContent=s;e.style.opacity=1;e.classList.remove('signal');void e.offsetWidth;e.classList.add('signal');clearTimeout(e.t);e.t=setTimeout(()=>{e.style.opacity=0;e.classList.remove('signal')},1000)}`
- `L262: function spawnX(size=10){let b=camera.bounds||getCameraBounds(),m=Math.max(30,size*.75);return rnd(b.left+m,b.right-m)}`

### `sudoku.html`
**Control flow signals**
- `L140: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
- `L278: function startGame(level) {`
- `L294: function resetBoard() {`
**Gameplay tuning signals**
- `L111: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L121: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L193: input.maxLength = 1;`
- `L260: top5.push({ name: playerName, time: timeTaken, difficulty });`
- `L284: timer = setInterval(updateTimer, 1000);`
- `L289: const minutes = String(Math.floor(timeElapsed / 60)).padStart(2, '0');`
- `L325: const board=baseBoard.map(row=>row.slice()),target=level==='easy'?30:level==='medium'?40:50;`
- `L326: const cells=Array.from({length:81},(_,i)=>i).sort(()=>Math.random()-.5);let removed=0,attempts=0;`
- `L328: if (removed>=target || attempts++>81) break;`
- `L330: const probe=board.map(row=>row.slice());if(sudokuSolutionCount(probe,2)===1)removed++;else board[r][c]=keep;`

### `the_worm.html`
**Control flow signals**
- `L56: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
- `L83: const modal=document.getElementById('modal'),modalBody=document.getElementById('modalBody');function openModal(html){modalBody.innerHTML=html;modal.classList.add('open')}modal.addEventListener('click',e=>{if(e.target===modal||e.target.closest('.close'))modal.classList.remove('open')});`
- `L92: function reset(){score=0;scoreEl.textContent='0';lenEl.textContent='4';timerEl.textContent='00:00';dir={x:1,y:0};queued={x:1,y:0};worm=[{x:10,y:12},{x:9,y:12},{x:8,y:12},{x:7,y:12}];prev=worm.map(p=>({...p}));food=null;special=null;poison=null;particles=[];dead=false;shake=0;flash=0;moveMs=MODES[diffEl.value].ms;spawnFood();draw(0)}`
**Gameplay tuning signals**
- `L27: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L37: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L80: const STATS='ppg_minigames_stats_v1',PREF='ppg_platform_prefs_v2',REC='ppg_records_v2_'+CFG.id;const read=(k,f)=>{try{return JSON.parse(localStorage.getItem(k))??f}catch{return f}},write=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v))}catch{}};`
- `L89: let worm=[],prev=[],dir={x:1,y:0},queued={x:1,y:0},food=null,special=null,poison=null,particles=[],running=false,dead=false,score=0,startAt=0,lastMove=0,moveMs=140,shake=0,flash=0,demo=PREVIEW,demoTick=0;`
- `L90: const MODES={calm:{ms:175,wrap:true,poison:0,speedup:2.0},groove:{ms:140,wrap:false,poison:.045,speedup:2.4},frenzy:{ms:105,wrap:false,poison:.085,speedup:2.9}};`
- `L92: function reset(){score=0;scoreEl.textContent='0';lenEl.textContent='4';timerEl.textContent='00:00';dir={x:1,y:0};queued={x:1,y:0};worm=[{x:10,y:12},{x:9,y:12},{x:8,y:12},{x:7,y:12}];prev=worm.map(p=>({...p}));food=null;special=null;poison=null;particles=[];dead=false;shake=0;flash=0;moveMs=MODES[diffEl.value].ms;spawnFood();draw(0)}`
- `L94: function formatTime(sec){sec=Math.max(0,Math.floor(sec||0));return '${String(Math.floor(sec/60)).padStart(2,'0')}:${String(sec%60).padStart(2,'0')}'}`
- `L95: function burst(x,y,color,count=18){for(let i=0;i<count;i++){let a=Math.random()*Math.PI*2,sp=50+Math.random()*160;particles.push({x:(x+.5)*C,y:(y+.5)*C,vx:Math.cos(a)*sp,vy:Math.sin(a)*sp,life:.35+Math.random()*.5,size:2+Math.random()*5,color})}}`
- `L102: function wormPoint(i,alpha){let p=worm[i],q=prev[Math.min(i,prev.length-1)]||p,px=p.x,py=p.y;if(MODES[diffEl.value].wrap){let dx=px-q.x,dy=py-q.y;if(dx>N/2)px-=N;else if(dx<-N/2)px+=N;if(dy>N/2)py-=N;else if(dy<-N/2)py+=N}let gx=q.x+(px-q.x)*alpha,gy=q.y+(py-q.y)*alpha;if(MODES[diffEl.value].wrap){gx=(gx%N+N)%N;gy=(gy%N+N)%N}return{x:(gx+.5)*C,y:(gy+.5)*C}}`
- `L104: function drawParticles(dt){for(let i=particles.length-1;i>=0;i--){let p=particles[i];p.life-=dt;p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=45*dt;ctx.globalAlpha=Math.max(0,p.life*1.7);ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(p.x,p.y,p.size,0,7);ctx.fill();if(p.life<=0)particles.splice(i,1)}ctx.globalAlpha=1}`

### `torre_de_hanoi.html`
**Control flow signals**
- `L272: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
- `L357: if (audioCtx.state === 'suspended') audioCtx.resume();`
- `L382: function startMusic() {`
- `L405: function startTimer() {`
- `L554: rod.addEventListener('click', () => chooseRod(index));`
- `L558: document.addEventListener('keydown', event => {`
- `L567: document.getElementById('newGame').addEventListener('click', setup);`
- `L569: document.getElementById('autoSolve').addEventListener('click', solveAutomatically);`
- `L571: document.getElementById('soundToggle').addEventListener('click', event => {`
- `L578: document.getElementById('musicToggle').addEventListener('click', event => {`
**Gameplay tuning signals**
- `L243: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L253: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L323: const DISK_HEIGHT = () => window.innerWidth <= 650 ? 27 : 30;`
- `L378: if (name === 'error') { tone(150, .14, 'sawtooth', .045); tone(115, .15, 'square', .025, .08); }`
- `L396: musicTimer = setInterval(tick, 620);`
- `L408: timerId = setInterval(() => { elapsed++; timerEl.textContent = formatTime(elapsed); }, 1000);`
- `L420: const minWidth = 34;`
- `L421: const available = Math.max(75, rod.clientWidth - 16);`
- `L445: timerEl.textContent = '00:00';`
- `L446: minimumEl.textContent = 2 ** numDisks - 1;`
- `L457: setTimeout(() => rodEls[index].classList.remove('invalid'), 330);`
- `L517: setTimeout(() => piece.remove(), 3300);`
- `L545: await wait(Math.max(115, 500 - numDisks * 45));`

### `tron.html`
**Control flow signals**
- `L44: function restart(){if(paused)setPaused(false);if(typeof window.PPGGameRestart==='function'){window.PPGGameRestart();return}location.reload()}`
**Gameplay tuning signals**
- `L15: const qs=new URLSearchParams(location.search);if(qs.get('preview')==='1'||qs.has('preview'))return;`
- `L25: window.setTimeout=(fn,ms,...args)=>{if(typeof fn!=='function')return nativeSetTimeout(fn,ms,...args);const run=()=>{if(paused)return nativeSetTimeout(run,50);fn(...args)};return nativeSetTimeout(run,ms)};`
- `L61: const DIRS={up:{x:0,y:-1,opp:'down'},down:{x:0,y:1,opp:'up'},left:{x:-1,y:0,opp:'right'},right:{x:1,y:0,opp:'left'}};let territory,player,ai,running=false,last=0,elapsed=0,rafId=0,powerups=[],powerSpawn=8,damageParticles=[],damageShake=0,damageFlash=0;`
- `L62: let audioCtx=null,sfxOn=true,musicOn=true,musicTimer=null,musicStep=0;const key=(x,y)=>x+','+y,inside=(x,y)=>x>=0&&x<COLS&&y>=0&&y<ROWS,idx=(x,y)=>y*COLS+x;`
- `L64: function makeRider(x,y,dir,owner,color){return{x,y,dir,owner,color,trail:[],trailSet:new Set(),alive:true,area:0,life:100,lastDamage:-99,hitCooldown:0,shieldUntil:0,boostUntil:0,moveCredit:0,powerText:'',burnUntil:0,burnDps:0,burnReason:''}}`
- `L68: function legalDirs(r){return Object.keys(DIRS).filter(d=>d!==DIRS[r.dir].opp)}function nextCell(r,d){return{x:r.x+DIRS[d].x,y:r.y+DIRS[d].y}}function isEnemyWall(r,x,y){return inside(x,y)&&territory[idx(x,y)]&&territory[idx(x,y)]!==r.owner}function isEnemyTrail(r,x,y){const op=r.owner===1?ai:player;return op.trailSet.has(key(x,y))}`
- `L72: function applyBurn(r,dt){if(!r.alive||elapsed>=r.burnUntil){r.burnDps=0;return}if(elapsed<r.shieldUntil){r.burnUntil=elapsed;return}const loss=Math.min(r.life,r.burnDps*dt);if(loss<=0)return;r.life-=loss;r.lastDamage=elapsed;if(Math.random()<dt*20)spawnDamageFx(r.x,r.y,r,.28);if(r.life<=0){r.life=0;r.alive=false;finish()}}`
- `L73: function regen(r,dt){if(!r.alive||r.life>=100||elapsed-r.lastDamage<5)return;r.life=Math.min(100,r.life+4*dt)}`
- `L76: function respawn(r){let best=null,bd=1e9;for(let y=0;y<ROWS;y+=2)for(let x=0;x<COLS;x+=2)if(territory[idx(x,y)]===r.owner){const d=Math.abs(x-r.x)+Math.abs(y-r.y);if(d<bd){bd=d;best={x,y}}}if(best){r.x=best.x;r.y=best.y;r.trail=[];r.trailSet.clear()}}`
- `L78: function spawnPower(){const types=['boost','shield','repair','pulse'];for(let tries=0;tries<80;tries++){const x=5+Math.floor(Math.random()*(COLS-10)),y=5+Math.floor(Math.random()*(ROWS-10));if(territory[idx(x,y)]===0&&!player.trailSet.has(key(x,y))&&!ai.trailSet.has(key(x,y))){powerups.push({x,y,type:types[(Math.random()*types.length)|0],ttl:18});break}}}`
- `L82: function recount(){let p=0,a=0;for(const v of territory){if(v===1)p++;else if(v===2)a++}player.area=p;ai.area=a;updateHUD()}`
- `L89: function loop(now){const dt=Math.min(.045,(now-last)/1000||0);last=now;update(dt);draw();if(running||damageParticles.length||damageFlash>0||damageShake>0)rafId=requestAnimationFrame(loop)}`
