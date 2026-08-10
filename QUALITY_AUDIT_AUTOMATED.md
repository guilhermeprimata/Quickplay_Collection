# Quickplay Collection — automated quality audit

Generated from the repository contents. Heuristics are intentionally conservative; false positives are preferable to silently missing a control path.

| Game | Platform | Native pause | Native restart | Native touch | Touch gap? | Audio | Storage | i18n signal | Bytes |
|---|---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|
| `advinhe_o_numero.html` | v1 | — | ✅ | — | ⚠️ | ✅ | ✅ | ✅ | 14662 |
| `bow_and_arrow.html` | v2 | — | — | ✅ | — | ✅ | ✅ | ✅ | 44666 |
| `campo_minado.html` | v1 | — | ✅ | — | ⚠️ | ✅ | ✅ | ✅ | 61273 |
| `click_speed.html` | v2 | — | — | ✅ | — | ✅ | ✅ | ✅ | 25047 |
| `corrida_de_cavalos.html` | v1 | — | — | — | ⚠️ | ✅ | ✅ | ✅ | 37443 |
| `dropworks.html` | none | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 142090 |
| `foguetinho.html` | v2 | — | — | ✅ | — | ✅ | ✅ | ✅ | 28948 |
| `idle_trader.html` | v1 | — | ✅ | ✅ | — | ✅ | ✅ | ✅ | 53009 |
| `jogo_da_forca.html` | v1 | — | ✅ | — | ⚠️ | ✅ | ✅ | ✅ | 57927 |
| `jogo_da_velha.html` | v1 | — | ✅ | — | ⚠️ | ✅ | ✅ | ✅ | 16730 |
| `kombo_blocks.html` | none | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 116039 |
| `leaping_into_life.html` | v2 | — | — | ✅ | — | ✅ | ✅ | ✅ | 22856 |
| `memory_genius.html` | v2 | — | ✅ | — | — | ✅ | ✅ | ✅ | 44353 |
| `pixel_bomberman.html` | v2 | — | — | — | ⚠️ | ✅ | ✅ | ✅ | 19899 |
| `pong.html` | v1 | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 25605 |
| `salve_os_gatinhos.html` | v2 | — | — | ✅ | — | ✅ | ✅ | ✅ | 27208 |
| `sudoku.html` | v1 | — | — | — | — | ✅ | ✅ | ✅ | 19776 |
| `the_worm.html` | v2 | — | — | ✅ | — | ✅ | ✅ | ✅ | 23645 |
| `torre_de_hanoi.html` | v1 | — | ✅ | — | — | ✅ | ✅ | ✅ | 32290 |
| `tron.html` | v2 | — | ✅ | ✅ | — | ✅ | ✅ | ✅ | 36039 |

## Automated findings

- Platform layer not v2: `advinhe_o_numero.html`, `campo_minado.html`, `corrida_de_cavalos.html`, `dropworks.html`, `idle_trader.html`, `jogo_da_forca.html`, `jogo_da_velha.html`, `kombo_blocks.html`, `pong.html`, `sudoku.html`, `torre_de_hanoi.html`
- No native pause signal: `advinhe_o_numero.html`, `bow_and_arrow.html`, `campo_minado.html`, `click_speed.html`, `corrida_de_cavalos.html`, `foguetinho.html`, `idle_trader.html`, `jogo_da_forca.html`, `jogo_da_velha.html`, `leaping_into_life.html`, `memory_genius.html`, `pixel_bomberman.html`, `salve_os_gatinhos.html`, `sudoku.html`, `the_worm.html`, `torre_de_hanoi.html`, `tron.html`
- No native restart/new-game signal: `bow_and_arrow.html`, `click_speed.html`, `corrida_de_cavalos.html`, `foguetinho.html`, `leaping_into_life.html`, `pixel_bomberman.html`, `salve_os_gatinhos.html`, `sudoku.html`, `the_worm.html`
- Canvas + keyboard but no native touch signal: `advinhe_o_numero.html`, `campo_minado.html`, `corrida_de_cavalos.html`, `jogo_da_forca.html`, `jogo_da_velha.html`, `pixel_bomberman.html`

## Balance/tuning candidates

These are the first numeric lines in each game touching difficulty-related concepts, to make the manual balancing pass faster.

### `advinhe_o_numero.html`
- `L12: canvas { display: block; margin: 0 auto; }`
- `L24: <p id="tempoRestante">180</p>`
- `L33: let tempoRestante = 180;`
- `L41: if (tempoRestante <= 0) {`
- `L53: const anguloFinal = (tempo / 180) * 2 * Math.PI;`
- `L98: tempoRestante = 180;`
- `L121: #ppg-toolbar{position:fixed;z-index:2147483000;top:10px;right:10px;display:flex;flex-wrap:wrap;justify-content:flex-end;gap:6px;max-width:min(92vw,620px);font-family:Inter,"Segoe UI",system-ui,sans-serif!important}`
- `L126: @media(max-width:720px){#ppg-toolbar{top:6px;right:6px}#ppg-toolbar button,#ppg-toolbar a{padding:6px 8px!important;font-size:11px!important}.ppg-card{padding:17px}}`
- `L130: const STATS_KEY='ppg_minigames_stats_v1', PREF_KEY='ppg_platform_prefs_v1', REC_KEY='ppg_records_'+CFG.id;`

### `bow_and_arrow.html`
- `L4: <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">`
- `L5: <title>Arqueiro do Vale: 10 Fases</title>`
- `L18: let W=800,H=600,DPR=1,last=performance.now(),running=false,charging=false,charge=0,score=0,combo=0,lives=12,phase=1,totalTime=0,phaseTime=35,spawnTimer=.55,bannerTime=0;`
- `L19: const LIVES_MAX=12,aim={x:600,y:250},arrows=[],targets=[],particles=[],rainDrops=[];`
- `L20: let audioOn=!PREVIEW,AC=null,musicTimer=null,musicStep=0,currentWeather=null,tripleShotTime=0,screenShake=0,lightning=0,frameErrors=0;`
- `L21: const wind={value:0,target:0,change:0};`
- `L24: balloon:{name:'Balão',points:10,r:31,hp:1,speed:25,material:'soft'},`
- `L25: bird:{name:'Pássaro',points:25,r:21,hp:1,speed:54,material:'soft'},`
- `L26: kite:{name:'Pipa',points:40,r:29,hp:1,speed:39,material:'soft'},`
- `L27: drone:{name:'Drone',points:70,r:30,hp:3,speed:28,material:'dense'},`
- `L28: ghost:{name:'Fantasma',points:85,r:27,hp:1,speed:37,material:'soft'},`
- `L29: meteor:{name:'Meteoro',points:100,r:30,hp:2,speed:60,material:'dense'},`
- `L30: saucer:{name:'Disco',points:120,r:30,hp:2,speed:50,material:'dense'},`
- `L31: rocket:{name:'Foguete',points:145,r:24,hp:2,speed:71,material:'dense'},`

### `campo_minado.html`
- `L59: min-height: 100vh;`
- `L69: max-width: 600px; /* Largura máxima para a área do jogo */`
- `L104: max-width: 100%;`
- `L122: gap: .65rem;`
- `L140: min-height: 44px;`
- `L199: max-width: 400px;`
- `L252: gap: 10px;`
- `L276: @media (max-width: 640px) {`
- `L277: .button-group { gap: .5rem; }`
- `L281: min-height: 40px;`
- `L314: gap: 2px;`
- `L316: max-width: 400px;`
- `L338: max-width: 400px;`
- `L371: <span id="bombs-left">Cocôs: 0</span>`

### `click_speed.html`
- `L4: <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">`
- `L7: :root{--bg:#090b14;--panel:#141827;--ink:#f4f6ff;--muted:#9ea7bd;--accent:#7c5cff;--hot:#ff3f7f;--mint:#48f0ca;--track:#23283b}`
- `L10: .app{width:min(760px,96vw);display:grid;gap:14px;text-align:center}.title{font-size:clamp(28px,6vw,58px);font-weight:950;letter-spacing:-.055em;margin:0;text-shadow:0 0 30px #7c5cff55}.sub{margin:-8px 0 4px;color:var(--muted)}`
- `L16: #cooldownShield{position:fixed;z-index:2147481000;left:0;right:0;bottom:0;top:var(--ppg-bar-h,48px);display:none;background:transparent;cursor:default}#cooldownShield.show{display:block}`
- `L18: @media(max-height:650px){.app{gap:8px}.title{font-size:30px}.sub{display:none}.panel{padding:8px}#clickBtn{height:140px}.result{min-height:75px;font-size:13px}}`
- `L20: <body><main class="app" id="clickApp"><h1 class="title">CLICK SPEED</h1><p class="sub">Um pequeno laboratório de caos motor.</p>`
- `L22: <section class="panel timerbox" id="timerBox"><span>DECORRIDO</span><div class="bar"><div class="barfill" id="barFill"></div></div><strong class="timebig" id="timeReadout">0.00s</strong></section>`
- `L35: function registerClick(e){if(!started)return;clickCount++;countEl.textContent=clickCount+' clique'+(clickCount===1?'':'s');particles(e,5+(clickCount%10===0?6:0));ppgTone(190+Math.min(600,clickCount*2),.018);milestone()}`
- `L37: function beginCooldown(){cooldown=true;shield.classList.add('show');const until=performance.now()+1350;function c(n){if(n<until)requestAnimationFrame(c);else{cooldown=false;shield.classList.remove('show');clickBtn.disabled=false}}requestAnimationFrame(c)}`
- `L49: .ppg-fixed-shift{max-height:calc(100dvh - var(--ppg-bar-h))!important}.ppg-tall-root{height:calc(100dvh - var(--ppg-bar-h))!important;max-height:calc(100dvh - var(--ppg-bar-h))!important}`
- `L55: const STATS_KEY='ppg_minigames_stats_v1',PREF_KEY='ppg_platform_prefs_v2',REC_KEY='ppg_records_v2_'+CFG.id;`
- `L75: function pollLife(){let v=null;try{v=null}catch{}window.PPGPlatform.setLife(v)}setInterval(pollLife,250);pollLife();syncNative(IS_PREVIEW?false:prefs.sound);`

### `corrida_de_cavalos.html`
- `L19: html, body { margin: 0; min-height: 100%; background: var(--bg); color: #fff; font-family: "Segoe UI", Arial, sans-serif; }`
- `L25: min-height: 100vh;`
- `L33: width: min(520px, 100%);`
- `L52: .menu-actions { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; }`
- `L54: #optionsPanel label { display: block; margin: 8px 0; color: #dbe2ea; }`
- `L56: #game { display: none; min-height: 100vh; padding: 18px; }`
- `L57: .game-shell { width: min(1500px, 100%); margin: 0 auto; }`
- `L58: .topbar { display: flex; align-items: center; justify-content: space-between; gap: 14px; margin-bottom: 14px; }`
- `L61: .game-grid { display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 16px; align-items: start; }`
- `L64: canvas { display: block; width: 100%; height: auto; border-radius: 10px; background: #111; }`
- `L65: .race-status { min-height: 28px; margin: 12px 3px 0; color: var(--gold); font-weight: 800; text-align: center; }`
- `L69: #horseButtons { display: grid; gap: 7px; max-height: 340px; overflow-y: auto; padding-right: 3px; }`
- `L70: .horse-button { display: grid; grid-template-columns: 27px 1fr auto; gap: 9px; align-items: center; width: 100%; padding: 10px; text-align: left; background: #303844; border: 1px solid transparent; }`
- `L76: .bet-controls { display: grid; grid-template-columns: 48px 1fr 48px; gap: 8px; align-items: center; }`

### `dropworks.html`
- `L62: const rr=Array.isArray(r)?Number(r[0]||0):Number(r||0), q=Math.max(0,Math.min(rr,Math.abs(w)/2,Math.abs(h)/2));`
- `L95: I18N[code].preview_hint=I18N[code].preview_hint||'Guide the flow, hit the target, waste as little as possible.';`
- `L97: I18N[code].objective_zero_waste=I18N[code].objective_zero_waste||'Hit every target while keeping waste low.';`
- `L115: pt:{weighted_tip:'Dica de timing',ach_heavy_weight_title:'Mira de Produção',ach_heavy_weight_desc:'Capture 250 partículas em recipientes em movimento.',material_elastic:'🟣 Elástico: Quica com muita energia'},`
- `L116: en:{weighted_tip:'Timing tip',ach_heavy_weight_title:'Production Aim',ach_heavy_weight_desc:'Catch 250 particles in moving containers.',material_elastic:'🟣 Elastic: High-energy bouncing material'},`
- `L117: es:{weighted_tip:'Consejo de timing',ach_heavy_weight_title:'Puntería de Producción',ach_heavy_weight_desc:'Captura 250 partículas en recipientes móviles.',material_elastic:'🟣 Elástico: Rebota con mucha energía'},`
- `L118: fr:{weighted_tip:'Astuce de timing',ach_heavy_weight_title:'Visée de Production',ach_heavy_weight_desc:'Capturez 250 particules dans des récipients mobiles.',material_elastic:'🟣 Élastique : Rebondit avec beaucoup d’énergie'},`
- `L119: de:{weighted_tip:'Timing-Tipp',ach_heavy_weight_title:'Produktionsziel',ach_heavy_weight_desc:'Fange 250 Partikel in bewegten Behältern.',material_elastic:'🟣 Elastisch: Springt mit hoher Energie'},`
- `L120: it:{weighted_tip:'Consiglio di timing',ach_heavy_weight_title:'Mira di Produzione',ach_heavy_weight_desc:'Cattura 250 particelle nei contenitori in movimento.',material_elastic:'🟣 Elastico: Rimbalza con molta energia'},`
- `L133: const PREF_KEY='fluxo_prefs_2026_v2', STATS_KEY='fluxo_player_stats_2026', PORTAL_STATS='ppg_minigames_stats_v1', GAME_ID='fluxo';`
- `L146: const INITIAL={unlockedLevel:1,levelResults:{},totalStars:0,perfectCount:0,currentStreak3Star:0,bestStreak3Star:0,unlockedAchievements:[],movingCatchesCount:0,materialsUsed:['water'],bestWasteRecordPct:100};`
- `L169: const m=level.containers[0]?.motion||{centerX:50,centerY:62,radiusX:28,radiusY:18,speed:.35,direction:1};`
- `L170: this.rigs=[{id:'wheel_main',type:'wheel',centerX:m.centerX,centerY:m.centerY,radiusX:m.radiusX,radiusY:m.radiusY,speed:m.speed,direction:m.direction||1}];`
- `L172: const tracks=[...new Set(level.containers.map(c=>Math.round((c.motion?.trackY??80)*10)/10))];`

### `foguetinho.html`
- `L12: #app{position:relative;width:min(100%,calc((100vh - 12px)*.72));height:min(calc(100vh - 12px),calc(100vw/0.72));aspect-ratio:0.72;border:2px solid #2a5790;border-radius:14px;overflow:hidden;background:#020716;box-shadow:0 0 36px #0b8ae955,inset 0 0 28px #000}`
- `L17: @media(max-width:420px){.logo{display:none}.top{grid-template-columns:1fr 1fr}.controls{grid-template-columns:1fr 1.35fr 1fr}.hud{padding:8px}}`
- `L33: <div class="betrow"><button id="minus" class="btn">−</button><input id="bet" type="number" min="1" step="1" value="10" aria-label="Créditos da missão"><button id="plus" class="btn">+</button></div>`
- `L47: let bank=100,best=1,playing=false,over=false,stake=0,mult=1,time=0,last=0,spawn=0,difficulty=0,shake=0,muted=false,animationId,hull=100,lastHullHit=-99,hullInvulnUntil=0,dodges=0;`
- `L49: const rocket={x:W/2,y:H-190,vx:0,vy:0,r:15,targetX:W/2,tilt:0};`
- `L53: let ac,master,musicTimer,beat=0;`
- `L56: function startMusic(){stopMusic();musicTimer=setInterval(()=>{if(!playing||muted)return;const notes=[110,138.59,164.81,220,164.81,138.59];tone(notes[beat++%notes.length],.16,'triangle',.08);if(beat%4===0)tone(55,.08,'square',.05)},220)}`
- `L59: function resetRocket(){Object.assign(rocket,{x:W/2,y:H-190,vx:0,vy:0,targetX:W/2,tilt:0})}`
- `L63: const r=Math.random();return Math.min(12,1.15+(-Math.log(1-r))*1.7)}`
- `L72: time+=dt;if(hull<100&&time-lastHullHit>5)hull=Math.min(100,hull+3*dt);mult=1+time*.115+time*time*.0018;difficulty=Math.min(1,(mult-1)/5);if(mult>=crashAt){explode('Falha crítica no propulsor!');return}`
- `L76: spawn-=dt;if(spawn<=0){spawnRock();spawn=Math.max(.24,.78-difficulty*.42)}`
- `L83: function loop(ts){const dt=Math.min(.033,(ts-last)/1000||0);last=ts;update(dt);draw();animationId=requestAnimationFrame(loop)}`
- `L100: .ppg-fixed-shift{max-height:calc(100dvh - var(--ppg-bar-h))!important}.ppg-tall-root{height:calc(100dvh - var(--ppg-bar-h))!important;max-height:calc(100dvh - var(--ppg-bar-h))!important}`
- `L105: const STATS_KEY='ppg_minigames_stats_v1',PREF_KEY='ppg_platform_prefs_v2',REC_KEY='ppg_records_v2_'+CFG.id;`

### `idle_trader.html`
- `L5: <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>`
- `L16: display:flex; flex-direction:column; gap:8px;`
- `L19: display:flex; align-items:center; justify-content:space-between; gap:12px;`
- `L23: header .stat{display:flex; gap:12px; flex-wrap:wrap; align-items:center}`
- `L28: .controls{display:flex; gap:10px; align-items:center; flex-wrap:wrap}`
- `L30: display:inline-flex; align-items:center; gap:6px; padding:6px 10px; border:2px solid #203060; border-radius:6px;`
- `L34: main{flex:1; display:flex; gap:10px; padding:10px; min-height:0}`
- `L37: background:#0006; border:1px solid #13224b; border-radius:8px; overflow:hidden; min-height:240px;`
- `L42: width:auto; height:auto; max-width:100%; max-height:100%;`
- `L53: aside{ width:390px; min-width:280px; max-width:95vw; display:flex; flex-direction:column; gap:10px; }`
- `L55: background:var(--panel); border:1px solid #1b2550; border-radius:8px; padding:10px; overflow:auto; min-height:0;`
- `L59: display:grid; grid-template-columns:1fr auto; gap:8px; align-items:center;`
- `L64: .btnRow{display:flex; gap:6px; flex-wrap:wrap; justify-content:flex-end}`
- `L70: .footerRow{display:flex; gap:8px; flex-wrap:wrap; justify-content:space-between; align-items:center}`

### `jogo_da_forca.html`
- `L33: min-height: 100vh;`
- `L42: gap: 20px;`
- `L76: max-width: 800px;`
- `L78: gap: 5px;`
- `L87: min-width: 30px;`
- `L123: max-width: 90%;`
- `L131: gap: 10px;`
- `L154: max-width: 100%;`
- `L185: @media (max-width: 600px) {`
- `L194: min-width: 25px;`
- `L219: @media (max-width: 400px) {`
- `L221: gap: 3px;`
- `L227: min-width: 22px;`
- `L231: gap: 5px;`

### `jogo_da_velha.html`
- `L45: @media(max-height:560px){.top5{display:none}#gameCanvas{width:min(400px,calc(100vw - 20px),calc(100dvh - var(--fitbar) - 135px))}}`
- `L52: <p>Tempo: <span id="timer">0</span>s</p>`
- `L53: <p>Pontuação: <span id="score">0</span></p>`
- `L68: let score = 0;`
- `L69: let timer = 0;`
- `L146: score += 10;`
- `L171: timer = 0;`
- `L184: localStorage.setItem("bbvelha_scores", JSON.stringify(scores.slice(0, 5)));`
- `L204: #ppg-toolbar{position:fixed;z-index:2147483000;top:10px;right:10px;display:flex;flex-wrap:wrap;justify-content:flex-end;gap:6px;max-width:min(92vw,620px);font-family:Inter,"Segoe UI",system-ui,sans-serif!important}`
- `L209: @media(max-width:720px){#ppg-toolbar{top:6px;right:6px}#ppg-toolbar button,#ppg-toolbar a{padding:6px 8px!important;font-size:11px!important}.ppg-card{padding:17px}}`
- `L213: const STATS_KEY='ppg_minigames_stats_v1', PREF_KEY='ppg_platform_prefs_v1', REC_KEY='ppg_records_'+CFG.id;`

### `kombo_blocks.html`
- `L5: <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">`
- `L19: @media(max-height:620px) and (min-width:721px){.subtitle{display:none}.titlebar{height:32px}.gameLayout{grid-template-columns:150px minmax(220px,280px) 160px}.card{padding:7px}.boardWrap{max-height:calc(100dvh - var(--bar-h) - 48px)}}`
- `L25: <main class="app"><div class="shell"><div class="titlebar"><div class="logoMark">K</div><div><h1>Kombo Blocks</h1><div class="subtitle" data-i18n="appSubtitle"></div></div></div>`
- `L54: let settings=load('kombo_blocks_settings_v2',DEFAULTS);settings={...DEFAULTS,...settings};let playerName=localStorage.getItem('kombo_blocks_player_name')||'';`
- `L74: function dropInterval(){let base=settings.difficulty==='easy'?1100:settings.difficulty==='hard'?650:900,min=settings.difficulty==='easy'?120:settings.difficulty==='hard'?30:50;return Math.max(min,Math.floor(base*Math.pow(.88,Math.max(0,stats.level-1))))}`
- `L78: function themeColor(c){if(settings.blockTheme==='colorblind'){let map={red:'#d55e00',green:'#009e73',blue:'#0072b2',yellow:'#f0e442',orange:'#e69f00',purple:'#cc79a7',cyan:'#56b4e9'};return map[c]||COLORS[c]}return COLORS[c]||'#fff'}`
- `L85: function fmtTime(s){s=Math.max(0,s|0);return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0')}`
- `L88: function registerElim(){let now=Date.now();elimTimes.push(now);elimTimes=elimTimes.filter(x=>now-x<10000);if(elimTimes.length>=2){stats.level++;toast(t('pacemaker'),'warn');audio.level();elimTimes=[]}}`
- `L95: function soft(){if(gameState!=='PLAYING'||!active)return;lastAction=Date.now();hint=null;if(!collide(active,grid,0,1)){active.y++;stats.score++;audio.move()}else lockAndContinue()}`
- `L96: function hard(){if(gameState!=='PLAYING'||!active)return;lastAction=Date.now();hint=null;let d=0;while(!collide(active,grid,0,1)){active.y++;d++}stats.score+=d*2;lockAndContinue()}`
- `L129: if(PREVIEW){settings.soundEnabled=false;settings.musicEnabled=false;settings.gameMode='classic';settings.difficulty='medium';$('#modeSelect').value='classic';$('#difficultySelect').value='medium';setTimeout(()=>startGame(false),80)}`

### `leaping_into_life.html`
- `L4: <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">`
- `L15: @media(max-height:760px){.hero p{display:none}.hero h1{font-size:clamp(21px,4.2vh,36px)}.tips{display:none}.chip{padding:5px 7px}.chip b{font-size:14px}.stage{width:min(100%,calc((100dvh - var(--bar) - 108px)*.75),540px)}}`
- `L46: function frame(now){let dt=Math.min(.035,(now-last)/1000||0);last=now;update(dt);draw(dt);requestAnimationFrame(frame)}reset();requestAnimationFrame(frame);if(PREVIEW)setTimeout(start,60);`

### `memory_genius.html`
- `L33: min-height: 100vh;`
- `L61: gap: 15px;`
- `L63: max-width: 300px;`
- `L109: gap: 10px;`
- `L139: max-width: 500px;`
- `L180: max-width: 400px;`
- `L203: gap: 10px;`
- `L208: max-width: 500px;`
- `L251: @media (max-width: 600px) {`
- `L263: gap: 10px;`
- `L272: gap: 8px;`
- `L291: @media(max-height:580px){.ranking{display:none}.game-board{width:min(300px,calc(100vw - 20px),calc(100dvh - var(--fitbar) - 165px))!important}.stats{flex-direction:row!important;gap:4px!important}}`
- `L303: <div class="stat-value" id="level">1</div>`
- `L307: <div class="stat-value" id="score">0</div>`

### `pixel_bomberman.html`
- `L8: canvas { background: #222; display: block; margin: auto; }`
- `L12: <h2>Pixel Bomberman</h2>`
- `L14: <p id="hud">Vidas: 3 | Pontos: 0</p>`
- `L26: let score = 0;`
- `L27: let lives = 3;`
- `L28: let enemyMoveTimer = 0;`
- `L29: let framesSinceDamage = 0;`
- `L105: else if (map[y][x] === "block") drawPixelArt(x, y, "#964B00", spriteBlock);`
- `L115: bombs.push({ x: player.x, y: player.y, timer: 60 });`
- `L122: { x: bomb.x + 1, y: bomb.y },`
- `L123: { x: bomb.x - 1, y: bomb.y },`
- `L124: { x: bomb.x, y: bomb.y + 1 },`
- `L125: { x: bomb.x, y: bomb.y - 1 }`
- `L130: score += 10;`

### `pong.html`
- `L5: <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">`
- `L12: #app{width:min(96vw,calc(92vh * 16 / 9),1100px);display:flex;flex-direction:column;gap:clamp(6px,1vh,12px)}`
- `L15: canvas{width:100%;height:100%;display:block;image-rendering:pixelated}`
- `L18: @media(max-height:520px){header{height:26px}.hint{display:none}.controls{height:32px}button{padding:4px 10px}#app{gap:4px;width:min(94vw,calc(82vh * 16 / 9))}}`
- `L30: const W=960,H=540,WIN=10;let state='menu',last=0,serveTimer=0,shake=0,flash=0,elapsed=0,muted=false,audio=null,musicStep=0,musicTimer=0;`
- `L32: const player={x:34,y:H/2-62,w:18,h:124,vy:0,score:0};`
- `L34: const ai={x:W-52,y:H/2-62,w:18,h:124,vy:0,score:0,target:H/2,reaction:0,mode:'recover',confidence:0,lastSeen:null,shotMemory:[0,0,0],rallyHits:0};`
- `L36: {name:'CASUAL',reaction:.19,error:58,maxSpeed:350,accel:1450,lookAhead:.75,adapt:0},`
- `L37: {name:'ESTRATEGISTA',reaction:.115,error:30,maxSpeed:445,accel:2050,lookAhead:1,adapt:.45},`
- `L38: {name:'MESTRE',reaction:.072,error:15,maxSpeed:525,accel:2700,lookAhead:1,adapt:.75}`
- `L39: ];let difficultyIndex=1;`
- `L40: const ball={x:W/2,y:H/2,r:10,vx:0,vy:0,speed:430,trail:[]};`
- `L46: function music(dt){if(muted||!audio||state!=='playing')return;musicTimer-=dt;if(musicTimer<=0){const seq=[110,0,165,0,147,0,196,220];const f=seq[musicStep++%seq.length];if(f)tone(f,.11,'triangle',.018);musicTimer=.18}}`
- `L47: function burst(x,y,color,n=12){for(let i=0;i<n;i++)particles.push({x,y,vx:rnd(-190,190),vy:rnd(-190,190),life:rnd(.25,.65),max:.65,color,size:rnd(2,6)})}`

### `salve_os_gatinhos.html`
- `L5: <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">`
- `L12: #stage{position:relative;width:min(calc(100vw - 12px),calc((100vh - 12px)*16/9));aspect-ratio:16/9;max-height:calc(100vh - 12px);overflow:hidden;border:3px solid #f8d878;border-radius:10px;box-shadow:0 0 0 3px #562d5f,0 18px 70px #000a;background:#11162d}`
- `L13: canvas{display:block;width:100%;height:100%;image-rendering:pixelated;image-rendering:crisp-edges}`
- `L14: #top{position:absolute;left:2%;right:2%;top:2%;display:flex;justify-content:space-between;align-items:flex-start;pointer-events:none;text-shadow:2px 2px #111;font-weight:900;font-size:clamp(10px,2.1vmin,20px)}`
- `L15: .pill{background:#101528d9;border:2px solid #fff4;padding:.35em .6em;border-radius:8px;box-shadow:3px 3px #0008}.lives{color:#ff819d}.combo{color:#ffd166}`
- `L16: #sound{position:absolute;right:2%;bottom:2%;width:clamp(34px,7vmin,56px);aspect-ratio:1;border:2px solid #fff;border-radius:8px;background:#20294d;color:white;font-size:clamp(16px,3vmin,24px);cursor:pointer}`
- `L25: <div id="top"><div class="pill">PONTOS <span id="score">000000</span><br><span class="combo" id="combo">COMBO x1</span></div><div class="pill lives" id="lives">♥ ♥ ♥</div></div>`
- `L36: let state='menu',score=0,lives=3,combo=1,best=0,elapsed=0,spawnTimer=1.2,shake=0,flash=0,muted=false,last=performance.now(),lastLifeLoss=-99,lifeRegenAcc=0,rescueCount=0;`
- `L38: const player={x:440,y:453,w:94,h:21,vx:0,max:430,acc:1900,drag:9};`
- `L47: function sfx(name){if(name==='catch'){tone(520,.08,'square',.16,180);tone(790,.14,'square',.1,80,.07)}if(name==='miss'){tone(150,.32,'sawtooth',.12,-80)}if(name==='spawn')tone(730,.06,'square',.05,-150)}`
- `L48: function startMusic(){if(musicTimer||!ac)return;let n=0;const notes=[220,277,330,440,330,277,247,330];musicTimer=setInterval(()=>{if(state==='play'&&!muted){tone(notes[n++%notes.length],.11,'triangle',.035);if(n%4===1)tone(110,.16,'square',.025,-20)}},240)}`
- `L50: function reset(){score=0;lives=3;combo=1;elapsed=0;spawnTimer=.8;cats=[];particles=[];player.x=433;player.vx=0;lastLifeLoss=-99;lifeRegenAcc=0;rescueCount=0;state='play';ui.overlay.classList.add('hidden');syncUI();audioOn()}`
- `L51: function syncUI(){ui.score.textContent=String(score).padStart(6,'0');ui.combo.textContent='COMBO x'+combo;ui.lives.textContent='♥ '.repeat(lives).trim()||'SEM VIDAS'}`
- `L57: function burst(x,y,color,n=10){for(let i=0;i<n;i++){const a=Math.random()*Math.PI*2,s=30+Math.random()*150;particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s-45,life:.35+Math.random()*.45,max:.8,color,size:2+Math.random()*4})}}`

### `sudoku.html`
- `L28: gap: 2px;`
- `L78: max-width: 300px;`
- `L103: @media(max-height:590px){.top-5{display:none}:root{--cell:min(40px,calc((100vw - 28px)/9.2),calc((100dvh - var(--fitbar) - 145px)/9.2))}}`
- `L116: <span id="timer">00:00</span>`
- `L150: input.maxLength = 1;`
- `L217: top5.push({ name: playerName, time: timeTaken, difficulty });`
- `L241: timer = setInterval(updateTimer, 1000);`
- `L246: const minutes = String(Math.floor(timeElapsed / 60)).padStart(2, '0');`
- `L268: // Shuffle rows and columns within each 3x3 block`
- `L277: if (level === 'easy') cellsToRemove = 20;`
- `L278: else if (level === 'medium') cellsToRemove = 40;`
- `L311: #ppg-toolbar{position:fixed;z-index:2147483000;top:10px;right:10px;display:flex;flex-wrap:wrap;justify-content:flex-end;gap:6px;max-width:min(92vw,620px);font-family:Inter,"Segoe UI",system-ui,sans-serif!important}`
- `L316: @media(max-width:720px){#ppg-toolbar{top:6px;right:6px}#ppg-toolbar button,#ppg-toolbar a{padding:6px 8px!important;font-size:11px!important}.ppg-card{padding:17px}}`
- `L320: const STATS_KEY='ppg_minigames_stats_v1', PREF_KEY='ppg_platform_prefs_v1', REC_KEY='ppg_records_'+CFG.id;`

### `the_worm.html`
- `L5: <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">`
- `L8: :root{--bar:48px;--bg:#111018;--panel:#1b1924;--panel2:#242030;--ink:#f7f1e8;--muted:#aaa0b4;--coral:#ff6b68;--mint:#73e2bd;--amber:#f0bf68;--plum:#614e72;--soil:#26201d;--line:#ffffff18}`
- `L17: @media(max-height:760px){.hero p{display:none}.hero{margin-bottom:4px}.hero h1{font-size:clamp(22px,4.5vh,38px)}.tips{display:none}.chip{padding:5px 7px}.chip b{font-size:14px}.canvas-wrap{width:min(100%,calc(100dvh - var(--bar) - 112px),720px)}}`
- `L25: <section class="hero"><div><h1>THE <span>WORM</span></h1></div><p>Uma cobrinha virou verme bioluminescente de jardim: corpo fluido, frutas, esporos perigosos e velocidade crescente.</p></section>`
- `L37: const STATS='ppg_minigames_stats_v1',PREF='ppg_platform_prefs_v2',REC='ppg_records_v2_'+CFG.id;const read=(k,f)=>{try{return JSON.parse(localStorage.getItem(k))??f}catch{return f}},write=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v))}catch{}};`
- `L46: let worm=[],prev=[],dir={x:1,y:0},queued={x:1,y:0},food=null,special=null,poison=null,particles=[],running=false,dead=false,score=0,startAt=0,lastMove=0,moveMs=140,shake=0,flash=0,demo=PREVIEW,demoTick=0;`
- `L47: const MODES={calm:{ms:175,wrap:true,poison:0,speedup:2.0},groove:{ms:140,wrap:false,poison:.045,speedup:2.4},frenzy:{ms:105,wrap:false,poison:.085,speedup:2.9}};`
- `L51: function formatTime(sec){sec=Math.max(0,Math.floor(sec||0));return '${String(Math.floor(sec/60)).padStart(2,'0')}:${String(sec%60).padStart(2,'0')}'}`

### `torre_de_hanoi.html`
- `L23: min-height: 100vh;`
- `L44: width: min(1120px, calc(100% - 24px));`
- `L65: gap: 10px;`
- `L70: label { display: grid; gap: 5px; color: var(--muted); font-size: .82rem; text-align: left; }`
- `L72: min-height: 42px;`
- `L89: gap: 1px;`
- `L95: .stat b { display: block; color: var(--accent); font-size: 1.18rem; }`
- `L101: grid-template-columns: repeat(3, minmax(0, 1fr));`
- `L102: gap: 14px;`
- `L103: min-height: 430px;`
- `L125: min-width: 0;`
- `L180: max-width: calc(100% - 16px);`
- `L217: #message { min-height: 24px; margin: 9px 0 0; color: var(--gold); font-weight: 750; }`
- `L223: @media (max-width: 650px) {`

### `tron.html`
- `L2: <html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"><title>Tron: Domínio</title>`
- `L10: <h1>TRON: DOMÍNIO</h1><p class="subtitle">Território é parede. Cauda é risco. Velocidade é uma dívida que vence rápido.</p>`
- `L18: const DIRS={up:{x:0,y:-1,opp:'down'},down:{x:0,y:1,opp:'up'},left:{x:-1,y:0,opp:'right'},right:{x:1,y:0,opp:'left'}};let territory,player,ai,running=false,last=0,elapsed=0,rafId=0,powerups=[],powerSpawn=8,damageParticles=[],damageShake=0,damageFlash=0;`
- `L19: let audioCtx=null,sfxOn=true,musicOn=true,musicTimer=null,musicStep=0;const key=(x,y)=>x+','+y,inside=(x,y)=>x>=0&&x<COLS&&y>=0&&y<ROWS,idx=(x,y)=>y*COLS+x;`
- `L21: function makeRider(x,y,dir,owner,color){return{x,y,dir,owner,color,trail:[],trailSet:new Set(),alive:true,area:0,life:100,lastDamage:-99,hitCooldown:0,shieldUntil:0,boostUntil:0,moveCredit:0,powerText:'',burnUntil:0,burnDps:0,burnReason:''}}`
- `L30: function regen(r,dt){if(!r.alive||r.life>=100||elapsed-r.lastDamage<5)return;r.life=Math.min(100,r.life+4*dt)}`
- `L33: function respawn(r){let best=null,bd=1e9;for(let y=0;y<ROWS;y+=2)for(let x=0;x<COLS;x+=2)if(territory[idx(x,y)]===r.owner){const d=Math.abs(x-r.x)+Math.abs(y-r.y);if(d<bd){bd=d;best={x,y}}}if(best){r.x=best.x;r.y=best.y;r.trail=[];r.trailSet.clear()}}`
- `L39: function recount(){let p=0,a=0;for(const v of territory){if(v===1)p++;else if(v===2)a++}player.area=p;ai.area=a;updateHUD()}`
- `L46: function loop(now){const dt=Math.min(.045,(now-last)/1000||0);last=now;update(dt);draw();if(running||damageParticles.length||damageFlash>0||damageShake>0)rafId=requestAnimationFrame(loop)}`
- `L59: .ppg-fixed-shift{max-height:calc(100dvh - var(--ppg-bar-h))!important}.ppg-tall-root{height:calc(100dvh - var(--ppg-bar-h))!important;max-height:calc(100dvh - var(--ppg-bar-h))!important}`
- `L65: const STATS_KEY='ppg_minigames_stats_v1',PREF_KEY='ppg_platform_prefs_v2',REC_KEY='ppg_records_v2_'+CFG.id;`
- `L85: function pollLife(){let v=null;try{v=(()=>{try{return player&&Number.isFinite(player.life)?player.life:null}catch{return null}})()}catch{}window.PPGPlatform.setLife(v)}setInterval(pollLife,250);pollLife();syncNative(IS_PREVIEW?false:prefs.sound);`
