# -*- coding: utf-8 -*-
"""identite.html — 5 thèmes de couleurs et 5 logos, appliqués au vrai dashboard."""
import json, pathlib

C = json.load(open('/home/claude/edufocus/carte.json'))
CARTE = json.dumps(C, separators=(',', ':'))

HTML = r"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>EduFocus — identité visuelle</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Nunito+Sans:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Nunito Sans',system-ui,sans-serif;background:#ECEEEF;color:#181B1E;padding:24px 18px 70px;
 -webkit-font-smoothing:antialiased}
.w{max-width:1400px;margin:0 auto}
h1{font-family:'Poppins',sans-serif;font-size:27px;font-weight:800;letter-spacing:-.03em}
h2{font-family:'Poppins',sans-serif;font-size:20px;font-weight:700;margin:34px 0 14px;letter-spacing:-.02em}
.sub{color:#5F676E;font-size:14px;margin-top:6px;line-height:1.6;max-width:80ch}
.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}

.th{border-radius:14px;overflow:hidden;background:var(--pa);box-shadow:0 3px 16px rgba(0,0,0,.12);
 color:var(--en);font-size:13px}
.tag{padding:11px 15px;border-bottom:1px solid var(--tr);display:flex;align-items:baseline;gap:9px;
 flex-wrap:wrap;background:var(--pa)}
.tag b{font-family:'Poppins',sans-serif;font-size:16px;font-weight:700}
.tag em{font-style:normal;font-size:11.5px;color:var(--gr)}
.hero{padding:18px 16px 20px;text-align:center;color:#fff;position:relative;
 background:linear-gradient(165deg,var(--a2),var(--a0))}
.kick{font-size:8.5px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;opacity:.6;margin-bottom:7px}
.cnt{font-family:'Poppins',sans-serif;font-size:38px;font-weight:800;letter-spacing:-.05em;line-height:.95}
.csb{font-size:10.5px;opacity:.82;margin-top:7px}
.hero::after{content:'';position:absolute;left:0;right:0;bottom:0;height:3px;
 background:linear-gradient(90deg,var(--ec) 0 67%,var(--ma) 67% 84%,var(--ri) 84% 100%)}
.bd{background:var(--fo);padding:11px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:9px}
.card{background:var(--pa);border:1px solid var(--tr);border-radius:9px;padding:10px}
.lab{font-size:8px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;color:var(--gr);margin-bottom:8px}
svg.map{width:100%;height:auto;display:block}
svg.map path{stroke:var(--pa);stroke-width:2.6}
.leg{display:flex;flex-wrap:wrap;gap:4px 9px;margin-top:8px;font-size:8.5px;color:var(--gr)}
.leg span{display:flex;align-items:center;gap:4px}
.leg b{width:8px;height:8px;border-radius:2px;flex:none}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-bottom:9px}
.kpis div{background:var(--pa);border:1px solid var(--tr);border-radius:8px;padding:8px 4px;text-align:center}
.kpis b{display:block;font-family:'Poppins',sans-serif;font-size:16px;font-weight:800;color:var(--ac);letter-spacing:-.03em}
.kpis i{display:block;font-style:normal;font-size:7.5px;color:var(--gr);margin-top:3px}
.waffle{display:grid;grid-template-columns:repeat(20,1fr);gap:2px 3px;
 --p:url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 16'%3E%3Ccircle cx='6' cy='3.3' r='3.05'/%3E%3Cpath d='M6 7.5c3.3 0 6 2.7 6 6V16H0v-2.5c0-3.3 2.7-6 6-6z'/%3E%3C/svg%3E")}
.waffle i{display:block;aspect-ratio:12/16;background-color:var(--ec);
 -webkit-mask:var(--p) center/contain no-repeat;mask:var(--p) center/contain no-repeat}
.waffle i.m{background-color:var(--ma)}.waffle i.n{background-color:var(--ri)}
.bars{display:grid;gap:3px;margin-top:2px}
.bar{display:grid;grid-template-columns:70px 1fr 36px;align-items:center;gap:6px;font-size:8.5px}
.bn{font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bt{height:10px;background:var(--tr);border-radius:3px;overflow:hidden}
.bt i{display:block;height:100%;border-radius:3px}
.bv{text-align:right;font-weight:700}
.sw{display:flex;margin-top:9px;border-radius:6px;overflow:hidden;border:1px solid var(--tr)}
.sw div{flex:1;height:24px;display:grid;place-items:center;font-size:6.5px;font-weight:700;color:#fff;
 font-family:ui-monospace,monospace}
.note{font-size:10px;color:var(--gr);margin-top:9px;line-height:1.5}

/* ═══ LOGOS ═══ */
.logos{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}
.lg{background:#fff;border-radius:14px;box-shadow:0 3px 16px rgba(0,0,0,.1);overflow:hidden}
.lg-top{padding:26px 18px 20px;display:grid;place-items:center;gap:16px;background:#FAFAFA}
.lg-row{display:flex;align-items:center;gap:14px}
.lg-name{font-family:'Poppins',sans-serif;font-size:25px;font-weight:800;letter-spacing:-.035em;color:#0F2A1C}
.lg-name span{font-weight:600;opacity:.62}
.lg-mini{display:flex;gap:10px;align-items:center;padding-top:4px;border-top:1px solid #EEE;width:100%;
 justify-content:center;margin-top:6px}
.lg-dark{background:#12181C;padding:12px;border-radius:9px;display:grid;place-items:center}
.lg-info{padding:14px 18px 18px;border-top:1px solid #EEE}
.lg-info b{font-family:'Poppins',sans-serif;font-size:15px;font-weight:700;display:block;margin-bottom:5px}
.lg-info p{font-size:12.5px;color:#5F676E;line-height:1.55}
</style></head><body><div class="w">

<h1>Identité visuelle — 5 thèmes, 5 logos</h1>
<p class="sub">Les cinq thèmes gardent le principe acquis : l'échelle de priorité reste une <b>gradation d'une même teinte</b> (pas un feu tricolore), et une seule couleur vive est réservée aux enfants sans aucune instruction. Ce qui change, c'est la teinte dominante et son intensité.</p>

<h2>Les thèmes</h2>
<div class="grid" id="themes"></div>

<h2>Les logos</h2>
<p class="sub" style="margin-bottom:14px">Chacun est en SVG, donc net à toute taille. Montré en grand, en petit (favicon) et sur fond sombre.</p>
<div class="logos" id="logos"></div>

</div>
<script>
const C = __CARTE__;
const WIL=[['Guidimakha',1,41469],['Hodh El Charghi',2,59368],['Hodh El Gharbi',3,43696],
 ['Assaba',4,48134],['Nouakchott',5,65995],['Gorgol',6,39071],['Trarza',7,26533],['Brakna',8,23674],
 ['Tagant',9,6588],['Inchiri',10,926],['Dakhlet Nouadhibou',11,6815],['Tiris Zemmour',12,1908],['Adrar',13,1054]];
const NIV=r=>r<=3?'n1':r<=6?'n2':r<=9?'n3':'n4';
const fr=n=>n.toLocaleString('fr-FR').replace(/\u202f|\u00a0/g,' ');
const MAP=Object.entries(C.paths).map(([k,d])=>{const w=WIL.find(x=>x[0]===k);
 return `<path d="${d}" fill="var(--${w?NIV(w[1]):'tr'})"></path>`;}).join('');
let WAF='';for(let i=0;i<100;i++)WAF+=`<i class="${i<67?'':i<84?'m':'n'}"></i>`;
const TOP=[...WIL].sort((a,b)=>b[2]-a[2]).slice(0,5);

/* fo=fond pa=papier en=encre gr=gris tr=trait ac=accent a2=clair a0=sombre
   n1..n4=échelle priorité  ec=école ma=mahadra ri=aucune instruction */
const T=[
['Drapeau','le vert et l’or de Mauritanie, saturés',
 {fo:'#F4F7F3',pa:'#FFFFFF',en:'#0E1A13',gr:'#68766D',tr:'#E0E8DE',ac:'#00713C',a2:'#009150',a0:'#00532C',
  n1:'#00713C',n2:'#2E9E64',n3:'#7FC69F',n4:'#CDE8D9',ec:'#8FCBAA',ma:'#F0B310',ri:'#D62839'},
 "Le plus identitaire : ce sont exactement les couleurs du drapeau. Le vert est franc, l’or éclatant, et le rouge du drapeau sert d’alerte. Aucun jury mauritanien ne s’y trompera."],
['Sahara','sable chaud, terre cuite, turquoise d’oasis',
 {fo:'#FBF6EE',pa:'#FFFFFF',en:'#1E170F',gr:'#7A6E5E',tr:'#EBE0CE',ac:'#B85C1E',a2:'#D97428',a0:'#8C4315',
  n1:'#B85C1E',n2:'#DB8B47',n3:'#EFBB8B',n4:'#F7E0C9',ec:'#3FA79B',ma:'#E5A82E',ri:'#C0392B'},
 "Le pays vu du désert. Chaleureux et immédiatement reconnaissable ; le turquoise de l’oasis fait ressortir les enfants scolarisés."],
['Atlantique','bleu océan, turquoise, corail',
 {fo:'#F2F8FA',pa:'#FFFFFF',en:'#0C1B22',gr:'#5F757F',tr:'#DCEAF0',ac:'#046A8C',a2:'#0688B4',a0:'#034D66',
  n1:'#046A8C',n2:'#2F9BBD',n3:'#88C6DA',n4:'#D2EAF2',ec:'#57C3B0',ma:'#F2A93B',ri:'#E8543F'},
 "La côte de Nouadhibou. Vif sans être criard, très lisible en projection ; le corail attire l’œil là où il faut."],
['Henné & indigo','l’indigo de la melhfa, l’orange du henné',
 {fo:'#F6F5FA',pa:'#FFFFFF',en:'#14122B',gr:'#6B6A85',tr:'#E4E2F0',ac:'#2E2A6E',a2:'#413CA0',a0:'#1E1B4B',
  n1:'#2E2A6E',n2:'#5A54B5',n3:'#A29CE0',n4:'#DEDBF4',ec:'#8E88D6',ma:'#E0761F',ri:'#D02F5B'},
 "Le plus original des cinq : personne d’autre n’aura de l’indigo. Culturellement juste (la melhfa, le henné) et visuellement mémorable."],
['Coucher du désert','magenta, orange et or du ciel au crépuscule',
 {fo:'#FCF4F5',pa:'#FFFFFF',en:'#24101A',gr:'#7C6069',tr:'#F2DFE3',ac:'#A81E52',a2:'#C92B67',a0:'#7A1339',
  n1:'#A81E52',n2:'#D2497F',n3:'#EC9CBB',n4:'#F9DDE6',ec:'#E88C3C',ma:'#F0B928',ri:'#B32020'},
 "Le plus audacieux. Très fort à l’écran, mais le magenta peut paraître peu institutionnel pour un ministère — à choisir si vous visez l’impact avant la sobriété."]];

document.getElementById('themes').innerHTML=T.map(([nom,sous,v,note],i)=>{
 const vars=Object.entries(v).map(([k,x])=>`--${k}:${x}`).join(';');
 const sw=[v.ac,v.n2,v.n3,v.ma,v.ri];
 return `<div class="th" style="${vars}">
  <div class="tag"><b>${i+1} · ${nom}</b><em>${sous}</em></div>
  <div class="hero"><div class="kick">Mauritanie · 6 à 14 ans</div>
   <div class="cnt">365 231</div><div class="csb">n'ont jamais vu une école</div></div>
  <div class="bd">
   <div class="kpis"><div><b>33,1 %</b><i>des 6-14 ans</i></div>
    <div><b>71 %</b><i>dans 5 wilayas</i></div><div><b>47,2 %</b><i>le pire taux</i></div></div>
   <div class="two">
    <div class="card"><div class="lab">Priorité</div>
     <svg class="map" viewBox="0 0 ${C.w} ${C.h}">${MAP}</svg>
     <div class="leg"><span><b style="background:var(--n1)"></b>Très élevée</span>
      <span><b style="background:var(--n2)"></b>Élevée</span>
      <span><b style="background:var(--n3)"></b>Moyenne</span>
      <span><b style="background:var(--n4)"></b>Faible</span></div></div>
    <div><div class="card" style="margin-bottom:9px"><div class="lab">Sur 100 enfants</div>
      <div class="waffle">${WAF}</div>
      <div class="leg"><span><b style="background:var(--ec)"></b>67 école</span>
       <span><b style="background:var(--ma)"></b>17 mahadra</span>
       <span><b style="background:var(--ri)"></b>16 rien</span></div></div>
     <div class="card"><div class="lab">Les 5 plus gros besoins</div>
      <div class="bars">${TOP.map(([n,r,val])=>`<div class="bar"><span class="bn">${n}</span>
       <div class="bt"><i style="width:${val/TOP[0][2]*100}%;background:var(--${NIV(r)})"></i></div>
       <span class="bv">${fr(val)}</span></div>`).join('')}</div></div></div></div>
   <div class="sw">${sw.map(h=>`<div style="background:${h}">${h}</div>`).join('')}</div>
   <p class="note">${note}</p></div></div>`}).join('');

/* ═══ LOGOS ═══ */
const V='#00713C', OR='#F0B310', RI='#D62839', NK='#0F2A1C';
const L=[
['Le carré manquant',
 `<svg viewBox="0 0 64 64" width="__S__" height="__S__">
  <g fill="__C__">${[...Array(9)].map((_,i)=>i===4?'':
   `<rect x="${8+(i%3)*20}" y="${8+((i/3)|0)*20}" width="14" height="14" rx="3"/>`).join('')}</g>
  <rect x="28" y="28" width="14" height="14" rx="3" fill="${RI}"/></svg>`,
 "Huit carrés alignés, un seul en rouge au centre — l'enfant qu'on ne compte pas. Se lit en un dixième de seconde, fonctionne à 16 px, et raconte tout le projet sans un mot."],
['La mise au point',
 `<svg viewBox="0 0 64 64" width="__S__" height="__S__">
  <circle cx="32" cy="32" r="26" fill="none" stroke="__C__" stroke-width="5"/>
  <circle cx="32" cy="32" r="15" fill="none" stroke="__C__" stroke-width="4" opacity=".45"/>
  <circle cx="32" cy="32" r="6.5" fill="${RI}"/>
  <path d="M32 2v10M32 52v10M2 32h10M52 32h10" stroke="__C__" stroke-width="5" stroke-linecap="round"/></svg>`,
 "Un viseur : EduFocus, c'est littéralement faire la mise au point. Les cercles concentriques évoquent le ciblage territorial, le point rouge la cible atteinte. Très net en petit."],
['L\'enfant et le pays',
 `<svg viewBox="0 0 64 64" width="__S__" height="__S__">
  <circle cx="32" cy="17" r="11" fill="__C__"/>
  <path d="M32 32c11.6 0 21 9.4 21 21v9H11v-9c0-11.6 9.4-21 21-21z" fill="__C__"/>
  <circle cx="32" cy="17" r="5.4" fill="${OR}"/>
  <path d="M23 46h18M23 53h12" stroke="#fff" stroke-width="3.4" stroke-linecap="round" opacity=".9"/></svg>`,
 "La silhouette d'enfant devenue signe, avec le croissant d'or à la place du visage — clin d'œil au drapeau. Les deux lignes du corps évoquent des barres de données."],
['La barre qui monte',
 `<svg viewBox="0 0 64 64" width="__S__" height="__S__">
  <rect x="6" y="42" width="11" height="16" rx="3" fill="__C__" opacity=".32"/>
  <rect x="21" y="32" width="11" height="26" rx="3" fill="__C__" opacity=".55"/>
  <rect x="36" y="20" width="11" height="38" rx="3" fill="__C__" opacity=".8"/>
  <rect x="51" y="6" width="11" height="52" rx="3" fill="${RI}"/></svg>`,
 "L'échelle de priorité elle-même, devenue logo. Quatre barres, la dernière en rouge : c'est exactement ce que fait l'outil, classer et désigner l'urgence. Le plus sobre."],
['Le croissant d\'enfants',
 `<svg viewBox="0 0 64 64" width="__S__" height="__S__">
  <defs><mask id="mk__ID__"><rect width="64" height="64" fill="#fff"/>
   <circle cx="40" cy="30" r="21" fill="#000"/></mask></defs>
  <circle cx="30" cy="32" r="25" fill="__C__" mask="url(#mk__ID__)"/>
  <circle cx="47" cy="14" r="5.6" fill="${OR}"/>
  <circle cx="27" cy="52" r="4.6" fill="${RI}"/></svg>`,
 "Le croissant et l'étoile du drapeau, redessinés : l'étoile devient un point d'or, et un second point rouge se détache en bas — l'enfant hors du croissant. Le plus culturel."]];

document.getElementById('logos').innerHTML=L.map(([nom,svg,txt],i)=>{
 const big=svg.replace(/__S__/g,'62').replace(/__C__/g,V).replace(/__ID__/g,'a'+i);
 const small=svg.replace(/__S__/g,'26').replace(/__C__/g,V).replace(/__ID__/g,'b'+i);
 const dark=svg.replace(/__S__/g,'40').replace(/__C__/g,'#FFFFFF').replace(/__ID__/g,'c'+i);
 return `<div class="lg"><div class="lg-top">
   <div class="lg-row">${big}<div class="lg-name">Edu<span>Focus</span></div></div>
   <div class="lg-mini">${small}<span style="font-size:11px;color:#8A9199">favicon 26 px</span>
    <div class="lg-dark">${dark}</div></div></div>
  <div class="lg-info"><b>${i+1} · ${nom}</b><p>${txt}</p></div></div>`}).join('');
</script></body></html>"""

out = pathlib.Path('/mnt/user-data/outputs/edufocus/identite.html')
out.write_text(HTML.replace('__CARTE__', CARTE), encoding='utf-8')
print(f"identite.html : {out.stat().st_size/1024:.0f} Ko")
