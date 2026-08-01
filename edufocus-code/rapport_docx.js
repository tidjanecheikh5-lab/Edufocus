const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  Header, Footer, PageNumber, LevelFormat, convertInchesToTwip, PageBreak,
  TabStopType, TabStopPosition
} = require('docx');

/* ── Charte ─────────────────────────────────────────────────────────── */
const VERT = '1A4A6B', OR = 'C08A2E', GRIS = '6A7480', ENCRE = '171B1F';
const TRAIT = 'E2E6EA', PAPIER = 'F5F7F8', ROUGE = 'A6413B';
const W = 9360;                       // largeur utile en DXA (A4, marges 1")

/* ── Fabriques ──────────────────────────────────────────────────────── */
const P = (text, o = {}) => new Paragraph({
  spacing: { after: o.after ?? 120, line: o.line ?? 276 },
  alignment: o.align,
  indent: o.indent,
  border: o.border,
  shading: o.shading,
  children: Array.isArray(text) ? text : [new TextRun({
    text, size: o.size ?? 20, color: o.color ?? ENCRE,
    bold: o.bold, italics: o.italics, font: o.font
  })]
});

const H1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  spacing: { before: 360, after: 160 },
  children: [new TextRun({ text, size: 30, bold: true, color: VERT })]
});

const H2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  spacing: { before: 240, after: 110 },
  children: [new TextRun({ text, size: 23, bold: true, color: ENCRE })]
});

const BUL = (text, o = {}) => new Paragraph({
  numbering: { reference: 'puces', level: 0 },
  spacing: { after: 70, line: 264 },
  children: Array.isArray(text) ? text
    : [new TextRun({ text, size: 20, color: ENCRE })]
});

/** Bloc encadré (fond clair, filet coloré à gauche) */
const CADRE = (lignes, couleur = OR) => new Table({
  width: { size: W, type: WidthType.DXA },
  columnWidths: [W],
  borders: {
    top:    { style: BorderStyle.SINGLE, size: 1, color: TRAIT },
    bottom: { style: BorderStyle.SINGLE, size: 1, color: TRAIT },
    right:  { style: BorderStyle.SINGLE, size: 1, color: TRAIT },
    left:   { style: BorderStyle.SINGLE, size: 24, color: couleur },
    insideHorizontal: { style: BorderStyle.NONE },
    insideVertical:   { style: BorderStyle.NONE }
  },
  rows: [new TableRow({ children: [new TableCell({
    width: { size: W, type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: PAPIER, color: 'auto' },
    margins: { top: 140, bottom: 140, left: 200, right: 200 },
    children: lignes
  })] })]
});

/** Tableau de données : en-tête vert, lignes alternées */
function TAB(entetes, lignes, largeurs, opts = {}) {
  const cols = largeurs.map(f => Math.round(W * f));
  cols[cols.length - 1] = W - cols.slice(0, -1).reduce((a, b) => a + b, 0);
  const cell = (txt, i, o = {}) => new TableCell({
    width: { size: cols[i], type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: o.fill ?? 'FFFFFF', color: 'auto' },
    margins: { top: 70, bottom: 70, left: 110, right: 110 },
    children: [new Paragraph({
      spacing: { after: 0, line: 240 },
      alignment: o.align,
      children: [new TextRun({
        text: String(txt), size: 18, bold: o.bold,
        color: o.color ?? ENCRE
      })]
    })]
  });
  const rows = [new TableRow({
    tableHeader: true,
    children: entetes.map((h, i) => cell(h, i, {
      fill: VERT, bold: true, color: 'FFFFFF',
      align: opts.right && opts.right.includes(i) ? AlignmentType.RIGHT : undefined
    }))
  })];
  lignes.forEach((l, n) => rows.push(new TableRow({
    children: l.map((v, i) => cell(v, i, {
      fill: n % 2 ? PAPIER : 'FFFFFF',
      bold: (opts.boldCol || []).includes(i) || (opts.boldRows || []).includes(n),
      color: (opts.accent || []).some(([r, c]) => r === n && c === i) ? ROUGE : undefined,
      align: opts.right && opts.right.includes(i) ? AlignmentType.RIGHT : undefined
    }))
  })));
  return new Table({
    width: { size: W, type: WidthType.DXA },
    columnWidths: cols,
    borders: {
      top:    { style: BorderStyle.SINGLE, size: 2, color: TRAIT },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: TRAIT },
      left:   { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: TRAIT },
      insideVertical:   { style: BorderStyle.NONE }
    },
    rows
  });
}

/** Bloc de code / formule */
const CODE = (lignes) => new Table({
  width: { size: W, type: WidthType.DXA }, columnWidths: [W],
  borders: {
    top: { style: BorderStyle.SINGLE, size: 1, color: TRAIT },
    bottom: { style: BorderStyle.SINGLE, size: 1, color: TRAIT },
    left: { style: BorderStyle.SINGLE, size: 1, color: TRAIT },
    right: { style: BorderStyle.SINGLE, size: 1, color: TRAIT },
    insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE }
  },
  rows: [new TableRow({ children: [new TableCell({
    width: { size: W, type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: 'EDF1F4', color: 'auto' },
    margins: { top: 120, bottom: 120, left: 180, right: 180 },
    children: lignes.map(l => new Paragraph({
      spacing: { after: 20, line: 240 },
      children: [new TextRun({ text: l, size: 17, font: 'Consolas', color: '17384F' })]
    }))
  })] })]
});

const ESPACE = (h = 160) => new Paragraph({ spacing: { after: h }, children: [] });

/* ── Contenu ────────────────────────────────────────────────────────── */
const body = [];

/* Page de titre */
body.push(new Paragraph({
  spacing: { before: 2200, after: 0 },
  children: [new TextRun({ text: 'INDABAX MAURITANIE 2026  ·  POPULATION & DÉMOGRAPHIE',
    size: 17, bold: true, color: GRIS, characterSpacing: 60 })]
}));
body.push(new Paragraph({
  spacing: { before: 240, after: 60 },
  children: [new TextRun({ text: 'EduFocus', size: 76, bold: true, color: VERT })]
}));
body.push(new Paragraph({
  spacing: { after: 300 },
  children: [new TextRun({ text: 'Rapport d’analyse', size: 40, color: ENCRE })]
}));
body.push(new Paragraph({
  border: { top: { style: BorderStyle.SINGLE, size: 12, color: OR } },
  spacing: { after: 260 }, children: []
}));
body.push(P('De la démographie à la décision : où investir dans l’éducation en Mauritanie.',
  { size: 24, color: GRIS }));
body.push(ESPACE(320));
body.push(P([new TextRun({ text: 'Document technique accompagnant le prototype. ', size: 20 }),
  new TextRun({ text: 'Tous les calculs sont reproductibles avec les scripts fournis.',
    size: 20, bold: true })]));
body.push(ESPACE(900));
body.push(CADRE([
  P([new TextRun({ text: 'Sources croisées   ', size: 19, bold: true, color: VERT }),
     new TextRun({ text: 'Base population par wilaya 2013-2019 (organisation du hackathon) et EPCV 2019 de l’ANSADE, 60 600 individus.', size: 19 })], { after: 90 }),
  P([new TextRun({ text: 'Résultat central   ', size: 19, bold: true, color: VERT }),
     new TextRun({ text: '365 231 enfants de 6 à 14 ans n’ont jamais fréquenté l’école formelle, soit 33,1 % de cette classe d’âge.', size: 19 })], { after: 0 })
], VERT));
body.push(new Paragraph({ children: [new PageBreak()] }));

/* Sommaire */
body.push(H1('Sommaire'));
[['1', 'Les deux sources', 'Base population du hackathon · EPCV 2019 de l’ANSADE'],
 ['2', 'Le croisement des deux bases', 'Clé de jointure · transformer des pourcentages en enfants'],
 ['3', 'La définition de « hors école formelle »', 'Regroupement de C2 · pourquoi séparer mahadra et absence d’instruction'],
 ['4', 'Les indicateurs construits', 'Sept indicateurs · contrôle de validité de la pauvreté'],
 ['5', 'L’indice de priorité éducative', 'Formule · justification des poids · classement des 13 wilayas'],
 ['6', 'Le mécanisme et le levier', 'Exclusion · Substitution · Volume élevé'],
 ['7', 'Le simulateur', 'Trois règles de répartition · le résultat contre-intuitif'],
 ['8', 'Les recommandations par wilaya', 'Règles de génération des actions chiffrées'],
 ['9', 'Les résultats nationaux', 'Chiffres clés · répartition par sexe et par milieu'],
 ['10', 'Limites', 'Marges d’erreur · absence de pondération · ce que les données ne disent pas'],
 ['11', 'Reproductibilité', 'Scripts et tests automatisés'],
 ['12', 'Sources', 'Références et ressources open source']
].forEach(([n, titre, sous]) => {
  body.push(new Paragraph({
    spacing: { after: 20, line: 264 },
    indent: { left: 460, hanging: 460 },
    children: [
      new TextRun({ text: n.padStart(2, ' ') + '.  ', size: 21, bold: true, color: OR }),
      new TextRun({ text: titre, size: 21, bold: true, color: ENCRE })
    ]
  }));
  body.push(new Paragraph({
    spacing: { after: 130, line: 240 }, indent: { left: 460 },
    children: [new TextRun({ text: sous, size: 18, color: GRIS })]
  }));
});
body.push(new Paragraph({ children: [new PageBreak()] }));

/* 1. Sources */
body.push(H1('1. Les deux sources'));
body.push(H2('1.1  Base population par wilaya, 2013-2019'));
body.push(P('Fournie par l’organisation du hackathon (fichier Population.xlsx, feuille Data). Une ligne par région, une colonne par année. Elle donne le nombre d’habitants.'));
body.push(P([new TextRun({ text: 'Population 2019 retenue pour la Mauritanie : ', size: 20 }),
  new TextRun({ text: '4 077 347 habitants', size: 20, bold: true })]));

body.push(H2('1.2  EPCV 2019 — Enquête Permanente sur les Conditions de Vie des ménages'));
body.push(P('Produite par l’ANSADE. Cette base ne fait pas partie des données du hackathon : elle a été obtenue auprès de l’Agence, producteur officiel des statistiques démographiques et de pauvreté du pays.'));
body.push(P('Fichier SPSS, 60 600 individus, 11 variables, 13 wilayas. Aucune valeur manquante sur les variables utilisées. Sous-échantillon des 6-14 ans : 16 451 enfants.'));
body.push(ESPACE(100));
body.push(TAB(['Variable', 'Libellé', 'Modalités'], [
  ['wilaya', 'Wilaya', '13'],
  ['Groupe_age', 'Groupe d’âge', '1 = 0-5 · 2 = 6-14 · 3 = 15-24 · 4 = 25-59 · 5 = 60+'],
  ['C2', 'Est-ce que [NOM] est déjà allé à l’école', 'voir section 3'],
  ['B2', 'Sexe', '1 = Masculin · 2 = Féminin'],
  ['milieu', 'Milieu', '1 = Urbain · 2 = Rural'],
  ['pauv', 'Prévalence de la pauvreté', '0 / 1']
], [0.18, 0.34, 0.48], { boldCol: [0] }));

/* 2. Croisement */
body.push(H1('2. Le croisement des deux bases'));
body.push(H2('2.1  La clé de jointure'));
body.push(P('Les deux bases sont reliées par la wilaya. Les libellés diffèrent d’une base à l’autre ; une table de correspondance explicite a été écrite plutôt qu’un rapprochement automatique, pour éviter toute erreur d’appariement silencieuse.'));
body.push(ESPACE(100));
body.push(TAB(['Libellé EPCV', 'Libellé base population', 'Nom retenu'], [
  ['Hodh charghy', 'El Hodh El Charghi', 'Hodh El Charghi'],
  ['Hodh Gharby', 'El Hodh El Gharbi', 'Hodh El Gharbi'],
  ['Dakhlett Nouadibou', 'D. Nouadhibou', 'Dakhlet Nouadhibou'],
  ['Guidimagha', 'Guidimakha', 'Guidimakha'],
  ['Tirs-ezemour', 'Tiris Zemour', 'Tiris Zemmour'],
  ['Assaba, Gorgol, Brakna, Trarza, Adrar, Tagant, Inchiri, Nouakchott', 'identiques', 'identiques']
], [0.40, 0.30, 0.30]));
body.push(ESPACE(120));
body.push(P('Les 13 wilayas s’apparient sans reste.', { bold: true }));

body.push(H2('2.2  Le principe : transformer des pourcentages en enfants'));
body.push(P('L’EPCV donne des taux sur un échantillon. La base population donne des effectifs. Multipliés, ils donnent des effectifs réels par wilaya. Pour chaque wilaya w :'));
body.push(CODE([
  'part_6_14(w)     = proportion d’individus avec Groupe_age = 2 dans l’EPCV',
  'enfants_6_14(w)  = population_2019(w) × part_6_14(w)',
  'taux_hors(w)     = proportion d’enfants 6-14 hors école formelle',
  'enfants_hors(w)  = enfants_6_14(w) × taux_hors(w)'
]));
body.push(ESPACE(140));
body.push(P('Exemple — Guidimakha', { bold: true, size: 21 }));
body.push(CODE([
  'population_2019  = 308 457 habitants     (base population)',
  'part_6_14        = 30,25 %               (EPCV : 1 879 enfants sur 6 211 individus)',
  'enfants_6_14     = 308 457 × 0,3025   =  93 317 enfants',
  'taux_hors        = 44,4 %                (EPCV : 835 enfants sur 1 879)',
  'enfants_hors     = 93 317 × 0,444     =  41 469 enfants'
]));
body.push(ESPACE(140));
body.push(CADRE([P([
  new TextRun({ text: 'C’est le cœur de la méthode. ', size: 20, bold: true }),
  new TextRun({ text: '44,4 % ne se budgète pas. 41 469 enfants se budgète.', size: 20 })
], { after: 0 })]));

/* 3. Définition */
body.push(H1('3. La définition de « hors école formelle »'));
body.push(P('La variable C2 distingue cinq situations. Le regroupement retenu :'));
body.push(ESPACE(100));
body.push(TAB(['Code', 'Modalité EPCV', 'Regroupement', 'National (6-14)'], [
  ['3', 'Oui, école formelle uniquement', 'Scolarisé', '27,5 %'],
  ['4', 'Oui, école formelle et enseignement coranique', 'Scolarisé', '39,4 %'],
  ['1', 'Oui, enseignement coranique uniquement', 'Hors formel — substitution', '16,2 %'],
  ['2', 'Oui, Mahadra uniquement', 'Hors formel — substitution', '0,5 %'],
  ['5', 'Non', 'Hors formel — aucune instruction', '16,4 %']
], [0.09, 0.42, 0.31, 0.18], { right: [3] }));
body.push(ESPACE(140));
body.push(CODE(['hors école formelle = C2 ∈ {1, 2, 5}   →   33,1 % au niveau national']));
body.push(ESPACE(140));
body.push(P('Un enfant qui fréquente à la fois l’école formelle et l’enseignement coranique est compté comme scolarisé (code 4). C’est un choix : il a accès au diplôme reconnu.'));

body.push(H2('Point de vocabulaire à connaître'));
body.push(CADRE([
  P('La catégorie appelée « mahadra » regroupe en réalité les codes 1 et 2, et elle est composée à 97 % d’enseignement coranique (16,2 %) contre seulement 0,5 % de mahadra à proprement parler.', { after: 90 }),
  P([new TextRun({ text: 'L’interface dit correctement « mahadra ou école coranique ». En revanche, toute formulation qui parlerait de « mahadra » seule serait imprécise', size: 20, bold: true }),
     new TextRun({ text: ' et doit être corrigée dans les supports de présentation.', size: 20 })], { after: 0 })
], ROUGE));

body.push(H2('Pourquoi séparer les deux'));
body.push(P('C’est l’idée centrale du projet. Deux wilayas au même taux hors école peuvent avoir des problèmes opposés.'));
body.push(ESPACE(100));
body.push(TAB(['', 'Hodh El Gharbi', 'Guidimakha'], [
  ['Taux hors école formelle', '47,2 %', '44,4 %'],
  ['Coranique ou mahadra', '32,9 %', '1,9 %'],
  ['Aucune instruction', '14,3 %', '42,5 %'],
  ['Levier', 'Passerelles', 'Écoles']
], [0.40, 0.30, 0.30], { boldCol: [0], right: [1, 2],
   accent: [[1, 1], [2, 2]], boldRows: [3] }));
body.push(ESPACE(140));
body.push(P('Au Hodh El Gharbi les enfants apprennent mais sans diplôme reconnu : il faut des équivalences. Au Guidimakha ils ne sont nulle part : il faut des écoles. Un classement par taux seul ne voit pas cette différence.'));

/* 4. Indicateurs */
body.push(H1('4. Les indicateurs construits'));
body.push(P('Tous calculés par wilaya sur l’EPCV, puis appliqués à la population 2019.'));
body.push(ESPACE(100));
body.push(TAB(['Indicateur', 'Calcul', 'Population de référence'], [
  ['taux_hors_ecole', 'part de C2 ∈ {1,2,5}', '6-14 ans'],
  ['pct_mahadra', 'part de C2 ∈ {1,2}', '6-14 ans'],
  ['pct_aucune_instruction', 'part de C2 = 5', '6-14 ans'],
  ['taux_garcons / taux_filles', 'taux hors école par B2', '6-14 ans'],
  ['taux_pauvrete', 'moyenne de pauv', 'tous individus'],
  ['part_rurale', 'part de milieu = 2', 'tous individus'],
  ['ratio_dependance', '(0-14 ans) / (15-59 ans) × 100', 'tous individus']
], [0.36, 0.36, 0.28], { boldCol: [0] }));
body.push(ESPACE(140));
body.push(CADRE([P([
  new TextRun({ text: 'Contrôle de validité.  ', size: 20, bold: true, color: VERT }),
  new TextRun({ text: 'Le taux de pauvreté national calculé sur l’échantillon donne 28,75 %, proche du chiffre officiel EPCV 2019 (≈ 28,2 %). La variable n’est pas inversée et le sens de codage est confirmé.', size: 20 })
], { after: 0 })], VERT));

/* 5. Indice */
body.push(H1('5. L’indice de priorité éducative'));
body.push(H2('5.1  Formule et normalisation'));
body.push(CODE([
  'indice = 0,45 × volume + 0,35 × intensité + 0,20 × vulnérabilité',
  '',
  'volume        = nombre d’enfants hors école',
  'intensité     = taux hors école',
  'vulnérabilité = taux de pauvreté',
  '',
  'Chaque composante est ramenée sur 0-100 par min-max sur les 13 wilayas :',
  'normalisé(x) = (x − min) / (max − min) × 100'
]));
body.push(ESPACE(140));
body.push(P('La wilaya la plus touchée du pays obtient 100, la moins touchée 0.'));

body.push(H2('5.2  Justification des poids'));
body.push(BUL([new TextRun({ text: 'Le volume ', size: 20, bold: true }),
  new TextRun({ text: 'pèse le plus (45 %) parce qu’un budget se dépense en enfants, pas en pourcentages.', size: 20 })]));
body.push(BUL([new TextRun({ text: 'L’intensité ', size: 20, bold: true }),
  new TextRun({ text: '(35 %) corrige l’effet de taille : sans elle, les grandes wilayas écraseraient le classement.', size: 20 })]));
body.push(BUL([new TextRun({ text: 'La vulnérabilité ', size: 20, bold: true }),
  new TextRun({ text: '(20 %) rappelle qu’à situation scolaire égale, une wilaya pauvre dispose de moins de moyens propres.', size: 20 })]));
body.push(ESPACE(120));
body.push(P('Ces poids sont un choix, pas un résultat. La formule est affichée dans l’application pour que quiconque puisse la recalculer autrement.'));

body.push(H2('5.3  Résultat'));
body.push(TAB(['Rang', 'Wilaya', 'Volume', 'Intensité', 'Vulnér.', 'Indice', 'Priorité'], [
  ['1', 'Guidimakha', '62', '93', '100', '81', 'Très élevée'],
  ['2', 'Hodh El Charghi', '90', '84', '33', '77', 'Très élevée'],
  ['3', 'Hodh El Gharbi', '66', '100', '58', '76', 'Très élevée'],
  ['4', 'Assaba', '73', '86', '55', '74', 'Élevée'],
  ['5', 'Nouakchott', '100', '45', '8', '62', 'Élevée'],
  ['6', 'Gorgol', '59', '66', '51', '60', 'Élevée'],
  ['7', 'Trarza', '39', '62', '33', '46', 'Moyenne'],
  ['8', 'Brakna', '35', '47', '69', '46', 'Moyenne'],
  ['9', 'Tagant', '9', '59', '69', '38', 'Moyenne'],
  ['10', 'Inchiri', '0', '26', '40', '17', 'Faible'],
  ['11', 'Dakhlet Nouadhibou', '9', '37', '0', '17', 'Faible'],
  ['12', 'Tiris Zemmour', '2', '25', '15', '12', 'Faible'],
  ['13', 'Adrar', '0', '0', '41', '8', 'Faible']
], [0.08, 0.26, 0.11, 0.12, 0.11, 0.10, 0.22],
  { boldCol: [1, 5], right: [0, 2, 3, 4, 5] }));
body.push(ESPACE(140));
body.push(P('Détail du calcul pour Guidimakha :', { bold: true }));
body.push(CODE(['0,45 × 62,3 + 0,35 × 93,2 + 0,20 × 100 = 28,0 + 32,6 + 20,0 = 80,6 → 81']));

body.push(H2('5.4  Deux résultats à savoir défendre'));
body.push(CADRE([
  P([new TextRun({ text: 'Nouakchott a le plus d’enfants hors école du pays (65 995) mais n’est que 5', size: 20, bold: true }),
     new TextRun({ text: 'e', size: 20, bold: true, superScript: true }),
     new TextRun({ text: '.  ', size: 20, bold: true }),
     new TextRun({ text: 'Son volume est maximal (100/100), mais son taux est faible (24,8 %, intensité 45) et c’est la wilaya la moins pauvre (13,1 %, vulnérabilité 8).', size: 20 })], { after: 110 }),
  P([new TextRun({ text: 'Hodh El Gharbi a le pire taux du pays (47,2 %) mais n’est que 3', size: 20, bold: true }),
     new TextRun({ text: 'e', size: 20, bold: true, superScript: true }),
     new TextRun({ text: '.  ', size: 20, bold: true }),
     new TextRun({ text: 'Elle compte moins d’enfants et moins de pauvreté que Guidimakha.', size: 20 })], { after: 110 }),
  P('Ces deux cas montrent que l’indice ne se contente pas de reclasser une seule colonne.', { after: 0, italics: true })
]));

/* 6. Mécanisme */
body.push(H1('6. Le mécanisme et le levier'));
body.push(P('Une règle explicite attribue à chaque wilaya un mécanisme dominant, et donc un levier d’action.'));
body.push(CODE([
  'part_aucune    = pct_aucune_instruction / taux_hors_ecole × 100',
  'part_nationale = enfants_hors_ecole / total national × 100',
  '',
  'si part_nationale ≥ 15 % et taux_hors_ecole < 33,1 %   →  Volume élevé',
  'sinon si part_aucune < 50 %                            →  Substitution',
  'sinon                                                  →  Exclusion'
]));
body.push(ESPACE(140));
body.push(TAB(['Mécanisme', 'Signification', 'Levier', 'Wilayas'], [
  ['Exclusion', 'La majorité des enfants hors école ne reçoit aucune instruction', 'Créer de l’offre scolaire, cantines, transferts', 'Guidimakha, Gorgol, Brakna, Tagant, Dakhlet Nouadhibou, Tiris Zemmour'],
  ['Substitution', 'La majorité est en coranique ou mahadra', 'Passerelles et équivalences', 'Hodh El Charghi, Hodh El Gharbi, Assaba, Trarza, Inchiri, Adrar'],
  ['Volume élevé', 'Poids national fort, taux sous la moyenne', 'Capacité d’accueil', 'Nouakchott']
], [0.15, 0.28, 0.24, 0.33], { boldCol: [0] }));

/* 7. Simulateur */
body.push(H1('7. Le simulateur'));
body.push(H2('7.1  Ce qu’il fait'));
body.push(P('L’utilisateur fixe une capacité exprimée en enfants — combien d’enfants il peut scolariser — et choisit une règle de répartition. Aucune wilaya ne peut recevoir plus de places qu’elle n’a d’enfants hors école ; le surplus est redistribué de façon itérative.'));
body.push(ESPACE(100));
body.push(TAB(['Règle', 'Principe'], [
  ['Selon le nombre', 'Part proportionnelle aux enfants hors école'],
  ['Les plus urgentes d’abord', 'Ordre de l’indice, chaque wilaya réglée entièrement avant la suivante'],
  ['La même part pour chacune', 'Partage égal entre les 13']
], [0.32, 0.68], { boldCol: [0] }));

body.push(H2('7.2  Le résultat contre-intuitif'));
body.push(CADRE([
  P([new TextRun({ text: 'Le taux national après simulation est identique pour les trois règles. ', size: 20, bold: true }),
     new TextRun({ text: 'C’est arithmétique : le nombre total d’enfants scolarisés ne dépend pas de la manière de les répartir. Avec 100 000 places, il passe de 33,1 % à 24,2 % dans les trois cas.', size: 20 })], { after: 0 })
], ROUGE));
body.push(ESPACE(140));
body.push(P('Ce qui change est la distribution :'));
body.push(ESPACE(100));
body.push(TAB(['100 000 places', 'Wilayas entièrement réglées', 'La plus en retard reste à'], [
  ['Selon le nombre', '0', '34,3 %'],
  ['Les plus urgentes', '1  (Guidimakha à 0 %)', '47,2 %  — Hodh El Gharbi intact'],
  ['La même part', '5  (les petites)', '36,1 %']
], [0.28, 0.34, 0.38], { boldCol: [0], accent: [[1, 2]] }));
body.push(ESPACE(140));
body.push(P('Concentrer règle quelques wilayas et en laisse d’autres intactes. Étaler soulage tout le monde sans régler personne. L’arbitrage est politique, pas statistique : l’outil l’éclaire, il ne le tranche pas.', { bold: true }));

body.push(H2('7.3  Pourquoi aucun coût n’est chiffré'));
body.push(P('Une place en école ne coûte pas ce que coûte une passerelle depuis une mahadra, et nous ne disposons d’aucune donnée de coût fiable. Convertir des enfants en ouguiyas serait une invention, pas une analyse.'));
body.push(H2('7.4  Des enfants aux moyens matériels'));
body.push(P('Le simulateur convertit les places en moyens concrets à partir de deux hypothèses seulement, toutes deux affichées à l’écran et modifiables par l’utilisateur.'));
body.push(ESPACE(100));
body.push(TAB(['Hypothèse', 'Défaut', 'Source'], [
  ['Élèves par salle de classe', '40', 'Normes minimales de l’INEE, maximum recommandé au primaire'],
  ['Salles par école', '6', 'Une salle par niveau du cycle fondamental']
], [0.32, 0.12, 0.56], { boldCol: [0], right: [1] }));
body.push(ESPACE(140));
body.push(P('Un enseignant est compté par salle. Le type de moyen dépend du mécanisme — c’est ce qui distingue ce dimensionnement d’un simple produit en croix.', { bold: true }));
body.push(ESPACE(100));
body.push(TAB(['Mécanisme', 'Moyen calculé', 'Raison'], [
  ['Exclusion et Volume élevé', 'Salles neuves et écoles pour les abriter', 'Voir la note ci-dessous'],
  ['Substitution', 'Classes passerelles, mahadras à certifier', 'On ne construit pas une école pour un enfant qui apprend déjà : il lui faut une équivalence, pas un bâtiment']
], [0.22, 0.36, 0.42], { boldCol: [0] }));
body.push(ESPACE(140));
body.push(CADRE([P([
  new TextRun({ text: 'Pourquoi des constructions neuves dans les deux premiers cas.  ', size: 20, bold: true }),
  new TextRun({ text: 'Nous ne disposons d’aucune donnée sur la capacité résiduelle des écoles existantes. Supposer qu’elles pourraient absorber ces enfants serait une hypothèse que rien ne soutient. Si le ministère connaît les places disponibles, son besoin de construction sera inférieur au nôtre : notre chiffre est un majorant, et c’est volontaire.', size: 20 })
], { after: 0 })]));
body.push(ESPACE(140));
body.push(P('À 100 000 places réparties au prorata : 2 508 salles, 2 508 enseignants, 216 écoles neuves, et 49 205 enfants à faire passer de la mahadra vers le formel. Si le ministère applique d’autres normes, il modifie les deux valeurs et l’ensemble se recalcule.'));

/* 8. Recommandations */
body.push(H1('8. Les recommandations par wilaya'));
body.push(P('Trois à quatre actions chiffrées sont générées pour chaque wilaya à partir de ses propres données, selon des règles fixes :'));
body.push(BUL([new TextRun({ text: 'Levier principal ', size: 20, bold: true }),
  new TextRun({ text: '— dicté par le mécanisme, chiffré en enfants et en salles.', size: 20 })]));
body.push(BUL([new TextRun({ text: 'Second volet éducatif ', size: 20, bold: true }),
  new TextRun({ text: '— l’autre catégorie, pour ne pas l’oublier.', size: 20 })]));
body.push(BUL([new TextRun({ text: 'Condition d’accès dominante ', size: 20, bold: true }),
  new TextRun({ text: '— pauvreté ≥ 35 % → lever l’obstacle du coût ; sinon ruralité ≥ 60 % → rapprocher l’école ; sinon cibler les quartiers.', size: 20 })]));
body.push(BUL([new TextRun({ text: 'Écart garçons-filles ', size: 20, bold: true }),
  new TextRun({ text: '— uniquement si l’écart atteint 4 points.', size: 20 })]));
body.push(ESPACE(120));
body.push(P('Quatre wilayas déclenchent la quatrième action : Nouakchott (+6,5 points au détriment des garçons), Trarza (+5,2), Tiris Zemmour (+5,2), Inchiri (+4,4). Aucune recommandation creuse n’est produite là où l’écart n’est pas significatif.'));

/* 9. Résultats nationaux */
body.push(H1('9. Les résultats nationaux'));
body.push(TAB(['Indicateur', 'Valeur'], [
  ['Population 2019', '4 077 347'],
  ['Part des 6-14 ans', '27,1 %'],
  ['Enfants de 6 à 14 ans (somme des wilayas)', '1 095 211'],
  ['Enfants de 6 à 14 ans (estimation nationale directe)', '1 106 872'],
  ['Enfants hors école formelle', '365 231'],
  ['Taux hors école formelle', '33,1 %'],
  ['dont coranique ou mahadra', '16,7 %  —  194 075 enfants'],
  ['dont aucune instruction', '16,4 %  —  171 103 enfants'],
  ['Concentration dans 5 wilayas', '71 %'],
  ['Taux de pauvreté', '28,8 %']
], [0.60, 0.40], { right: [1], boldRows: [4] }));

body.push(H2('Répartition des 365 231 enfants hors école'));
body.push(TAB(['', 'Part', 'Effectif', 'Taux dans le groupe'], [
  ['Garçons', '52,4 %', '191 381', '34,0 %'],
  ['Filles', '47,6 %', '173 850', '32,1 %'],
  ['Campagne', '73,6 %', '268 810', '42,0 %'],
  ['Ville', '26,4 %', '96 421', '20,8 %']
], [0.28, 0.18, 0.26, 0.28], { boldCol: [0], right: [1, 2, 3], boldRows: [2] }));
body.push(ESPACE(160));
body.push(CADRE([
  P([new TextRun({ text: 'La fracture n’est pas le genre — elle est territoriale. ', size: 21, bold: true, color: VERT }),
     new TextRun({ text: 'L’écart garçons-filles est de 1,9 point au niveau national ; l’écart ville-campagne est de 21,2 points, soit plus du double de taux.', size: 20 })], { after: 0 })
], VERT));

/* 10. Limites */
body.push(H1('10. Limites'));
body.push(H2('10.1  Précision de l’échantillon'));
body.push(P('L’EPCV est un échantillon. Les taux sont des estimations assorties d’une marge d’erreur, calculée ici à 95 % de confiance.'));
body.push(ESPACE(100));
body.push(TAB(['Wilaya', 'Enfants enquêtés', 'Taux', 'Marge'], [
  ['Nouakchott', '2 619', '24,8 %', '± 1,7'],
  ['Hodh El Charghi', '2 293', '40,7 %', '± 2,0'],
  ['Guidimakha', '1 879', '44,4 %', '± 2,2'],
  ['Gorgol', '1 778', '33,5 %', '± 2,2'],
  ['Assaba', '1 468', '41,6 %', '± 2,5'],
  ['Brakna', '1 426', '25,5 %', '± 2,3'],
  ['Hodh El Gharbi', '1 380', '47,2 %', '± 2,6'],
  ['Trarza', '1 187', '31,6 %', '± 2,6'],
  ['Adrar', '598', '6,2 %', '± 1,9'],
  ['Dakhlet Nouadhibou', '594', '21,2 %', '± 3,3'],
  ['Tagant', '483', '30,2 %', '± 4,1'],
  ['Tiris Zemmour', '479', '16,3 %', '± 3,3'],
  ['Inchiri', '267', '16,9 %', '± 4,5']
], [0.34, 0.24, 0.20, 0.22], { boldCol: [0], right: [1, 2, 3], boldRows: [12] }));
body.push(ESPACE(140));
body.push(CADRE([P([
  new TextRun({ text: 'Conséquence à assumer.  ', size: 20, bold: true }),
  new TextRun({ text: 'Les écarts de rang entre wilayas voisines ne sont pas tous statistiquement significatifs. Guidimakha (44,4 ± 2,2) et Hodh El Gharbi (47,2 ± 2,6) ont des intervalles qui se chevauchent.', size: 20 })
], { after: 0 })], ROUGE));

body.push(H2('10.2  Absence de pondération de sondage'));
body.push(P('L’extrait exploité ne comporte pas de variable de pondération. Les taux sont calculés sur l’échantillon brut. Ils peuvent s’écarter légèrement des chiffres officiels publiés par l’ANSADE.'));
body.push(P('Conséquence mesurée. L’échantillon n’est pas proportionnel à la population : les petites wilayas y sont surreprésentées. Inchiri compte 24 425 habitants pour 267 enfants enquêtés, quand Nouakchott en compte 1 195 636 pour 2 619 enfants. Deux façons d’estimer le nombre d’enfants de 6 à 14 ans divergent donc :', { bold: true }));
body.push(ESPACE(100));
body.push(TAB(['Méthode', 'Résultat'], [
  ['Somme wilaya par wilaya — Σ(population_w × part_6_14_w)', '1 095 211'],
  ['Estimation nationale directe — population × part brute (27,15 %)', '1 106 872'],
  ['Écart', '11 661 enfants, soit 1,1 %']
], [0.68, 0.32], { right: [1], boldRows: [0] }));
body.push(ESPACE(140));
body.push(P('Nous retenons la première, calculée wilaya par wilaya, parce qu’elle applique à chaque territoire sa propre structure d’âge au lieu d’une moyenne nationale influencée par la composition de l’échantillon.'));
body.push(CADRE([
  P([new TextRun({ text: 'Le chiffre central du projet — 365 231 enfants hors école — est construit par cette même méthode wilaya par wilaya. Il n’est pas affecté par ce biais.', size: 20, bold: true })], { after: 100 }),
  P('En revanche, la formulation « 1 107 000 enfants en âge d’être scolarisés » qui figure dans le document de soumission correspond à l’estimation nationale directe. L’écart de 1,1 % avec la somme des wilayas doit être signalé si la question est posée.', { after: 0 })
], VERT));

body.push(H2('10.3  Ce que les données ne disent pas'));
body.push(BUL('Les taux datent de 2019 et sont appliqués à la population 2019. Rien ne dit qu’ils sont encore valables aujourd’hui.'));
body.push(BUL('C2 mesure si l’enfant est déjà allé à l’école, pas s’il y est aujourd’hui ni ce qu’il y apprend. Un enfant inscrit mais absent est compté comme scolarisé.'));
body.push(BUL('Aucune mesure de la qualité de l’enseignement, de la distance à l’école, de l’état des bâtiments ni du nombre d’enseignants disponibles.'));
body.push(BUL('Aucune prédiction. EduFocus décrit une situation observée et la rend comparable ; il ne dit pas ce qui se passera si l’on investit.'));

/* 11. Reproductibilité */
body.push(H1('11. Reproductibilité'));
body.push(CODE([
  'pip install pyreadstat pandas openpyxl shapely',
  '',
  'python analyse.py   # croisement, indicateurs, indice   → wilayas_detail.csv',
  'python dataset.py   # noms et explications AR / EN      → wilayas.csv',
  'python actions.py   # recommandations chiffrées         → wilayas.csv',
  'python carte.py     # frontières Natural Earth          → carte.json',
  'python build.py     # assemblage                        → index.html',
  'python verif.py     # 59 tests automatisés'
]));
body.push(ESPACE(140));
body.push(P('analyse.py affiche tous les contrôles nationaux à l’exécution. Le prototype lit une source unique, wilayas.csv (13 lignes) : aucun indicateur n’est recalculé dans l’interface, à l’exception assumée de l’allocation du simulateur.'));
body.push(P('59 tests automatisés couvrent la géométrie de la carte, l’absence de débordement sur mobile et en RTL, la somme des grilles de 100, la conservation de la capacité du simulateur sous les trois règles, la traduction des trois langues et le comportement en cas de valeur manquante.'));

/* 12. Sources */
body.push(H1('12. Sources'));
body.push(P([new TextRun({ text: '1.  Population par wilaya, 2013-2019. ', size: 20, bold: true }),
  new TextRun({ text: 'Base fournie par l’organisation du hackathon — IndabaX Mauritanie, Édition 2026.', size: 20 })]));
body.push(P([new TextRun({ text: '2.  Enquête Permanente sur les Conditions de Vie des ménages (EPCV 2019). ', size: 20, bold: true }),
  new TextRun({ text: 'Agence Nationale de la Statistique et de l’Analyse Démographique et Économique (ANSADE), République Islamique de Mauritanie. Extrait exploité : 60 600 individus, 13 wilayas. Base obtenue auprès de l’ANSADE, accessible sur demande auprès de l’Agence.', size: 20 })]));
body.push(P([new TextRun({ text: '3.  Fond de carte. ', size: 20, bold: true }),
  new TextRun({ text: 'Natural Earth, admin-1 (domaine public), simplifié à 1,2 km.', size: 20 })]));
body.push(P([new TextRun({ text: '4.  Ressources open source. ', size: 20, bold: true }),
  new TextRun({ text: 'Polices Poppins, Nunito Sans, IBM Plex Sans Arabic et Amiri (SIL Open Font License 1.1). Aucune bibliothèque graphique externe : carte, anneaux et graphiques sont écrits en SVG.', size: 20 })]));
body.push(P([new TextRun({ text: '5.  Normes minimales de l’INEE. ', size: 20, bold: true }),
  new TextRun({ text: 'Inter-Agency Network for Education in Emergencies : 40 élèves par enseignant au maximum en primaire. Utilisé comme hypothèse par défaut du simulateur, modifiable par l’utilisateur.', size: 20 })]));

/* ── Document ───────────────────────────────────────────────────────── */
const doc = new Document({
  creator: 'Équipe EduFocus',
  title: 'EduFocus — Rapport d’analyse',
  description: 'IndabaX Mauritanie 2026 — Population & Démographie',
  styles: {
    default: {
      document: { run: { font: 'Calibri', size: 20, color: ENCRE },
                  paragraph: { spacing: { line: 276 } } },
      heading1: { run: { font: 'Calibri', size: 30, bold: true, color: VERT } },
      heading2: { run: { font: 'Calibri', size: 23, bold: true, color: ENCRE } }
    }
  },
  numbering: {
    config: [{
      reference: 'puces',
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: '\u2022',
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: convertInchesToTwip(0.3),
                                        hanging: convertInchesToTwip(0.18) } } }
      }]
    }]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },      // A4
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({ children: [new Paragraph({
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: TRAIT } },
        spacing: { after: 200 },
        tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
        children: [
          new TextRun({ text: 'EduFocus — Rapport d’analyse', size: 16, color: GRIS, bold: true }),
          new TextRun({ text: '\tIndabaX Mauritanie 2026', size: 16, color: GRIS })
        ]
      })] })
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ children: ['Page ', PageNumber.CURRENT, ' / ', PageNumber.TOTAL_PAGES],
          size: 16, color: GRIS })]
      })] })
    },
    children: body
  }]
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync('/mnt/user-data/outputs/edufocus/EduFocus_Rapport_Analyse.docx', b);
  console.log('docx écrit :', (b.length / 1024).toFixed(0), 'Ko');
});
