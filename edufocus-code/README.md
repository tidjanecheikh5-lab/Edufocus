# EduFocus

**De la démographie à la décision : où investir dans l'éducation en Mauritanie**

Projet réalisé pour le hackathon **IndabaX Mauritanie — Édition 2026**
Thème : Population & Démographie

🔗 **Prototype en ligne :** _(coller le lien ici après déploiement)_

---

## Le problème

**365 231 enfants mauritaniens de 6 à 14 ans ne sont jamais allés à l'école formelle**, soit 33,1 % de cette classe d'âge. Avec des moyens limités, l'État doit choisir où construire et où recruter. Aucun outil ne comparait objectivement les 13 wilayas.

## L'idée

Un classement ne suffit pas. **Hodh El Gharbi (47,2 %) et Guidimakha (44,4 %) ont presque le même taux — et des problèmes opposés :**

| | Hodh El Gharbi | Guidimakha |
|---|---|---|
| Hors école formelle | 47,2 % | 44,4 % |
| Mahadra ou école coranique | **32,9 %** | 1,9 % |
| Aucune instruction | 14,3 % | **42,5 %** |
| Levier | Passerelles | Écoles |

Au Hodh El Gharbi les enfants **apprennent**, sans diplôme reconnu : il faut des équivalences. Au Guidimakha ils ne sont **nulle part** : il faut des écoles. Même chiffre, solutions opposées. C'est ce que voit EduFocus.

## La méthode

Nous relions deux bases par la wilaya :

- **Base population 2013-2019** (fournie par l'organisation) → le *nombre* d'habitants
- **EPCV 2019** de l'ANSADE, 60 600 individus → les *taux*

Multipliés, ils donnent des effectifs réels. **Nous transformons des pourcentages en enfants.** Un pourcentage ne se budgète pas ; 41 469 enfants, si.

Les wilayas sont classées par un **Indice de Priorité Éducative** :

```
indice = 0,45 x volume + 0,35 x intensite + 0,20 x vulnerabilite
```

chaque composante ramenée sur 0-100 par min-max sur les 13 wilayas.

Le classement a été testé sur les **231 combinaisons de poids possibles** : Guidimakha, Hodh El Gharbi et Assaba sont dans les cinq premières dans 100 % des cas ; cinq wilayas n'y entrent jamais. Le choix des poids déplace l'ordre, pas la décision.

---

## Le prototype

Un fichier HTML autonome, sans serveur ni connexion. Sept écrans, trois langues (français, arabe avec RTL, anglais).

| Écran | Contenu |
|---|---|
| Accueil | Tableau de bord : compteur, grille de 100 personnes, anneaux sexe/milieu, histogrammes |
| Carte | Les 13 wilayas colorées par priorité, cliquables |
| Classement | Tableau triable, export CSV |
| Fiche wilaya | Chiffres clés, décomposition, « pourquoi cette wilaya », actions chiffrées |
| Simulateur | Trois règles de répartition, moyens à mobiliser |
| Comparateur | Deux wilayas côte à côte |
| Méthode | Sources, formule, sensibilité, limites, déclaration IA |

**Principe : une seule source.** L'application lit `wilayas.csv` (13 lignes) et se contente de l'afficher. Indice, rang, priorité, mécanisme et explications sont calculés en amont. Seule exception assumée : l'allocation du simulateur.

---

## Lancer le projet

### Voir le prototype

Ouvrir `index.html` dans un navigateur. Rien d'autre n'est nécessaire.

Servi par un serveur HTTP, un fichier `wilayas.csv` placé à côté remplace les données embarquées au chargement — l'interface suit sans qu'aucun code ne change.

### Refaire l'analyse depuis les données brutes

```bash
pip install pyreadstat pandas openpyxl shapely
python analyse.py   # croisement des bases, indicateurs, indice -> wilayas_detail.csv
python dataset.py   # noms et explications AR / EN             -> wilayas.csv
python actions.py   # recommandations chiffrees par wilaya     -> wilayas.csv
python carte.py     # frontieres Natural Earth -> chemins SVG  -> carte.json
python build.py     # assemblage                               -> index.html
python verif.py     # 102 tests automatises (Playwright)
```

`analyse.py` affiche tous les contrôles nationaux à l'exécution.

### Les tests

102 tests couvrent la géométrie de la carte, l'absence de débordement sur mobile et en RTL, la somme des grilles de 100, la conservation de la capacité du simulateur sous les trois règles, le contraste du texte sur les quatre niveaux de priorité, la traduction des trois langues et le comportement en cas de valeur manquante.

---

## Structure du dépôt

```
index.html               Le prototype complet, autonome
wilayas.csv              Les 13 lignes de donnees, 21 colonnes
wilayas.xlsx             Les memes donnees pour Excel
carte.json               Frontieres des wilayas en chemins SVG (6 Ko)

analyse.py               EPCV x population -> indicateurs et indice
dataset.py               Traductions arabe et anglais
actions.py               Recommandations chiffrees par wilaya
carte.py                 Natural Earth -> chemins SVG
build.py                 Assemblage du fichier final
verif.py                 Suite de tests
rapport_docx.js          Generation du rapport Word
explorations/            Maquettes de conception (palettes, themes, apercus)

RAPPORT_ANALYSE.md       Rapport d'analyse complet
EduFocus_Rapport_Analyse.docx
NOTICE_EQUIPE.md         Notice de mise en service
```

---

## Données et licences

**Les données brutes de l'EPCV ne sont pas incluses dans ce dépôt.** Elles ont été obtenues auprès de l'ANSADE et restent accessibles sur demande auprès de l'Agence. Seules les données agrégées par wilaya (13 lignes) sont publiées.

### Sources

1. **Population par wilaya, 2013-2019** — base fournie par l'organisation du hackathon, IndabaX Mauritanie, Édition 2026.
2. **Enquête Permanente sur les Conditions de Vie des ménages (EPCV 2019)** — Agence Nationale de la Statistique et de l'Analyse Démographique et Économique (ANSADE), République Islamique de Mauritanie. Extrait exploité : 60 600 individus, 13 wilayas.
3. **Fond de carte** — Natural Earth, admin-1, domaine public, simplifié à 1,2 km.
4. **Polices** — Poppins, Nunito Sans, IBM Plex Sans Arabic, Amiri (SIL Open Font License 1.1).
5. **Normes minimales de l'INEE** — 40 élèves par enseignant maximum au primaire, hypothèse par défaut du simulateur, modifiable par l'utilisateur.

Aucune bibliothèque graphique externe : carte, anneaux et graphiques sont écrits en SVG.

### Usage de l'intelligence artificielle

Déclaré conformément à l'article 5 du règlement du hackathon. Le détail figure dans l'écran **Méthode**, section 7, du prototype.

---

## Limites

- L'EPCV est un **échantillon** : les taux sont des estimations. La marge d'erreur va de ±1,7 point à Nouakchott à ±4,5 points en Inchiri.
- L'extrait exploité **ne comporte pas de pondération de sondage**.
- Les taux datent de **2019** et sont appliqués à la population 2019.
- Nous mesurons si l'enfant **est déjà allé** à l'école, pas s'il y est aujourd'hui.
- Nous ne mesurons **ni la qualité** de l'enseignement, ni la distance à l'école, ni le nombre d'enseignants disponibles.
- **Aucune prédiction** : EduFocus décrit une situation observée et la rend comparable.
- **Aucun coût chiffré** : convertir des enfants en ouguiyas sans données de coût fiables serait une invention.

---

## Équipe

_(compléter : noms des membres et rôles)_

Les projets développés pendant le hackathon restent la propriété de leurs créateurs (article 9 du règlement).
