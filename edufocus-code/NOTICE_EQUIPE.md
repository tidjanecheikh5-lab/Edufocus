# EduFocus — notice de mise en service

**IndabaX Mauritanie 2026 · thème Population & Démographie**

---

## Ouvrir le prototype

Double-cliquez sur `index.html`. Il s'ouvre dans n'importe quel navigateur, **sans
serveur et sans connexion internet**. Les données sont embarquées dans la page.

Pour le montrer au jury sur téléphone, deux options :

- **Un lien** : déposez le dossier `edufocus/` sur Netlify Drop
  (netlify.com/drop — glisser-déposer, aucun compte requis) ou sur GitHub Pages.
  Vous obtenez une adresse en 30 secondes.
- **Sans réseau** : copiez `index.html` sur le téléphone et ouvrez-le depuis le
  gestionnaire de fichiers. Tout fonctionne.

---

## Remplacer les données

L'application lit **une seule source**. Si vous mettez un fichier `wilayas.csv`
à côté de `index.html` **et que la page est servie par un serveur** (lien web),
ce fichier remplace la copie embarquée au chargement.

En ouverture directe (`file://`), le navigateur interdit la lecture de fichiers
voisins : la page utilise alors sa copie interne. Pour changer les données dans
ce cas, relancez `python build.py` — cela réinjecte le CSV dans la page.

**Aucun indicateur n'est calculé dans l'interface.** Indice, rang, niveau de
priorité, mécanisme et explication viennent tous du fichier. Seule exception,
assumée et documentée dans l'écran Méthodologie (section 5) : l'allocation du
simulateur, qui est par nature un calcul.

Si une valeur manque, la page affiche `—` et ne casse pas. C'est testé.

---

## Les polices — à faire si vous avez 10 minutes

La page appelle IBM Plex et Amiri depuis Google Fonts. **Sans connexion au
moment de la démonstration, elle retombe sur Georgia + police système** :
lisible, mais ce n'est plus tout à fait votre charte, et l'arabe s'affichera
dans la police système du téléphone.

Pour rendre la page vraiment autonome :

1. Allez sur `google-webfonts-helper.herokuapp.com` (ou téléchargez les `.woff2`
   depuis fonts.google.com).
2. Récupérez **IBM Plex Sans Arabic** (400, 600, 700), **IBM Plex Serif** (600)
   et **Amiri** (400, 700).
3. Mettez les `.woff2` dans un dossier `fonts/` à côté de `index.html`.
4. Dans `index.html`, remplacez la balise `<link ... fonts.googleapis.com ...>`
   par des règles `@font-face` pointant vers `fonts/`.

Ce n'est pas indispensable — la page reste parfaitement utilisable sans — mais
si le wifi du lieu est incertain, ça vaut le quart d'heure.

---

## Refaire l'analyse depuis les données brutes

```bash
pip install pyreadstat pandas openpyxl shapely
python analyse.py     # EPCV + population  -> wilayas_detail.csv + contrôles
python dataset.py     # ajoute AR et EN    -> wilayas.csv
python carte.py       # frontières         -> carte.json   (nécessite ne10.geojson)
python build.py       # assemble           -> index.html
python verif.py       # 39 tests automatisés
```

`analyse.py` affiche à l'écran tous les contrôles nationaux. Si un chiffre ne
correspond plus à votre document de soumission, il apparaît là.

Le fond de carte vient de Natural Earth (admin-1, domaine public), fichier
`ne_10m_admin_1_states_provinces.geojson`, simplifié à 1,2 km. Les chemins SVG
finaux pèsent 6 Ko.

---

## Avant de soumettre

- [ ] **Remplir la déclaration d'usage de l'IA** (écran Méthodologie, section 6).
      Elle est vide et marquée « à compléter ». L'article 5 du règlement l'exige,
      et l'omettre est un motif de disqualification.
- [ ] Vérifier que le PDF descriptif (1 à 2 pages) et le visuel sont soumis
      via le formulaire **avant le 1er août 23h59**.
- [ ] Tester le lien sur un vrai téléphone, pas en redimensionnant la fenêtre.
- [ ] Décider qui montre quoi pendant les 7 à 10 minutes de démonstration.

---

## Ce que contient le dossier

| Fichier | Rôle |
|---|---|
| `index.html` | Le prototype complet, autonome (101 Ko) |
| `wilayas.csv` | Les 13 lignes de données, 21 colonnes |
| `wilayas.xlsx` | Les mêmes données, lisibles dans Excel |
| `analyse.py` | EPCV × population → indicateurs et indice |
| `dataset.py` | Ajout des noms et explications AR / EN |
| `carte.py` | Frontières Natural Earth → chemins SVG |
| `build.py` | Assemblage du fichier final |
| `verif.py` | 46 tests automatisés |
| `controles.txt` | Sortie des contrôles nationaux |
