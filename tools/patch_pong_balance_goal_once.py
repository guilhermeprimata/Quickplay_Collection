from pathlib import Path

p=Path('pong.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label):
    global s
    if old not in s:
        raise SystemExit(f'{label}: target not found')
    s=s.replace(old,new,1)

# 1) Tone down visual saturation while preserving the psychedelic arcade identity.
rep("function burst(x,y,color,n=16,sp=220){for(let i=0;i<n;i++)particles.push({x,y,vx:rnd(-sp,sp),vy:rnd(-sp,sp),life:rnd(.25,.8),max:.8,size:rnd(2,7),color})}function announce(text,sub='',color='#fff',power=1.1){msgs.push({text,sub,color,age:0,life:rnd(1.15,1.9)*power,style:(Math.random()*5)|0,rot:rnd(-.15,.15),x:W/2+rnd(-30,30),y:H/2+rnd(-45,30),seed:rnd(0,10),power})}",
"function burst(x,y,color,n=16,sp=220){n=Math.max(2,Math.ceil(n*.62));while(particles.length>150)particles.shift();for(let i=0;i<n;i++)particles.push({x,y,vx:rnd(-sp*.88,sp*.88),vy:rnd(-sp*.88,sp*.88),life:rnd(.22,.62),max:.62,size:rnd(2,5.5),color})}function announce(text,sub='',color='#fff',power=1.1){while(msgs.length>=4)msgs.shift();const pwr=power*.88;msgs.push({text,sub,color,age:0,life:rnd(.95,1.45)*pwr,style:(Math.random()*5)|0,rot:rnd(-.11,.11),x:W/2+rnd(-24,24),y:H/2+rnd(-34,24),seed:rnd(0,10),power:pwr})}",
'visual density')
rep("const q=m.age/m.life,inA=clamp(q/.14,0,1),outA=clamp((1-q)/.28,0,1),a=Math.min(inA,outA)*.78,boom=1+(1-inA)*1.6,fade=1+q*.16,scale=boom*fade",
"const q=m.age/m.life,inA=clamp(q/.14,0,1),outA=clamp((1-q)/.25,0,1),a=Math.min(inA,outA)*.60,boom=1+(1-inA)*1.22,fade=1+q*.10,scale=boom*fade",
'message alpha')
rep("clamp(30*m.power,20,48)","clamp(26*m.power,18,40)",'message main size')
rep("clamp(13*m.power,11,20)","clamp(12*m.power,10,17)",'message sub size')
rep("X.globalAlpha=(1-i/b.trail.length)*(.23+h*.27);","X.globalAlpha=(1-i/b.trail.length)*(.16+h*.19);",'ball trail alpha')

# 2) Rebalance AI: Strategic should be beatable/human; Master should remain genuinely difficult.
old_diffs="const seriesOptions=[1,3,5],diffs=[{name:'CASUAL',reaction:.19,error:58,max:390,accel:1750,fatigueCap:.42,fatigueRate:.0019},{name:'ESTRATEGISTA',reaction:.125,error:34,max:470,accel:2200,fatigueCap:.35,fatigueRate:.0016},{name:'MESTRE',reaction:.08,error:19,max:550,accel:2850,fatigueCap:.28,fatigueRate:.0013}];"
new_diffs="const seriesOptions=[1,3,5],diffs=[{name:'CASUAL',reaction:.22,error:68,max:370,accel:1550,fatigueCap:.52,fatigueRate:.0026,erratic:.105,drift:82},{name:'ESTRATEGISTA',reaction:.155,error:49,max:435,accel:1950,fatigueCap:.48,fatigueRate:.00235,erratic:.072,drift:65},{name:'MESTRE',reaction:.060,error:12,max:625,accel:3450,fatigueCap:.24,fatigueRate:.00095,erratic:.010,drift:24}];"
rep(old_diffs,new_diffs,'difficulty table')

old_ai="function updateAI(dt){const d=diffs[difficulty],jam=fx.p2.jam>0?1:0;p2.fatigue=clamp(p2.fatigue+dt*(d.fatigueRate+Math.min(.0007,rally*.00003)),0,d.fatigueCap);if(p2.fatigue>.2&&p2.notice<1){p2.notice=1;announce('CPU CANSANDO','REFLEXOS COMEÇAM A CAIR','#ffb34d',.8)}if(p2.fatigue>.3&&p2.notice<2){p2.notice=2;announce('CPU FATIGADA','MAIS CHANCE DE ERRO','#ff5d70',.9)}p2.reaction-=dt;if(p2.reaction<=0){p2.reaction=d.reaction*rnd(.82,1.2)*(1+p2.fatigue*1.7+jam*.35);let target=ball.vx>0?predictY(ball):H/2+(p1.score-p2.score)*6;const err=(d.error+ball.base/MAX*10+d.error*p2.fatigue*2+jam*24)*(Math.random()*2-1);if(Math.random()<p2.fatigue*.17+jam*.06)target+=rnd(-120,120);p2.target=clamp(target+err,p2.h/2+arenaTop(),arenaBottom()-p2.h/2)}const diff=p2.target-(p2.y+p2.h/2),stam=1-p2.fatigue*.34,imp=jam?.74:1,ov=fx.p2.overdrive>0?1.2:1,max=d.max*stam*imp*ov,acc=d.accel*(1-p2.fatigue*.28)*imp*ov,des=clamp(diff*6,-max,max);p2.vy+=clamp(des-p2.vy,-acc*dt,acc*dt);const old=p2.y;p2.y=clamp(p2.y+p2.vy*dt,arenaTop(),arenaBottom()-p2.h);p2.distance+=Math.abs(p2.y-old)}"
new_ai="function updateAI(dt){const d=diffs[difficulty],jam=fx.p2.jam>0?1:0;const rallyLoad=Math.min(.0011,rally*.000045);p2.fatigue=clamp(p2.fatigue+dt*(d.fatigueRate+rallyLoad),0,d.fatigueCap);if(p2.fatigue>.2&&p2.notice<1){p2.notice=1;safeFx(()=>announce('CPU CANSANDO','REFLEXOS COMEÇAM A CAIR','#ffb34d',.7),'fatigue notice')}if(p2.fatigue>.34&&p2.notice<2){p2.notice=2;safeFx(()=>announce('CPU FATIGADA','ERROS MAIS PROVÁVEIS','#ff5d70',.75),'fatigue notice')}p2.reaction-=dt;if(p2.reaction<=0){p2.reaction=d.reaction*rnd(.86,1.28)*(1+p2.fatigue*2.25+jam*.4);let target=ball.vx>0?predictY(ball):H/2+(p1.score-p2.score)*5;const fatigueErr=d.error*p2.fatigue*2.8,err=(d.error+ball.base/MAX*8+fatigueErr+jam*28)*(Math.random()*2-1);const lapseChance=d.erratic+p2.fatigue*(difficulty===2?.07:.28)+jam*.075;if(Math.random()<lapseChance){target+=rnd(-d.drift,d.drift)*(1+p2.fatigue*1.7);if(difficulty<2&&Math.random()<.28)p2.reaction+=rnd(.04,.11)}p2.target=clamp(target+err,p2.h/2+arenaTop(),arenaBottom()-p2.h/2)}const delta=p2.target-(p2.y+p2.h/2),stam=1-p2.fatigue*(difficulty===2?.22:.46),imp=jam?.76:1,ov=fx.p2.overdrive>0?1.2:1,max=d.max*stam*imp*ov,acc=d.accel*(1-p2.fatigue*(difficulty===2?.18:.40))*imp*ov,des=clamp(delta*5.6,-max,max);p2.vy+=clamp(des-p2.vy,-acc*dt,acc*dt);const old=p2.y;p2.y=clamp(p2.y+p2.vy*dt,arenaTop(),arenaBottom()-p2.h);p2.distance+=Math.abs(p2.y-old)}"
rep(old_ai,new_ai,'AI behavior')

# 3) Goal sound: punchy low impact + arcade rise + shimmer.
old_sfx="function hitSfx(b,perfect=false){const h=clamp((b.base-BASE)/(MAX-BASE),0,1),f=240+h*850+(perfect?150:0);osc(f,.045,'square',.16);osc(f*1.5,.035,'triangle',.07,.018);if(perfect)osc(f*2.05,.08,'sine',.08,.03)}function sfx(n){if(n==='power'){osc(620,.07,'square',.15);osc(930,.12,'triangle',.1,.05)}else if(n==='goal'){osc(330,.09,'square',.13);osc(495,.12,'square',.13,.07);osc(660,.15,'triangle',.08,.14)}else if(n==='shield'){osc(520,.06,'sine',.12);osc(780,.14,'sine',.1,.04)}else if(n==='super'){osc(220,.12,'sawtooth',.12);osc(440,.15,'square',.12,.07);osc(880,.2,'triangle',.09,.15)}}"
new_sfx="function hitSfx(b,perfect=false){const h=clamp((b.base-BASE)/(MAX-BASE),0,1),f=240+h*850+(perfect?150:0);osc(f,.045,'square',.16);osc(f*1.5,.035,'triangle',.07,.018);if(perfect)osc(f*2.05,.08,'sine',.08,.03)}function goalSfx(){safeFx(()=>{osc(82,.22,'sine',.20);osc(164,.12,'sawtooth',.11,.015);noiseHit(.09,.02);[392,523.25,659.25,783.99].forEach((f,i)=>osc(f,.11+i*.025,i<2?'square':'triangle',.12-i*.012,.055+i*.07));osc(1174.66,.28,'sine',.07,.31)},'goal sound')}function sfx(n){if(n==='power'){osc(620,.07,'square',.15);osc(930,.12,'triangle',.1,.05)}else if(n==='goal'){goalSfx()}else if(n==='shield'){osc(520,.06,'sine',.12);osc(780,.14,'sine',.1,.04)}else if(n==='super'){osc(220,.12,'sawtooth',.12);osc(440,.15,'square',.12,.07);osc(880,.2,'triangle',.09,.15)}}"
rep(old_sfx,new_sfx,'goal sound')

# 4) Dedicated goal freeze state with two flashes and serve from conceding side toward scorer.
rep("let state='menu',last=performance.now(),elapsed=0,serveTimer=.7,mode='ai',difficulty=1,seriesIndex=0,chaos=false,sudden=false;",
"let state='menu',last=performance.now(),elapsed=0,serveTimer=.7,mode='ai',difficulty=1,seriesIndex=0,chaos=false,sudden=false,goalPauseTimer=0,goalPending=null;",
'goal state vars')

anchor="function serve(dir=Math.random()<.5?-1:1,speed=BASE){ball=makeBall(true);balls=[ball];ball.base=speed;const a=rnd(-.48,.48);ball.vx=Math.cos(a)*speed*dir;ball.vy=Math.sin(a)*speed;serveTimer=.65;rally=0;history.length=0;triple=0;powerup=null;powerTimer=Math.max(powerTimer,rnd(4,7))}"
new_anchor=anchor+"function serveFromConceder(scorer){const loser=scorer==='p1'?'p2':'p1',dir=scorer==='p1'?-1:1;ball=makeBall(true,loser==='p2'?W-105:105,H/2+rnd(-70,70));balls=[ball];ball.base=BASE;const a=rnd(-.34,.34);ball.vx=Math.cos(a)*BASE*dir;ball.vy=Math.sin(a)*BASE;serveTimer=.28;rally=0;history.length=0;triple=0;powerup=null;powerTimer=Math.max(powerTimer,rnd(5,8));state='playing'}function beginGoalPause(scorer,willWin=false){goalPending={scorer,willWin};goalPauseTimer=.72;state='goalpause';balls.forEach(b=>{b.vx=0;b.vy=0;b.trail.length=0});safeFx(()=>sfx('goal'),'goal sfx')}"
rep(anchor,new_anchor,'serve from conceder')

old_point="function point(side){const scorer=side==='p1'?p1:p2,loser=side==='p1'?p2:p1;if(loser.shield>0){loser.shield--;stats[loser.side].shield++;score(loser.side,450,'CLUTCH SAVE');announce('EXTRA LIFE SAVED!',`${loser.side==='p1'?'P1':'P2'} NÃO PERDE O PONTO`,'#ff7ac6',1.4);sfx('shield');return afterPoint(()=>serve(side==='p1'?-1:1))}scorer.score++;stats[side].goals++;const goalPts=1400+Math.round(rally*28+ball.base*1.1+hitStreak[side]*8);score(side,goalPts,'GOAL QUALITY');hitStreak[loser.side]=0;combo[loser.side]=0;announce('GOAL!',`+${goalPts} • RALLY ${rally}`,side==='p1'?'#52e7ff':'#ff647c',1.45);sfx('goal');maybeSudden();if(scorer.score>=WIN)return afterPoint(()=>winGame(side));afterPoint(()=>serve(side==='p1'?-1:1))}"
new_point="function point(side){const scorer=side==='p1'?p1:p2,loser=side==='p1'?p2:p1;if(loser.shield>0){loser.shield--;stats[loser.side].shield++;safeFx(()=>score(loser.side,450,'CLUTCH SAVE'),'shield score');safeFx(()=>announce('EXTRA LIFE SAVED!',`${loser.side==='p1'?'P1':'P2'} NÃO PERDE O PONTO`,'#ff7ac6',1.0),'shield msg');safeFx(()=>sfx('shield'),'shield sfx');return serveFromConceder(side)}scorer.score++;stats[side].goals++;const goalPts=1400+Math.round(rally*28+ball.base*1.1+hitStreak[side]*8);safeFx(()=>score(side,goalPts,'GOAL QUALITY'),'goal score');hitStreak[loser.side]=0;combo[loser.side]=0;safeFx(()=>announce('GOAL!',`+${goalPts} • RALLY ${rally}`,side==='p1'?'#52e7ff':'#ff647c',1.12),'goal msg');maybeSudden();beginGoalPause(side,scorer.score>=WIN)}"
rep(old_point,new_point,'goal pause point')

# Goal pause advances independently of normal gameplay; nothing else updates during it.
rep("if(state==='replay'){updateReplay(dt);return}if(state==='menu'||state==='gameover'){updateAttract(dt);return}if(state!=='playing')return;",
"if(state==='replay'){updateReplay(dt);return}if(state==='menu'||state==='gameover'){updateAttract(dt);return}if(state==='goalpause'){goalPauseTimer=Math.max(0,goalPauseTimer-dt);if(goalPauseTimer<=0&&goalPending){const g=goalPending;goalPending=null;if(g.willWin)winGame(g.scorer);else serveFromConceder(g.scorer)}return}if(state!=='playing')return;",
'goal pause update')

# Two quick screen flashes during the freeze.
rep("if(state==='paused'){X.fillStyle='#020916c9';X.fillRect(0,0,W,H);pixel('PAUSADO',W/2,H/2-18,46,'center','#ffd34d');pixel('P para continuar',W/2,H/2+35,15,'center','#a8e8ff')}X.restore()}",
"if(state==='goalpause'){const f1=goalPauseTimer<.62&&goalPauseTimer>.50,f2=goalPauseTimer<.34&&goalPauseTimer>.22;if(f1||f2){X.save();X.globalAlpha=f1?.62:.48;X.fillStyle='#ffffff';X.fillRect(0,0,W,H);X.restore()}pixel('GOAL!',W/2,H/2,42,'center',goalPending?.scorer==='p1'?'#52e7ff':'#ff657b',.82)}if(state==='paused'){X.fillStyle='#020916c9';X.fillRect(0,0,W,H);pixel('PAUSADO',W/2,H/2-18,46,'center','#ffd34d');pixel('P para continuar',W/2,H/2+35,15,'center','#a8e8ff')}X.restore()}",
'goal flash draw')

p.write_text(s,encoding='utf-8')
print('PONG_BALANCE_GOAL_PATCH_OK')
