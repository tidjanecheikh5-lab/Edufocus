# -*- coding: utf-8 -*-
"""Assemble apercus.html : les trois directions, en vrai, palette C."""
import json, pathlib

P = json.load(open('/home/claude/edufocus/points.json'))
DATA = json.dumps(P, separators=(',', ':'))

HTML = r"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>EduFocus — trois directions</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Nunito+Sans:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
:root{
  --vert:#084C33; --vert2:#0C6242; --vert0:#05341F; --or:#E5A80F;
  --sable:#FAFAF7; --papier:#FFFFFF; --encre:#0E1A15; --gris:#707A74; --trait:#E6E6E0;
  --p1:#CE3B33; --p2:#E4842F; --p3:#E5A80F; --p4:#46A56F;
  --disp:'Poppins',system-ui,sans-serif; --body:'Nunito Sans',system-ui,sans-serif;
}
[data-theme=dark]{
  --sable:#0D1512; --papier:#152019; --encre:#EAF0EC; --gris:#93A099; --trait:#243228;
  --vert:#1E8A5C; --vert2:#25A06C; --vert0:#0A3A26; --or:#F2B62C;
  --p1:#F2564C; --p2:#FA9445; --p3:#F2B62C; --p4:#4FBE83;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--body);background:var(--sable);color:var(--encre);
  -webkit-font-smoothing:antialiased;transition:background .3s,color .3s}
.wrap{max-width:1280px;margin:0 auto;padding:26px 22px 70px}
h1{font-family:var(--disp);font-size:27px;font-weight:800;letter-spacing:-.03em}
.sub{color:var(--gris);font-size:14px;margin-top:6px;line-height:1.6;max-width:70ch}
.topbar{display:flex;align-items:center;gap:14px;margin-bottom:26px;flex-wrap:wrap}
.tog{margin-inline-start:auto;display:flex;gap:2px;background:var(--trait);border-radius:99px;
  padding:3px}
.tog button{border:0;background:none;font:inherit;font-size:12px;font-weight:700;
  padding:6px 14px;border-radius:99px;cursor:pointer;color:var(--gris)}
.tog button[aria-pressed=true]{background:var(--papier);color:var(--encre);
  box-shadow:0 1px 3px rgba(0,0,0,.14)}

.opt{margin-bottom:44px;border:1px solid var(--trait);border-radius:16px;overflow:hidden;
  background:var(--papier);box-shadow:0 4px 22px rgba(0,0,0,.07)}
.opthead{display:flex;align-items:baseline;gap:12px;padding:15px 20px;flex-wrap:wrap;
  border-bottom:1px solid var(--trait)}
.optn{font-family:var(--disp);font-size:12px;font-weight:800;color:#fff;background:var(--vert);
  width:26px;height:26px;border-radius:50%;display:grid;place-items:center;flex:none}
.opth{font-family:var(--disp);font-size:19px;font-weight:700;letter-spacing:-.02em}
.optd{font-size:13px;color:var(--gris);flex:1;min-width:200px}
.risk{font-size:11px;font-weight:700;padding:4px 10px;border-radius:99px;white-space:nowrap}
.r1{background:rgba(70,165,111,.16);color:var(--p4)}
.r2{background:rgba(228,132,47,.16);color:var(--p2)}
.r3{background:rgba(206,59,51,.16);color:var(--p1)}

/* ══ 1 · ATLAS ═════════════════════════════════════════════════ */
.atlas{display:grid;grid-template-columns:1fr 1fr;min-height:430px}
.atlas-map{background:var(--sable);border-inline-end:1px solid var(--trait);padding:16px;
  display:grid;place-items:center;position:relative}
.atlas-map svg{width:100%;height:auto;max-height:400px}
.atlas-map path{stroke:var(--papier);stroke-width:2.4;cursor:pointer;transition:filter .15s}
.atlas-map path:hover{filter:brightness(1.15)}
.pin{position:absolute;transform:translate(-50%,-50%);display:flex;align-items:center;gap:4px;
  background:var(--papier);border-radius:99px;padding:2px 7px 2px 2px;
  box-shadow:0 1px 4px rgba(0,0,0,.2);font-size:9.5px;font-weight:700;white-space:nowrap}
.pin u{width:15px;height:15px;border-radius:50%;color:#fff;font-size:9px;font-weight:800;
  display:grid;place-items:center;text-decoration:none}
.atlas-side{padding:20px;overflow:auto;max-height:430px}
.eyebrow{font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
  color:var(--gris);margin-bottom:9px}
.big{font-family:var(--disp);font-size:46px;font-weight:800;letter-spacing:-.045em;
  color:var(--vert);line-height:.95}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:16px 0}
.kpis div{background:var(--sable);border:1px solid var(--trait);border-radius:10px;
  padding:10px 6px;text-align:center}
.kpis b{display:block;font-family:var(--disp);font-size:20px;font-weight:800;color:var(--vert);
  letter-spacing:-.03em}
.kpis i{display:block;font-style:normal;font-size:9px;color:var(--gris);margin-top:4px}
.rows{display:grid;gap:5px;margin-top:6px}
.row{display:grid;grid-template-columns:96px 1fr 44px;align-items:center;gap:8px;font-size:11px}
.rbar{height:13px;background:var(--trait);border-radius:3px;overflow:hidden}
.rbar i{display:block;height:100%;border-radius:3px}
.rv{text-align:right;font-weight:700;font-variant-numeric:tabular-nums}

/* ══ 2 · LE MUR ════════════════════════════════════════════════ */
.mur{padding:20px}
.murtop{display:flex;align-items:flex-end;gap:16px;flex-wrap:wrap;margin-bottom:14px}
.modes{display:flex;gap:6px;margin-inline-start:auto;flex-wrap:wrap}
.modes button{font:inherit;font-size:12px;font-weight:700;padding:8px 14px;cursor:pointer;
  border:1px solid var(--trait);background:var(--sable);color:var(--encre);border-radius:99px;
  transition:.15s}
.modes button[aria-pressed=true]{background:var(--vert);border-color:var(--vert);color:#fff}
canvas{width:100%;display:block;border-radius:12px;background:var(--sable);
  border:1px solid var(--trait)}
.murleg{display:flex;gap:16px;flex-wrap:wrap;margin-top:12px;font-size:12px;color:var(--gris)}
.murleg span{display:flex;align-items:center;gap:6px}
.murleg b{width:9px;height:9px;border-radius:50%;flex:none}
.murcap{font-size:12.5px;color:var(--gris);margin-top:10px;line-height:1.55;max-width:74ch}

/* ══ 3 · ATLAS VIVANT ══════════════════════════════════════════ */
.viv{position:relative;padding:20px}
.vivwrap{position:relative;border-radius:12px;overflow:hidden;background:var(--sable);
  border:1px solid var(--trait)}
.arname{position:absolute;inset-inline-end:18px;top:8px;font-family:var(--disp);
  font-size:78px;font-weight:800;color:var(--vert);opacity:.07;pointer-events:none;
  line-height:1;letter-spacing:-.03em}
.vivbtn{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}
.vivbtn button{font:inherit;font-size:12px;font-weight:700;padding:8px 15px;cursor:pointer;
  border:1px solid var(--vert);background:var(--vert);color:#fff;border-radius:99px}
.vivbtn button.alt{background:none;color:var(--encre);border-color:var(--trait)}
@media (max-width:820px){ .atlas{grid-template-columns:1fr} .atlas-side{max-height:none} }
</style></head><body>

<div class="wrap">
  <div class="topbar">
    <div>
      <h1>Trois directions pour EduFocus</h1>
      <p class="sub">Palette C appliquée. Tout ce que vous voyez fonctionne avec les vraies
      données : 3 653 points, un point pour 100 enfants. Testez le thème sombre en haut à droite.</p>
    </div>
    <div class="tog" role="group">
      <button data-th="light" aria-pressed="true">Clair</button>
      <button data-th="dark" aria-pressed="false">Sombre</button>
    </div>
  </div>

  <!-- 1 -->
  <div class="opt">
    <div class="opthead"><span class="optn">1</span>
      <span class="opth">Atlas</span>
      <span class="optd">La carte reste à gauche en permanence. Cliquez une wilaya : le détail
        s'ouvre à droite sans jamais perdre le pays de vue.</span>
      <span class="risk r1">2 h · risque faible</span></div>
    <div class="atlas">
      <div class="atlas-map" id="aMap"></div>
      <div class="atlas-side" id="aSide"></div>
    </div>
  </div>

  <!-- 2 -->
  <div class="opt">
    <div class="opthead"><span class="optn">2</span>
      <span class="opth">Le mur des 365 231</span>
      <span class="optd">Chaque point est 100 enfants réels. Changez de regroupement :
        les points se réorganisent sous vos yeux.</span>
      <span class="risk r2">4 h · risque moyen</span></div>
    <div class="mur">
      <div class="murtop">
        <div><div class="eyebrow">Enfants hors école formelle</div>
          <div class="big" id="murN">365 231</div></div>
        <div class="modes" id="murModes"></div>
      </div>
      <canvas id="murC" width="1600" height="640"></canvas>
      <div class="murleg" id="murLeg"></div>
      <p class="murcap" id="murCap"></p>
    </div>
  </div>

  <!-- 3 -->
  <div class="opt">
    <div class="opthead"><span class="optn">3</span>
      <span class="opth">Atlas vivant</span>
      <span class="optd">Les points migrent et se rassemblent en carte de Mauritanie.
        La densité que vous voyez est la densité réelle. Nom de la wilaya en arabe en filigrane.</span>
      <span class="risk r3">6 h · risque élevé</span></div>
    <div class="viv">
      <div class="vivwrap">
        <div class="arname" id="vivAr">كيدي ماغة</div>
        <canvas id="vivC" width="1600" height="700"></canvas>
      </div>
      <div class="vivbtn">
        <button id="vivGo">Rejouer la migration</button>
        <button class="alt" id="vivTo">Disperser</button>
      </div>
      <p class="murcap">Au chargement, les 3 653 points partent en désordre puis rejoignent
        leur wilaya. Nouakchott devient une tache dense : 660 points sur un territoire minuscule.
        C'est la concentration du besoin, montrée sans un seul chiffre.</p>
    </div>
  </div>
</div>

<script>
const P = __DATA__;
const W = P.w, H = P.h, PTS = P.pts;
const CSSV = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();

/* ── thème ─────────────────────────────────────────────────── */
document.querySelectorAll('.tog button').forEach(b => b.onclick = () => {
  document.documentElement.dataset.theme = b.dataset.th;
  document.querySelectorAll('.tog button').forEach(x =>
    x.setAttribute('aria-pressed', x === b));
  drawAtlas(); layout(MODE, true); vivDraw();
});

/* ── données wilayas ───────────────────────────────────────── */
const WIL = [
  ['Guidimakha',1,41469,'p1'],['Hodh El Charghi',2,59368,'p1'],['Hodh El Gharbi',3,43696,'p1'],
  ['Assaba',4,48134,'p2'],['Nouakchott',5,65995,'p2'],['Gorgol',6,39071,'p2'],
  ['Trarza',7,26533,'p3'],['Brakna',8,23674,'p3'],['Tagant',9,6588,'p3'],
  ['Inchiri',10,926,'p4'],['Dakhlet Nouadhibou',11,6815,'p4'],['Tiris Zemmour',12,1908,'p4'],
  ['Adrar',13,1054,'p4']];
const COLR = {1:'p1',2:'p1',3:'p1',4:'p2',5:'p2',6:'p2',7:'p3',8:'p3',9:'p3',
              10:'p4',11:'p4',12:'p4',13:'p4'};
const fr = n => n.toLocaleString('fr-FR').replace(/\u202f|\u00a0/g,' ');

/* ══ 1 · ATLAS ═════════════════════════════════════════════ */
const DEPORT={'Nouakchott':[104,556],'Inchiri':[150,468],'Dakhlet Nouadhibou':[112,388],
  'Guidimakha':[292,756],'Gorgol':[352,706],'Hodh El Gharbi':[607,678],'Assaba':[452,636],
  'Brakna':[366,600],'Trarza':[236,616]};
function drawAtlas(){
  const paths = Object.entries(P.paths).map(([k,d])=>{
    const w = WIL.find(x=>x[0]===k);
    return `<path d="${d}" fill="var(--${w?w[3]:'trait'})" data-w="${k}"></path>`;}).join('');
  const lines = Object.entries(DEPORT).map(([k,[x,y]])=>{
    const c=P.centres[k]; return c?`<line x1="${x}" y1="${y}" x2="${c[0]}" y2="${c[1]}"
      stroke="var(--gris)" stroke-width="1.6" opacity=".5"></line>`:'';}).join('');
  const pins = WIL.map(([k,r,,c])=>{
    const [x,y] = DEPORT[k]||P.centres[k];
    return `<div class="pin" data-w="${k}" style="left:${x/W*100}%;top:${y/H*100}%">
      <u style="background:var(--${c})">${r}</u>${k}</div>`;}).join('');
  document.getElementById('aMap').innerHTML =
    `<svg viewBox="0 0 ${W} ${H}">${paths}${lines}</svg>${pins}`;
  document.querySelectorAll('#aMap path,#aMap .pin').forEach(el =>
    el.onclick = () => side(el.dataset.w));
  side('Guidimakha');
}
function side(k){
  const w = WIL.find(x=>x[0]===k) || WIL[0];
  const mx = Math.max(...WIL.map(x=>x[2]));
  document.getElementById('aSide').innerHTML = `
    <div class="eyebrow">${k} · rang ${w[1]} sur 13</div>
    <div class="big">${fr(w[2])}</div>
    <p style="font-size:12.5px;color:var(--gris);margin-top:7px">
      enfants de 6 à 14 ans jamais scolarisés</p>
    <div class="kpis">
      <div><b>${w[1]}<span style="font-size:12px;color:var(--gris)">/13</span></b><i>priorité</i></div>
      <div><b>${(w[2]/365231*100).toFixed(1).replace('.',',')} %</b><i>du besoin national</i></div>
      <div><b>${Math.round(w[2]/40)}</b><i>salles de classe</i></div>
    </div>
    <div class="eyebrow" style="margin-top:16px">Les 13 wilayas</div>
    <div class="rows">${[...WIL].sort((a,b)=>b[2]-a[2]).map(([n,r,v,c])=>
      `<div class="row" style="opacity:${n===k?1:.62}">
        <span style="font-weight:${n===k?800:600};overflow:hidden;text-overflow:ellipsis;
          white-space:nowrap">${n}</span>
        <div class="rbar"><i style="width:${v/mx*100}%;background:var(--${c})"></i></div>
        <span class="rv">${fr(v)}</span></div>`).join('')}</div>`;
}

/* ══ 2 · LE MUR ════════════════════════════════════════════ */
const cv = document.getElementById('murC'), cx = cv.getContext('2d');
const N = PTS.length;
const cur = new Float32Array(N*2), tgt = new Float32Array(N*2);
let MODE = 'grille', t0 = 0, anim = null;

const MODES = {
  grille:['Tous',  "3 653 points. Un point pour 100 enfants. C'est l'échelle réelle du problème."],
  instr :['Instruction', "À gauche en or, les enfants en mahadra ou école coranique : ils apprennent, sans diplôme reconnu. À droite en rouge, ceux qui ne reçoivent aucune instruction."],
  wilaya:['Wilaya', "Les 13 wilayas, triées par nombre d'enfants. Nouakchott et Hodh El Charghi pèsent à eux seuls un tiers du total."],
  milieu:['Milieu', "Sept enfants hors école sur dix vivent à la campagne. C'est la vraie fracture : le taux y atteint 43 % contre 22 % en ville."]
};
function targets(m){
  const pad=30, w=cv.width-pad*2, h=cv.height-pad*2;
  if(m==='grille'){
    const cols=Math.ceil(Math.sqrt(N*w/h)), rows=Math.ceil(N/cols);
    const gx=w/cols, gy=Math.min(gx, h/rows);
    const ox=pad+(w-cols*gx)/2, oy=pad+(h-rows*gy)/2;
    PTS.forEach((p,i)=>{ tgt[i*2]=ox+(i%cols)*gx+gx/2; tgt[i*2+1]=oy+Math.floor(i/cols)*gy+gy/2; });
  } else if(m==='instr' || m==='milieu'){
    const key = m==='instr' ? 2 : 4;
    const A = PTS.map((p,i)=>i).filter(i=>PTS[i][key]===(m==='instr'?1:1));
    const B = PTS.map((p,i)=>i).filter(i=>PTS[i][key]!==(m==='instr'?1:1));
    [[A,pad,w*0.47],[B,pad+w*0.53,w*0.47]].forEach(([arr,x0,ww])=>{
      const cols=Math.ceil(Math.sqrt(arr.length*ww/h)), gx=ww/cols;
      const gy=Math.min(gx,h/Math.ceil(arr.length/cols));
      const oy=pad+(h-Math.ceil(arr.length/cols)*gy)/2;
      arr.forEach((idx,j)=>{ tgt[idx*2]=x0+(j%cols)*gx+gx/2;
                             tgt[idx*2+1]=oy+Math.floor(j/cols)*gy+gy/2; });
    });
  } else {
    const order=[...WIL].sort((a,b)=>b[2]-a[2]).map(x=>x[1]);
    const cw=w/order.length;
    order.forEach((rang,c)=>{
      const arr=PTS.map((p,i)=>i).filter(i=>PTS[i][3]===rang);
      const cols=Math.max(1,Math.floor(cw/7)), gx=cw/cols;
      const gy=Math.min(gx, h/Math.max(1,Math.ceil(arr.length/cols)));
      arr.forEach((idx,j)=>{ tgt[idx*2]=pad+c*cw+(j%cols)*gx+gx/2;
        tgt[idx*2+1]=cv.height-pad-Math.floor(j/cols)*gy-gy/2; });
    });
  }
}
function colorOf(i,m){
  const p=PTS[i];
  if(m==='instr') return CSSV(p[2]===1?'--or':'--p1');
  if(m==='milieu')return CSSV(p[4]===1?'--p1':'--p4');
  if(m==='wilaya')return CSSV('--'+COLR[p[3]]);
  return CSSV('--vert');
}
function paint(m){
  cx.clearRect(0,0,cv.width,cv.height);
  const groups={};
  for(let i=0;i<N;i++){ const c=colorOf(i,m); (groups[c]=groups[c]||[]).push(i); }
  for(const c in groups){ cx.fillStyle=c;
    cx.beginPath();
    for(const i of groups[c]){ cx.moveTo(cur[i*2]+2.4,cur[i*2+1]);
      cx.arc(cur[i*2],cur[i*2+1],2.4,0,6.284); }
    cx.fill(); }
}
function layout(m,instant){
  MODE=m; targets(m);
  document.querySelectorAll('#murModes button').forEach(b=>
    b.setAttribute('aria-pressed', b.dataset.m===m));
  document.getElementById('murCap').textContent=MODES[m][1];
  const L={grille:[['--vert','Un point = 100 enfants']],
    instr:[['--or','Mahadra ou école coranique · 194 075'],['--p1','Aucune instruction · 171 103']],
    milieu:[['--p1','Campagne · 7 sur 10'],['--p4','Ville · 3 sur 10']],
    wilaya:[['--p1','Priorité très élevée'],['--p2','Élevée'],['--p3','Moyenne'],['--p4','Faible']]}[m];
  document.getElementById('murLeg').innerHTML=L.map(([c,t])=>
    `<span><b style="background:var(${c})"></b>${t}</span>`).join('');
  if(instant){ for(let i=0;i<N*2;i++) cur[i]=tgt[i]; paint(m); return; }
  const from=Float32Array.from(cur); t0=performance.now();
  cancelAnimationFrame(anim);
  (function step(now){
    const k=Math.min(1,(now-t0)/900), e=1-Math.pow(1-k,3);
    for(let i=0;i<N*2;i++) cur[i]=from[i]+(tgt[i]-from[i])*e;
    paint(m);
    if(k<1) anim=requestAnimationFrame(step);
  })(t0);
}
document.getElementById('murModes').innerHTML=Object.entries(MODES).map(([k,v])=>
  `<button data-m="${k}" aria-pressed="${k==='grille'}">${v[0]}</button>`).join('');
document.querySelectorAll('#murModes button').forEach(b=>b.onclick=()=>layout(b.dataset.m));

/* ══ 3 · ATLAS VIVANT ══════════════════════════════════════ */
const vc=document.getElementById('vivC'), vx=vc.getContext('2d');
const vcur=new Float32Array(N*2), vtgt=new Float32Array(N*2);
const SC=Math.min(vc.width/W, vc.height/H)*0.94;
const OX=(vc.width-W*SC)/2, OY=(vc.height-H*SC)/2;
for(let i=0;i<N;i++){ vtgt[i*2]=OX+PTS[i][0]*SC; vtgt[i*2+1]=OY+PTS[i][1]*SC; }
function vivDraw(){
  vx.clearRect(0,0,vc.width,vc.height);
  const g={};
  for(let i=0;i<N;i++){ const c=CSSV('--'+COLR[PTS[i][3]]); (g[c]=g[c]||[]).push(i); }
  for(const c in g){ vx.fillStyle=c; vx.beginPath();
    for(const i of g[c]){ vx.moveTo(vcur[i*2]+2.1,vcur[i*2+1]);
      vx.arc(vcur[i*2],vcur[i*2+1],2.1,0,6.284); }
    vx.fill(); }
}
function vivRun(toMap){
  const from=Float32Array.from(vcur), t=performance.now();
  const dst=new Float32Array(N*2);
  if(toMap){ dst.set(vtgt); }
  else for(let i=0;i<N;i++){ dst[i*2]=Math.random()*vc.width; dst[i*2+1]=Math.random()*vc.height; }
  (function step(now){
    const k=Math.min(1,(now-t)/1500), e=1-Math.pow(1-k,3);
    for(let i=0;i<N*2;i++) vcur[i]=from[i]+(dst[i]-from[i])*e;
    vivDraw(); if(k<1) requestAnimationFrame(step);
  })(t);
}
for(let i=0;i<N;i++){ vcur[i*2]=Math.random()*vc.width; vcur[i*2+1]=Math.random()*vc.height; }
document.getElementById('vivGo').onclick=()=>vivRun(true);
document.getElementById('vivTo').onclick=()=>vivRun(false);

/* démarrage */
drawAtlas();
layout('grille', true);
setTimeout(()=>vivRun(true), 500);
</script></body></html>"""

out = pathlib.Path('/mnt/user-data/outputs/edufocus/apercus.html')
out.write_text(HTML.replace('__DATA__', DATA), encoding='utf-8')
print(f"apercus.html : {out.stat().st_size/1024:.0f} Ko · {len(P['pts'])} points")
