# -*- coding: utf-8 -*-
"""themes.html — trois thèmes sobres, appliqués à la carte et au tableau de bord."""
import json, pathlib

C = json.load(open('/home/claude/edufocus/carte.json'))
CARTE = json.dumps(C, separators=(',', ':'))

HTML = r"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>EduFocus — trois thèmes sobres</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Nunito+Sans:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Nunito Sans',system-ui,sans-serif;background:#EDEEEF;padding:20px 16px 60px;
  -webkit-font-smoothing:antialiased;color:#1a1d20}
.head{max-width:1300px;margin:0 auto 22px}
.head h1{font-family:'Poppins',sans-serif;font-size:25px;font-weight:800;letter-spacing:-.03em}
.head p{font-size:14px;color:#5f676e;margin-top:7px;line-height:1.6;max-width:78ch}
.head b{color:#1a1d20}
.grid{display:grid;gap:20px;max-width:1300px;margin:0 auto;
  grid-template-columns:repeat(auto-fit,minmax(390px,1fr))}

.th{border-radius:14px;overflow:hidden;background:var(--papier);
  box-shadow:0 3px 18px rgba(0,0,0,.12);font-size:13px;color:var(--encre)}

/* ═══ A · Ardoise ═══ */
.tA{--fond:#F6F7F8;--papier:#FFFFFF;--encre:#171B1F;--gris:#6A7480;--trait:#E3E6E9;
  --acc:#123A56;--acc2:#1B5074;--acc0:#0C2739;
  --n1:#123A56;--n2:#356C90;--n3:#7DA4BE;--n4:#C4D5E0;
  --ec:#A9BDCA;--ma:#C08A2E;--ri:#A6413B}
/* ═══ B · Graphite ═══ */
.tB{--fond:#FAFAF9;--papier:#FFFFFF;--encre:#14161A;--gris:#71767E;--trait:#E5E5E3;
  --acc:#24272C;--acc2:#34383F;--acc0:#141619;
  --n1:#24272C;--n2:#565A61;--n3:#8E9298;--n4:#CBCDCF;
  --ec:#C3C6C8;--ma:#B98A3C;--ri:#A4462F}
/* ═══ C · Vert-de-gris ═══ */
.tC{--fond:#F7F8F6;--papier:#FFFFFF;--encre:#171C19;--gris:#6E7772;--trait:#E3E7E2;
  --acc:#1B4237;--acc2:#265A4A;--acc0:#102C24;
  --n1:#1B4237;--n2:#3F6E5E;--n3:#83A697;--n4:#C6D5CD;
  --ec:#A7BDB1;--ma:#B08339;--ri:#9E4038}

.tag{padding:12px 16px;border-bottom:1px solid var(--trait);display:flex;
  align-items:baseline;gap:10px;flex-wrap:wrap;background:var(--papier)}
.tag h2{font-family:'Poppins',sans-serif;font-size:16px;font-weight:700;letter-spacing:-.02em}
.tag em{font-style:normal;font-size:11.5px;color:var(--gris)}

.hero{padding:20px 18px 22px;text-align:center;color:#fff;position:relative;
  background:linear-gradient(165deg,var(--acc2),var(--acc0))}
.kick{font-size:9px;font-weight:700;letter-spacing:.19em;text-transform:uppercase;
  color:rgba(255,255,255,.55);margin-bottom:8px}
.cnt{font-family:'Poppins',sans-serif;font-size:41px;font-weight:800;letter-spacing:-.05em;
  line-height:.94}
.csb{font-size:11px;color:rgba(255,255,255,.8);margin-top:8px}
.hero::after{content:'';position:absolute;left:0;right:0;bottom:0;height:2px;
  background:linear-gradient(90deg,var(--ec) 0 67%,var(--ma) 67% 84%,var(--ri) 84% 100%)}

.bd{background:var(--fond);padding:12px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.card{background:var(--papier);border:1px solid var(--trait);border-radius:9px;padding:11px}
.lab{font-size:8.5px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;
  color:var(--gris);margin-bottom:9px}
svg.map{width:100%;height:auto;display:block}
svg.map path{stroke:var(--papier);stroke-width:2.6}
.leg{display:flex;flex-wrap:wrap;gap:5px 10px;margin-top:9px;font-size:9px;color:var(--gris)}
.leg span{display:flex;align-items:center;gap:5px}
.leg b{width:9px;height:9px;border-radius:2px;flex:none}

.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:10px}
.kpis div{background:var(--papier);border:1px solid var(--trait);border-radius:9px;
  padding:9px 5px;text-align:center}
.kpis b{display:block;font-family:'Poppins',sans-serif;font-size:18px;font-weight:800;
  color:var(--acc);letter-spacing:-.035em}
.kpis i{display:block;font-style:normal;font-size:8px;color:var(--gris);margin-top:3px}

.waffle{display:grid;grid-template-columns:repeat(20,1fr);gap:2px 3px;
  --p:url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 16'%3E%3Ccircle cx='6' cy='3.3' r='3.05'/%3E%3Cpath d='M6 7.5c3.3 0 6 2.7 6 6V16H0v-2.5c0-3.3 2.7-6 6-6z'/%3E%3C/svg%3E")}
.waffle i{display:block;aspect-ratio:12/16;background-color:var(--ec);
  -webkit-mask:var(--p) center/contain no-repeat;mask:var(--p) center/contain no-repeat}
.waffle i.m{background-color:var(--ma)} .waffle i.n{background-color:var(--ri)}

.bars{display:grid;gap:4px;margin-top:2px}
.bar{display:grid;grid-template-columns:82px 1fr 40px;align-items:center;gap:7px;font-size:9.5px}
.bn{font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bt{height:12px;background:var(--trait);border-radius:3px;overflow:hidden}
.bt i{display:block;height:100%;border-radius:3px}
.bv{text-align:right;font-weight:700;font-variant-numeric:tabular-nums}
.sw{display:flex;margin-top:10px;border-radius:6px;overflow:hidden;border:1px solid var(--trait)}
.sw div{flex:1;height:26px;display:grid;place-items:center;font-size:7px;font-weight:700;
  color:#fff;font-family:ui-monospace,monospace}
.note{font-size:10.5px;color:var(--gris);margin-top:10px;line-height:1.55}
</style></head><body>

<div class="head">
  <h1>Trois thèmes sobres</h1>
  <p>Changement important : les quatre niveaux de priorité ne sont plus rouge / orange / jaune /
  vert, mais <b>quatre intensités d'une même teinte</b> — du plus foncé au plus clair. Un niveau
  de priorité est une donnée ordonnée, une échelle graduée la représente mieux qu'une palette
  bariolée. La carte devient nettement plus calme, et le rouge reste réservé à une seule chose :
  les enfants qui ne reçoivent aucune instruction.</p>
</div>

<div class="grid" id="g"></div>

<script>
const C = __CARTE__;
const WIL = [['Guidimakha',1,41469],['Hodh El Charghi',2,59368],['Hodh El Gharbi',3,43696],
 ['Assaba',4,48134],['Nouakchott',5,65995],['Gorgol',6,39071],['Trarza',7,26533],
 ['Brakna',8,23674],['Tagant',9,6588],['Inchiri',10,926],['Dakhlet Nouadhibou',11,6815],
 ['Tiris Zemmour',12,1908],['Adrar',13,1054]];
const NIV = r => r<=3?'n1':r<=6?'n2':r<=9?'n3':'n4';
const fr = n => n.toLocaleString('fr-FR').replace(/\u202f|\u00a0/g,' ');

const MAP = Object.entries(C.paths).map(([k,d])=>{
  const w = WIL.find(x=>x[0]===k);
  return `<path d="${d}" fill="var(--${w?NIV(w[1]):'trait'})"></path>`;}).join('');
let WAF=''; for(let i=0;i<100;i++) WAF+=`<i class="${i<67?'':i<84?'m':'n'}"></i>`;
const TOP = [...WIL].sort((a,b)=>b[2]-a[2]).slice(0,5);

const T = [
 ['tA','A · Ardoise','neutres froids, échelle bleu-gris',
  ['#123A56','#356C90','#7DA4BE','#C4D5E0','#A6413B'],
  "Le plus net et le plus technique. Le bleu-ardoise n'a aucune connotation d'alerte : c'est la position sur l'échelle qui parle, pas la couleur. Le rouge ne sert plus qu'à une seule chose."],
 ['tB','B · Graphite','quasi noir et blanc, un seul accent',
  ['#24272C','#565A61','#8E9298','#CBCDCF','#A4462F'],
  "Le plus sobre des trois. La carte est en gris purs, et la seule couleur de toute la page est la rouille des enfants sans instruction. Radical, très éditorial — celui qui se remarque parce qu'il ne cherche pas à se faire remarquer."],
 ['tC','C · Vert-de-gris','le vert mauritanien, désaturé',
  ['#1B4237','#3F6E5E','#83A697','#C6D5CD','#9E4038'],
  "Garde le lien avec le drapeau, mais le vert est éteint et passé en échelle. Le compromis si vous tenez à l'ancrage national sans le côté vif de l'actuel."]
];

document.getElementById('g').innerHTML = T.map(([cls,titre,sous,hex,note])=>`
<div class="th ${cls}">
  <div class="tag"><h2>${titre}</h2><em>${sous}</em></div>
  <div class="hero">
    <div class="kick">Mauritanie · enfants de 6 à 14 ans</div>
    <div class="cnt">365 231</div>
    <div class="csb">n'ont jamais mis les pieds dans une école</div>
  </div>
  <div class="bd">
    <div class="kpis">
      <div><b>33,1 %</b><i>des enfants 6-14</i></div>
      <div><b>71 %</b><i>dans 5 wilayas</i></div>
      <div><b>47,2 %</b><i>le pire taux</i></div>
    </div>
    <div class="two">
      <div class="card">
        <div class="lab">Priorité par wilaya</div>
        <svg class="map" viewBox="0 0 ${C.w} ${C.h}">${MAP}</svg>
        <div class="leg">
          <span><b style="background:var(--n1)"></b>Très élevée</span>
          <span><b style="background:var(--n2)"></b>Élevée</span>
          <span><b style="background:var(--n3)"></b>Moyenne</span>
          <span><b style="background:var(--n4)"></b>Faible</span>
        </div>
      </div>
      <div>
        <div class="card" style="margin-bottom:10px">
          <div class="lab">Sur 100 enfants</div>
          <div class="waffle">${WAF}</div>
          <div class="leg">
            <span><b style="background:var(--ec)"></b>67 à l'école</span>
            <span><b style="background:var(--ma)"></b>17 mahadra</span>
            <span><b style="background:var(--ri)"></b>16 nulle part</span>
          </div>
        </div>
        <div class="card">
          <div class="lab">Les 5 plus gros besoins</div>
          <div class="bars">${TOP.map(([n,r,v])=>`<div class="bar">
            <span class="bn">${n}</span>
            <div class="bt"><i style="width:${v/TOP[0][2]*100}%;background:var(--${NIV(r)})"></i></div>
            <span class="bv">${fr(v)}</span></div>`).join('')}</div>
        </div>
      </div>
    </div>
    <div class="sw">${hex.map(h=>`<div style="background:${h}">${h}</div>`).join('')}</div>
    <p class="note">${note}</p>
  </div>
</div>`).join('');
</script></body></html>"""

out = pathlib.Path('/mnt/user-data/outputs/edufocus/themes.html')
out.write_text(HTML.replace('__CARTE__', CARTE), encoding='utf-8')
print(f"themes.html : {out.stat().st_size/1024:.0f} Ko")
