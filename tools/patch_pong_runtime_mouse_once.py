from pathlib import Path

p=Path('pong.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label):
    global s
    if old not in s:
        raise SystemExit(f'{label}: target not found')
    s=s.replace(old,new,1)

# Non-critical audiovisual/scoring work must never stop the physics loop.
anchor="function burst(x,y,color,n=16,sp=220){for(let i=0;i<n;i++)particles.push({x,y,vx:rnd(-sp,sp),vy:rnd(-sp,sp),life:rnd(.25,.8),max:.8,size:rnd(2,7),color})}function announce(text,sub='',color='#fff',power=1.1){msgs.push({text,sub,color,age:0,life:rnd(1.15,1.9)*power,style:(Math.random()*5)|0,rot:rnd(-.15,.15),x:W/2+rnd(-30,30),y:H/2+rnd(-45,30),seed:rnd(0,10),power})}"
new=anchor+"\nlet runtimeFaults=0;function safeFx(fn,label='fx'){try{return fn()}catch(err){runtimeFaults++;console.warn('Neon Pong non-critical '+label+' error:',err);return null}}"
rep(anchor,new,'safeFx helper')

old="function collidePaddle(b,p,dir){const nx=clamp(b.x,p.x,p.x+p.w),ny=clamp(b.y,p.y,p.y+p.h),dx=b.x-nx,dy=b.y-ny;if(dx*dx+dy*dy>b.r*b.r||Math.sign(b.vx)!==dir)return false;const local=clamp((b.y-p.y)/p.h,0,1),zone=local<1/3?0:local>2/3?2:1,perfect=!p.ghost&&Math.abs(local-.5)<.075,rel=clamp((b.y-(p.y+p.h/2))/(p.h/2),-1,1);b.base=Math.min(MAX,b.base*1.032+5.5);const out=b.base*boost(p.side),ang=rel*1.08;b.vx=Math.cos(ang)*out*-dir;b.vy=Math.sin(ang)*out+p.vy*.18;b.last=p.side;b.x=dir<0?p.x+p.w+b.r:p.x-b.r;b.pulse=.16;rally++;stats[p.side].maxRally=Math.max(stats[p.side].maxRally,rally);hitSfx(b,perfect);burst(b.x,b.y,perfect?'#ffffff':(p.side==='p1'?'#50e7ff':'#ff667a'),perfect?25:12,perfect?320:200);if(!p.ghost)zoneHit(p.side,zone,perfect,b);else score(p.side,45,'GHOST SAVE');if([10,20,30,40,50].includes(rally)){score(p.side,250+rally*12,`RALLY ${rally}`);announce(`RALLY ${rally}!`,rally>=40?'HYPER VELOCITY':rally>=20?'ARENA PEGANDO FOGO':'KEEP IT GOING',rally>=40?'#ff364f':'#7fffea',1.2)}return true}"
new="function collidePaddle(b,p,dir){const nx=clamp(b.x,p.x,p.x+p.w),ny=clamp(b.y,p.y,p.y+p.h),dx=b.x-nx,dy=b.y-ny;if(dx*dx+dy*dy>b.r*b.r||Math.sign(b.vx)!==dir)return false;const local=clamp((b.y-p.y)/p.h,0,1),zone=local<1/3?0:local>2/3?2:1,perfect=!p.ghost&&Math.abs(local-.5)<.075,rel=clamp((b.y-(p.y+p.h/2))/(p.h/2),-1,1);b.base=Math.min(MAX,Math.max(BASE,b.base*1.032+5.5));const out=b.base*boost(p.side),ang=rel*1.08;b.vx=Math.cos(ang)*out*-dir;b.vy=Math.sin(ang)*out+p.vy*.18;b.last=p.side;b.x=dir<0?p.x+p.w+b.r:p.x-b.r;b.pulse=.16;rally++;stats[p.side].maxRally=Math.max(stats[p.side].maxRally,rally);safeFx(()=>hitSfx(b,perfect),'hit sound');safeFx(()=>burst(b.x,b.y,perfect?'#ffffff':(p.side==='p1'?'#50e7ff':'#ff667a'),perfect?25:12,perfect?320:200),'hit particles');if(!p.ghost)safeFx(()=>zoneHit(p.side,zone,perfect,b),'hit scoring');else safeFx(()=>score(p.side,45,'GHOST SAVE'),'ghost scoring');if([10,20,30,40,50].includes(rally))safeFx(()=>{score(p.side,250+rally*12,`RALLY ${rally}`);announce(`RALLY ${rally}!`,rally>=40?'HYPER VELOCITY':rally>=20?'ARENA PEGANDO FOGO':'KEEP IT GOING',rally>=40?'#ff364f':'#7fffea',1.2)},'rally milestone');return true}"
rep(old,new,'safe paddle collision')

# Physics watchdog for NaN/Infinity/zero-speed corruption.
anchor2="function normalize(b){if(!b.last)return;const desired=b.base*boost(b.last),m=Math.hypot(b.vx,b.vy)||1;b.vx=b.vx/m*desired;b.vy=b.vy/m*desired}"
new2=anchor2+"function saneBall(b){return Number.isFinite(b.x)&&Number.isFinite(b.y)&&Number.isFinite(b.vx)&&Number.isFinite(b.vy)&&Number.isFinite(b.base)&&b.base>=BASE*.75&&Math.hypot(b.vx,b.vy)>40}function repairBalls(){for(const b of[...balls]){if(saneBall(b))continue;console.warn('Neon Pong repaired invalid ball state',b);if(b.primary){serve(Math.random()<.5?-1:1,BASE)}else balls=balls.filter(q=>q!==b)}}"
rep(anchor2,new2,'ball watchdog')

# Run watchdog before and after ball integration.
rep("const bd=dt*(slowmo>0?.72:1);for(const b of[...balls]){normalize(b);modifierPhysics(b,bd);",
    "repairBalls();const bd=dt*(slowmo>0?.72:1);for(const b of[...balls]){normalize(b);modifierPhysics(b,bd);",
    'watchdog before integration')
rep("snapshot();if(ball.x<-35)point('p2');else if(ball.x>W+35)point('p1')}",
    "repairBalls();snapshot();if(ball.x<-35)point('p2');else if(ball.x>W+35)point('p1')}",
    'watchdog after integration')

# Never let one transient frame exception kill requestAnimationFrame permanently.
old_loop="function loop(t){const dt=Math.min(.033,(t-last)/1000||0);last=t;update(dt);draw();requestAnimationFrame(loop)}"
new_loop="function loop(t){const dt=Math.min(.033,(t-last)/1000||0);last=t;try{update(dt)}catch(err){runtimeFaults++;console.error('Neon Pong frame update recovered:',err);safeFx(()=>repairBalls(),'frame repair')}try{draw()}catch(err){runtimeFaults++;console.error('Neon Pong frame draw recovered:',err)}requestAnimationFrame(loop)}"
rep(old_loop,new_loop,'resilient frame loop')

# Mouse follows vertical position anywhere in the browser viewport, not just over canvas.
old_events="addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()));C.addEventListener('pointermove',setPointer);C.addEventListener('pointerdown',e=>{audioInit();ac?.resume();setPointer(e)});"
new_events="addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()));window.addEventListener('pointermove',setPointer,{passive:true});C.addEventListener('pointerdown',e=>{try{audioInit();ac?.resume?.().catch?.(()=>{})}catch{}setPointer(e)});"
rep(old_events,new_events,'global pointer tracking')

# Wording so users know the mouse remains active outside the playfield.
s=s.replace("1P • W/S, ↑↓, mouse/toque • D SUPER • gamepad suportado", "1P • W/S, ↑↓, mouse em toda a janela/toque • D SUPER • gamepad suportado")
s=s.replace("<b>1P:</b> W/S, setas, mouse/toque ou gamepad.", "<b>1P:</b> W/S, setas, mouse (mesmo fora da arena, dentro da janela), toque ou gamepad.")

p.write_text(s,encoding='utf-8')
print('PONG_RUNTIME_MOUSE_PATCH_OK')
