const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  Header, Footer, PageNumber, LevelFormat, convertInchesToTwip } = require('docx');

const ACC='1A4A6B', ACC2='2A6B94', OR='C08A2E', GRIS='6A7480', ENCRE='171B1F';
const TRAIT='E2E6EA', PAPIER='F5F7F8', ROUGE='A6413B';
const W = 10140;

const P=(t,o={})=>new Paragraph({spacing:{after:o.after??78,line:o.line??236},
  alignment:o.align, children:Array.isArray(t)?t:[new TextRun({text:t,size:o.size??18,
  color:o.color??ENCRE,bold:o.bold,italics:o.italics})]});
const H1=t=>new Paragraph({spacing:{before:190,after:88},
  children:[new TextRun({text:t,size:24,bold:true,color:ACC})]});
const H2=t=>new Paragraph({spacing:{before:150,after:70},
  children:[new TextRun({text:t,size:19,bold:true,color:ENCRE})]});
const BUL=t=>new Paragraph({numbering:{reference:'p',level:0},
  spacing:{after:38,line:238},children:Array.isArray(t)?t:[new TextRun({text:t,size:18})]});
const ESP=(h=110)=>new Paragraph({spacing:{after:h},children:[]});

const CADRE=(lignes,c=OR)=>new Table({width:{size:W,type:WidthType.DXA},columnWidths:[W],
  borders:{top:{style:BorderStyle.SINGLE,size:1,color:TRAIT},
    bottom:{style:BorderStyle.SINGLE,size:1,color:TRAIT},
    right:{style:BorderStyle.SINGLE,size:1,color:TRAIT},
    left:{style:BorderStyle.SINGLE,size:22,color:c},
    insideHorizontal:{style:BorderStyle.NONE},insideVertical:{style:BorderStyle.NONE}},
  rows:[new TableRow({children:[new TableCell({width:{size:W,type:WidthType.DXA},
    shading:{type:ShadingType.CLEAR,fill:PAPIER,color:'auto'},
    margins:{top:120,bottom:120,left:180,right:180},children:lignes})]})]});

function TAB(head,rows,fr,opts={}){
  const cols=fr.map(f=>Math.round(W*f));
  cols[cols.length-1]=W-cols.slice(0,-1).reduce((a,b)=>a+b,0);
  const cell=(t,i,o={})=>new TableCell({width:{size:cols[i],type:WidthType.DXA},
    shading:{type:ShadingType.CLEAR,fill:o.fill??'FFFFFF',color:'auto'},
    margins:{top:48,bottom:48,left:90,right:90},
    children:[new Paragraph({spacing:{after:0,line:236},alignment:o.align,
      children:[new TextRun({text:String(t),size:16,bold:o.bold,color:o.color??ENCRE})]})]});
  const rr=[new TableRow({tableHeader:true,children:head.map((h,i)=>
    cell(h,i,{fill:ACC,bold:true,color:'FFFFFF',
      align:(opts.right||[]).includes(i)?AlignmentType.RIGHT:undefined}))})];
  rows.forEach((l,n)=>rr.push(new TableRow({children:l.map((v,i)=>cell(v,i,{
    fill:n%2?PAPIER:'FFFFFF',bold:(opts.boldCol||[]).includes(i),
    color:(opts.accent||[]).some(([r,c])=>r===n&&c===i)?ROUGE:undefined,
    align:(opts.right||[]).includes(i)?AlignmentType.RIGHT:undefined}))})));
  return new Table({width:{size:W,type:WidthType.DXA},columnWidths:cols,
    borders:{top:{style:BorderStyle.SINGLE,size:2,color:TRAIT},
      bottom:{style:BorderStyle.SINGLE,size:2,color:TRAIT},
      left:{style:BorderStyle.NONE},right:{style:BorderStyle.NONE},
      insideHorizontal:{style:BorderStyle.SINGLE,size:1,color:TRAIT},
      insideVertical:{style:BorderStyle.NONE}},rows:rr});
}

const b=[];

/* ─────────── En-tête du document ─────────── */
b.push(new Paragraph({spacing:{after:40},
  children:[new TextRun({text:'DOCUMENT DE SOLUTION',size:16,bold:true,color:GRIS,
    characterSpacing:70})]}));
b.push(new Paragraph({spacing:{after:30},
  children:[new TextRun({text:'EduFocus',size:44,bold:true,color:ACC})]}));
b.push(P('De la démographie à la décision : où investir dans l’éducation en Mauritanie.',
  {size:23,color:GRIS,after:170}));
b.push(P([new TextRun({text:'Hackathon IndabaX Mauritanie — Édition 2026   ·   ',size:17,color:GRIS}),
  new TextRun({text:'Thème : From Data to Storytelling · Population & Démographie',size:17,color:GRIS})],{after:20}));
b.push(P([new TextRun({text:'Équipe DataSphere   ·   Date : 01 / 08 / 2026',size:17,color:GRIS,bold:true})],{after:130}));

/* ─────────── 1. Problématique ─────────── */
b.push(H1('1. Problématique'));
b.push(H2('Contexte et problème identifié'));
b.push(P([new TextRun({text:'La Mauritanie est un pays très jeune : 63 % de la population a moins de 25 ans et 27 % des Mauritaniens ont entre 6 et 14 ans. Quand une population a cette structure, sa première demande à l’État n’est ni l’emploi ni la santé : ',size:18}),
  new TextRun({text:'c’est l’école.',size:18,bold:true})]));
b.push(P('Mais la démographie est déséquilibrée de deux façons opposées. La population se concentre sur Nouakchott, qui a absorbé 44 % de la croissance nationale entre 2013 et 2019. Les enfants, eux, sont ailleurs : le Gorgol compte 128 enfants de moins de 15 ans pour 100 adultes actifs, contre 63 à Nouakchott. Les wilayas qui portent la charge d’enfants la plus lourde sont aussi les plus rurales et les plus pauvres.'));
b.push(ESP(90));
b.push(CADRE([P([new TextRun({text:'365 231 enfants de 6 à 14 ans ',size:20,bold:true,color:ACC}),
  new TextRun({text:'ne sont jamais allés à l’école formelle, soit 33,1 % de cette classe d’âge. Sept sur dix vivent à la campagne, et 71 % se concentrent dans cinq wilayas seulement.',size:18})],{after:0})],ACC));
b.push(ESP(110));
b.push(H2('Pourquoi les données disponibles ne permettaient pas encore d’agir'));
b.push(BUL([new TextRun({text:'Les données existent mais ne se parlent pas. ',size:18,bold:true}),
  new TextRun({text:'La base population donne des habitants ; l’EPCV donne des taux. Séparées, ni l’une ni l’autre ne dit combien d’enfants sont concernés dans une wilaya donnée.',size:18})]));
b.push(BUL([new TextRun({text:'Un pourcentage ne se budgète pas. ',size:18,bold:true}),
  new TextRun({text:'« 44,4 % d’enfants hors école » ne se traduit ni en salles de classe ni en enseignants. Un ministère construit pour des enfants, pas pour des taux.',size:18})]));
b.push(BUL([new TextRun({text:'Aucun outil ne comparait objectivement les 13 wilayas, ',size:18,bold:true}),
  new TextRun({text:'et surtout aucun ne distinguait des situations que le même chiffre recouvre.',size:18})]));
b.push(ESP(90));
b.push(H2('Le lien avec « From Data to Storytelling »'));
b.push(P('Notre récit n’est pas une mise en scène des données : c’est une révélation qu’elles ne livrent pas seules. Deux wilayas affichent presque le même taux. Un tableau de bord ordinaire leur donnerait la même réponse. En décomposant ce que les enfants font réellement, tout les oppose.'));
b.push(ESP(70));
b.push(TAB(['','Hodh El Gharbi','Guidimakha'],[
  ['Hors école formelle','47,2 %','44,4 %'],
  ['Mahadra ou école coranique','32,9 %','1,9 %'],
  ['Aucune instruction','14,3 %','42,5 %'],
  ['Ce qu’il faut faire','Passerelles','Écoles']],
  [0.40,0.30,0.30],{boldCol:[0],right:[1,2],accent:[[1,1],[2,2]]}));
b.push(ESP(110));
b.push(P([new TextRun({text:'Même chiffre. Problèmes opposés. Solutions opposées. ',size:18,bold:true}),
  new TextRun({text:'Au Hodh El Gharbi les enfants apprennent, sans diplôme reconnu : il leur faut une équivalence. Au Guidimakha ils ne sont nulle part : il leur faut une école. C’est cette histoire que raconte EduFocus, et elle n’est lisible qu’une fois les données croisées et décomposées.',size:18})]));

/* ─────────── 2. Solution ─────────── */
b.push(H1('2. Solution développée'));
b.push(H2('Description de la solution'));
b.push(P('EduFocus est une application web trilingue (français, arabe, anglais) qui classe les 13 wilayas de Mauritanie selon un Indice de Priorité Éducative et dit, pour chacune, quoi faire. Elle est conçue pour être comprise sans formation statistique : les pourcentages y sont représentés par des silhouettes d’enfants, et chaque écran répond à une question posée en langage courant.'));
b.push(P([new TextRun({text:'Sept écrans : ',size:18,bold:true}),
  new TextRun({text:'un tableau de bord national (compteur, 100 enfants représentés, répartitions ville/campagne et garçons/filles), une carte des priorités, un classement triable, une fiche par wilaya, un simulateur de répartition, un comparateur et une page de méthode.',size:18})],{after:80}));
b.push(P([new TextRun({text:'La fonctionnalité qui différencie l’outil est l’encadré « Pourquoi cette wilaya ? ». ',size:18,bold:true}),
  new TextRun({text:'Pour chaque région, un texte écrit à partir de ses propres chiffres explique son classement, puis trois à quatre actions chiffrées disent quoi faire — nombre d’enfants sans instruction, salles nécessaires, obstacle dominant. L’outil ne demande pas qu’on lui fasse confiance : il montre son raisonnement.',size:18})]));
b.push(ESP(90));
b.push(H2('Approche technique'));
b.push(P([new TextRun({text:'Données. ',size:18,bold:true}),
  new TextRun({text:'Deux bases reliées par la wilaya. La base population 2013-2019 fournie par l’organisation donne les effectifs. L’EPCV 2019 de l’ANSADE — 60 600 individus, que nous sommes allés chercher car elle ne fait pas partie des données du hackathon — donne les taux.',size:18})]));
b.push(ESP(80));
b.push(P([new TextRun({text:'Pipeline, des données brutes au récit final. ',size:18,bold:true}),
  new TextRun({text:'Lecture du fichier SPSS et de la base population (pyreadstat, pandas) → jointure par une table de correspondance explicite des 13 libellés de wilaya → conversion taux × population en effectifs réels → décomposition de la variable de scolarisation en trois situations (école formelle, mahadra ou coranique, aucune instruction) → normalisation min-max et calcul de l’indice → génération des explications et des actions à partir de règles, dans les trois langues → injection dans une page autonome, contrôlée par 103 tests automatisés.',size:18})],{after:80}));
b.push(P([new TextRun({text:'Indice de Priorité Éducative : ',size:18,bold:true}),
  new TextRun({text:'0,45 × volume + 0,35 × intensité + 0,20 × vulnérabilité, chaque composante ramenée sur 0-100 par min-max sur les 13 wilayas. Le volume pèse le plus parce qu’un budget se dépense en enfants ; l’intensité corrige l’effet de taille ; la vulnérabilité rappelle qu’à situation scolaire égale, une wilaya pauvre a moins de moyens propres.',size:18})]));
b.push(ESP(80));
b.push(P([new TextRun({text:'Architecture. ',size:18,bold:true}),
  new TextRun({text:'L’application lit une source unique de 13 lignes et se contente de l’afficher : tous les indicateurs sont calculés en amont, ce qui la rend actualisable à chaque nouvelle enquête sans toucher au code. Page autonome, sans serveur ni connexion, sans bibliothèque graphique externe — carte et graphiques sont écrits en SVG. Python (pyreadstat, pandas, shapely) pour l’analyse, HTML/CSS/JavaScript pour l’interface, Playwright pour les tests.',size:18})]));

/* ─────────── 3. Résultats ─────────── */
b.push(H1('3. Résultats & Perspectives'));
b.push(H2('Résultats obtenus'));
b.push(TAB(['Indicateur','Résultat','Indicateur','Résultat'],[
  ['Enfants identifiés','365 231','Langues','3 (dont arabe RTL)'],
  ['Wilayas diagnostiquées','13 / 13','Tests automatisés','103, tous passants'],
  ['Actions chiffrées','44','Poids de l’app','184 Ko, hors connexion']],
  [0.26,0.22,0.26,0.26],{boldCol:[0,2]}));
b.push(ESP(100));
b.push(P([new TextRun({text:'Robustesse et précision assumée. ',size:18,bold:true}),
  new TextRun({text:'Le classement a été recalculé pour les 231 combinaisons de poids possibles : Guidimakha, Hodh El Gharbi et Assaba figurent dans les cinq premières dans 100 % des cas, cinq wilayas n’y entrent jamais. Le choix des poids déplace l’ordre, pas la décision. L’EPCV restant un échantillon, la marge d’erreur va de ±1,7 point à Nouakchott à ±4,5 points en Inchiri, et nous l’écrivons dans l’outil. Nous ne chiffrons aucun coût : convertir des enfants en ouguiyas sans données fiables serait une invention.',size:18})]));
b.push(ESP(60));
b.push(H2('Impact potentiel et suite envisagée'));
b.push(P('Transférable immédiatement à l’ANSADE et au ministère de l’Éducation nationale : pour chaque wilaya, EduFocus livre le nombre d’enfants concernés, l’intensité du problème, sa dimension sociale et le levier adapté, avec l’explication du classement. Trois prolongements sont prêts à être engagés :'));
b.push(BUL([new TextRun({text:'Actualisation automatique. ',size:18,bold:true}),
  new TextRun({text:'Un module de correspondance des variables permettrait de traiter une EPCV future dont la structure aurait changé.',size:18})]));
b.push(BUL([new TextRun({text:'Descente à la moughataa. ',size:18,bold:true}),
  new TextRun({text:'La méthode s’applique telle quelle à un découpage plus fin.',size:18})]));
b.push(BUL([new TextRun({text:'Dimensionnement budgétaire. ',size:18,bold:true}),
  new TextRun({text:'Avec les coûts unitaires du ministère, le simulateur produirait un chiffrage complet et identifierait le facteur limitant : budget, construction ou recrutement.',size:18})]));
b.push(ESP(30));

/* ─────────── Certification ─────────── */
b.push(CADRE([
  P('Nous certifions que ce document et les livrables associés ont été entièrement réalisés par notre équipe durant le hackathon IndabaX Mauritanie 2026. L’usage d’outils d’IA est déclaré conformément à l’article 5 ; le détail figure dans l’écran « Méthode » du prototype.',{bold:true,after:70}),
  P([new TextRun({text:'Équipe DataSphere   ·   Signature :  ______________________',size:17,color:GRIS})],{after:0})
],ACC));

const doc=new Document({
  creator:'Équipe DataSphere',title:'EduFocus — Document de solution',
  description:'IndabaX Mauritanie 2026',
  styles:{default:{document:{run:{font:'Calibri',size:18,color:ENCRE},
    paragraph:{spacing:{line:268}}}}},
  numbering:{config:[{reference:'p',levels:[{level:0,format:LevelFormat.BULLET,text:'\u2022',
    alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:convertInchesToTwip(0.28),
    hanging:convertInchesToTwip(0.16)}}}}]}]},
  sections:[{properties:{page:{size:{width:11906,height:16838},
    margin:{top:850,right:1080,bottom:720,left:1080}}},
    headers:{default:new Header({children:[new Paragraph({
      border:{bottom:{style:BorderStyle.SINGLE,size:6,color:TRAIT}},spacing:{after:160},
      children:[new TextRun({text:'EduFocus · Document de solution — IndabaX Mauritanie 2026',
        size:15,color:GRIS})]})]})},
    footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,
      children:[new TextRun({children:['Page ',PageNumber.CURRENT,' / ',PageNumber.TOTAL_PAGES],
        size:15,color:GRIS})]})]})},
    children:b}]});

Packer.toBuffer(doc).then(x=>{
  fs.writeFileSync('/mnt/user-data/outputs/edufocus/EduFocus_Document_Solution.docx',x);
  console.log('docx écrit :',(x.length/1024).toFixed(0),'Ko');
});
