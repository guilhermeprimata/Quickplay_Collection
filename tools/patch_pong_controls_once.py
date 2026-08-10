from pathlib import Path

p = Path('pong.html')
s = p.read_text(encoding='utf-8')
old = """function update(dt){updateLabelsAndParticles(dt);if(state!=='playing')return;elapsed+=dt;music(dt);updatePowerups(dt);const input=(keys.has('arrowup')||keys.has('w')?-1:0)+(keys.has('arrowdown')||keys.has('s')?1:0),jam=effects.player.jam>0?.72:1,over=effects.player.overdrive>0?1.25:1,accel=2600*jam*over,max=560*jam*over;if(input){pointerTarget=null;player.vy+=input*accel*dt;player.vy*=.88}else if(pointerTarget!=null){const diff=pointerTarget-(player.y+player.h/2),desired=clamp(diff*8,-max,max),delta=clamp(desired-player.vy,-accel*dt,accel*dt);player.vy+=delta;if(Math.abs(diff)<3)player.vy*=Math.pow(.05,dt)}else player.vy*=Math.pow(.0008,dt);player.vy=clamp(player.vy,-max,max);player.y=clamp(player.y+player.vy*dt,0,H-player.h);updateAI(dt);"""
new = """function update(dt){updateLabelsAndParticles(dt);if(state!=='playing')return;elapsed+=dt;music(dt);updatePowerups(dt);
 const input=(keys.has('arrowup')||keys.has('w')?-1:0)+(keys.has('arrowdown')||keys.has('s')?1:0),jam=effects.player.jam>0?.84:1,over=effects.player.overdrive>0?1.22:1;
 // Controle desacoplado: mouse/toque segue o alvo quase imediatamente; teclado usa velocidade-alvo alta e aceleração forte.
 // Ambos preservam uma vy física para que movimento da raquete continue influenciando o ângulo da rebatida.
 const keyMax=900*jam*over,keyAccel=6800*jam*over;
 if(input){
  pointerTarget=null;
  const desired=input*keyMax,delta=clamp(desired-player.vy,-keyAccel*dt,keyAccel*dt);
  player.vy+=delta;
  player.y=clamp(player.y+player.vy*dt,0,H-player.h);
 }else if(pointerTarget!=null){
  const center=player.y+player.h/2,diff=pointerTarget-center,followRate=30*jam*over,follow=1-Math.exp(-followRate*dt);
  const oldY=player.y,nextY=clamp(player.y+diff*follow,0,H-player.h);
  player.y=nextY;
  player.vy=dt>0?clamp((nextY-oldY)/dt,-1450*jam*over,1450*jam*over):0;
  if(Math.abs(diff)<.7){player.y=clamp(pointerTarget-player.h/2,0,H-player.h);player.vy=0}
 }else{
  player.vy*=Math.exp(-11*dt);
  if(Math.abs(player.vy)<2)player.vy=0;
  player.y=clamp(player.y+player.vy*dt,0,H-player.h);
 }
 updateAI(dt);"""
if old not in s:
    raise SystemExit('Pong control block not found or already patched')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
print('PONG_CONTROL_PATCH_OK')
