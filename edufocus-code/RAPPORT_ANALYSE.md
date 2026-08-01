# EduFocus — Rapport d'analyse

**IndabaX Mauritanie 2026 · Équipe DataSphere**
Thème : From Data to Storytelling · Population & Démographie
Document technique accompagnant le prototype. Tous les calculs sont reproductibles
avec les scripts fournis.

---

## 1. Les deux sources

### 1.1 Base population par wilaya, 2013-2019

Fournie par l'organisation du hackathon. Fichier `Population.xlsx`, feuille `Data`.
Une ligne par région, une colonne par année. Elle donne le **nombre d'habitants**.

Population 2019 retenue pour la Mauritanie : **4 077 347 habitants**.

### 1.2 EPCV 2019 — Enquête Permanente sur les Conditions de Vie des ménages

Produite par l'ANSADE. **Cette base ne fait pas partie des données du hackathon** :
elle a été obtenue auprès de l'Agence, producteur officiel des statistiques
démographiques et de pauvreté du pays.

Fichier SPSS, **60 600 individus**, 11 variables, 13 wilayas. Aucune valeur
manquante sur les variables utilisées.

| Variable | Libellé | Modalités |
|---|---|---|
| `wilaya` | Wilaya | 13 |
| `Groupe_age` | Groupe d'âge | 1 = 0-5 · **2 = 6-14** · 3 = 15-24 · 4 = 25-59 · 5 = 60+ |
| `C2` | Est-ce que [NOM] est déjà allé à l'école | voir §3 |
| `B2` | Sexe | 1 = Masculin · 2 = Féminin |
| `milieu` | Milieu | 1 = Urbain · 2 = Rural |
| `pauv` | Prévalence de la pauvreté | 0 / 1 |

Sous-échantillon des 6-14 ans : **16 451 enfants**.

---

## 2. Le croisement des deux bases

### 2.1 La clé de jointure

Les deux bases sont reliées par la **wilaya**. Les libellés diffèrent d'une base à
l'autre ; une table de correspondance explicite a été écrite plutôt qu'un
rapprochement automatique, pour éviter toute erreur d'appariement silencieuse.

| Libellé EPCV | Libellé base population | Nom retenu |
|---|---|---|
| Hodh charghy | El Hodh El Charghi | Hodh El Charghi |
| Hodh Gharby | El Hodh El Gharbi | Hodh El Gharbi |
| Dakhlett Nouadibou | D. Nouadhibou | Dakhlet Nouadhibou |
| Guidimagha | Guidimakha | Guidimakha |
| Tirs-ezemour | Tiris Zemour | Tiris Zemmour |
| Assaba, Gorgol, Brakna, Trarza, Adrar, Tagant, Inchiri, Nouakchott | identiques | identiques |

Les 13 wilayas s'apparient sans reste.

### 2.2 Le principe : transformer des pourcentages en enfants

L'EPCV donne des **taux** sur un échantillon. La base population donne des
**effectifs**. Multipliés, ils donnent des effectifs réels par wilaya.

Pour chaque wilaya *w* :

```
part_6_14(w)      = proportion d'individus avec Groupe_age = 2 dans l'EPCV
enfants_6_14(w)   = population_2019(w) × part_6_14(w)
taux_hors(w)      = proportion d'enfants 6-14 hors école formelle dans l'EPCV
enfants_hors(w)   = enfants_6_14(w) × taux_hors(w)
```

**Exemple — Guidimakha**

```
population_2019   = 308 457 habitants        (base population)
part_6_14         = 30,25 %                  (EPCV, 1 879 enfants sur 6 211 individus)
enfants_6_14      = 308 457 × 0,3025 = 93 317 enfants
taux_hors         = 44,4 %                   (EPCV, 835 enfants sur 1 879)
enfants_hors      = 93 317 × 0,444 = 41 469 enfants
```

C'est le cœur de la méthode : *44,4 %* ne se budgète pas, *41 469 enfants* se
budgète.

---

## 3. La définition de « hors école formelle »

La variable `C2` distingue cinq situations. Le regroupement retenu :

| Code | Modalité EPCV | Regroupement | National (6-14) |
|---|---|---|---|
| 3 | Oui, école formelle uniquement | **Scolarisé** | 27,5 % |
| 4 | Oui, école formelle et enseignement coranique | **Scolarisé** | 39,4 % |
| 1 | Oui, enseignement coranique uniquement | **Hors formel — substitution** | 16,2 % |
| 2 | Oui, Mahadra uniquement | **Hors formel — substitution** | 0,5 % |
| 5 | Non | **Hors formel — aucune instruction** | 16,4 % |

```
hors école formelle = C2 ∈ {1, 2, 5}   →  33,1 % au niveau national
```

**Un enfant qui fréquente à la fois l'école formelle et l'enseignement coranique
est compté comme scolarisé** (code 4). C'est un choix : il a accès au diplôme
reconnu.

### Point de vocabulaire à connaître

La catégorie appelée « mahadra » dans nos documents regroupe en réalité les codes
1 et 2, et elle est composée à **97 % d'enseignement coranique** (16,2 %) contre
seulement 0,5 % de mahadra à proprement parler.

L'interface dit correctement « mahadra ou école coranique ». **En revanche, toute
formulation qui parlerait de « mahadra » seule serait imprécise** et doit être
corrigée dans les supports de présentation.

### Pourquoi séparer les deux

C'est l'idée centrale du projet. Deux wilayas au même taux hors école peuvent
avoir des problèmes opposés :

| | Hodh El Gharbi | Guidimakha |
|---|---|---|
| Taux hors école formelle | 47,2 % | 44,4 % |
| Coranique ou mahadra | **32,9 %** | 1,9 % |
| Aucune instruction | 14,3 % | **42,5 %** |
| Levier | Passerelles | Écoles |

Au Hodh El Gharbi les enfants **apprennent** mais sans diplôme reconnu : il faut
des équivalences. Au Guidimakha ils ne sont **nulle part** : il faut des écoles.
Un classement par taux seul ne voit pas cette différence.

---

## 4. Les indicateurs construits

Tous calculés par wilaya sur l'EPCV, puis appliqués à la population 2019.

| Indicateur | Calcul | Population de référence |
|---|---|---|
| `taux_hors_ecole` | part de `C2 ∈ {1,2,5}` | 6-14 ans |
| `pct_mahadra` | part de `C2 ∈ {1,2}` | 6-14 ans |
| `pct_aucune_instruction` | part de `C2 = 5` | 6-14 ans |
| `taux_garcons` / `taux_filles` | taux hors école par `B2` | 6-14 ans |
| `taux_pauvrete` | moyenne de `pauv` | tous individus |
| `part_rurale` | part de `milieu = 2` | tous individus |
| `ratio_dependance` | (0-14 ans) / (15-59 ans) × 100 | tous individus |

**Contrôle de validité** : le taux de pauvreté national calculé sur l'échantillon
donne **28,75 %**, proche du chiffre officiel EPCV 2019 (≈ 28,2 %). La variable
n'est pas inversée et le sens de codage est confirmé.

---

## 5. L'indice de priorité éducative

### 5.1 Formule

```
indice = 0,45 × volume + 0,35 × intensité + 0,20 × vulnérabilité
```

- **volume** = nombre d'enfants hors école
- **intensité** = taux hors école
- **vulnérabilité** = taux de pauvreté

### 5.2 Normalisation

Chaque composante est ramenée sur 0-100 par min-max sur les 13 wilayas :

```
normalisé(x) = (x − min) / (max − min) × 100
```

La wilaya la plus touchée du pays obtient 100, la moins touchée 0.

### 5.3 Justification des poids

- Le **volume** pèse le plus (45 %) parce qu'un budget se dépense en enfants, pas
  en pourcentages.
- L'**intensité** (35 %) corrige l'effet de taille : sans elle, les grandes wilayas
  écraseraient le classement.
- La **vulnérabilité** (20 %) rappelle qu'à situation scolaire égale, une wilaya
  pauvre dispose de moins de moyens propres.

### 5.3 bis Pourquoi 45 / 35 / 20 et pas d'autres chiffres

**Le raisonnement derrière chaque poids**

- **Volume 45 %** — seule des trois grandeurs à se traduire directement en salles
  et en enseignants. Poids majoritaire mais pas majorité absolue : à 50 % ou plus,
  le classement se réduit à un tri par population et Nouakchott passe première.
- **Intensité 35 %** — contrepoids du volume, presque aussi lourd, pour que les
  petites wilayas très touchées ne disparaissent pas derrière les grandes.
- **Vulnérabilité 20 %** — minoritaire à dessein. La pauvreté module la difficulté
  d'agir, elle ne mesure pas le problème scolaire.

**Analyse de sensibilité**

Le classement a été recalculé pour les **231 combinaisons de poids possibles** par
pas de 5 %, de 100/0/0 à 0/0/100.

| Wilaya | Dans le top 5 | Rang mini | Rang maxi |
|---|---|---|---|
| Guidimakha | **100 %** | 1 | 5 |
| Hodh El Gharbi | **100 %** | 1 | 5 |
| Assaba | **100 %** | 2 | 5 |
| Hodh El Charghi | 80 % | 1 | 10 |
| Gorgol | 45 % | 5 | 6 |
| Nouakchott | 33 % | 1 | 12 |
| Brakna | 22 % | 2 | 9 |
| Tagant | 20 % | 2 | 10 |
| Trarza, Inchiri, D. Nouadhibou, Tiris Zemmour, Adrar | **0 %** | 6 | 13 |

Guidimakha arrive première dans 67 % des combinaisons.

**Conclusion, énoncée sans complaisance.** Le classement fin *bouge* : seul un
tiers des combinaisons donne exactement le même top 5, et Hodh El Charghi peut
descendre au 10ᵉ rang si l'on ne retient que l'intensité. Nous ne prétendons pas
que 45/35/20 soit la seule pondération défendable.

En revanche, **l'ensemble des wilayas prioritaires est robuste** : trois y sont
quoi qu'on fasse, cinq n'y entrent jamais. Le choix des poids déplace l'ordre, pas
la décision. Un décideur privilégiant l'intensité investirait dans les mêmes
régions, dans un ordre différent.

La formule est affichée dans l'application : elle n'est pas là pour être crue,
elle est là pour être recalculée.

### 5.4 Résultat

| Rang | Wilaya | Volume | Intensité | Vulnér. | Indice | Priorité |
|---|---|---|---|---|---|---|
| 1 | Guidimakha | 62 | 93 | 100 | **81** | Très élevée |
| 2 | Hodh El Charghi | 90 | 84 | 33 | **77** | Très élevée |
| 3 | Hodh El Gharbi | 66 | 100 | 58 | **76** | Très élevée |
| 4 | Assaba | 73 | 86 | 55 | **74** | Élevée |
| 5 | Nouakchott | 100 | 45 | 8 | **62** | Élevée |
| 6 | Gorgol | 59 | 66 | 51 | **60** | Élevée |
| 7 | Trarza | 39 | 62 | 33 | **46** | Moyenne |
| 8 | Brakna | 35 | 47 | 69 | **46** | Moyenne |
| 9 | Tagant | 9 | 59 | 69 | **38** | Moyenne |
| 10 | Inchiri | 0 | 26 | 40 | **17** | Faible |
| 11 | Dakhlet Nouadhibou | 9 | 37 | 0 | **17** | Faible |
| 12 | Tiris Zemmour | 2 | 25 | 15 | **12** | Faible |
| 13 | Adrar | 0 | 0 | 41 | **8** | Faible |

Détail du calcul pour Guidimakha :
`0,45 × 62,3 + 0,35 × 93,2 + 0,20 × 100 = 28,0 + 32,6 + 20,0 = 80,6 → 81`

### 5.5 Deux résultats à savoir défendre

**Nouakchott a le plus d'enfants hors école du pays (65 995) mais n'est que 5e.**
Son volume est maximal (100/100), mais son taux est faible (24,8 %, intensité 45)
et c'est la wilaya la moins pauvre (13,1 %, vulnérabilité 8).

**Hodh El Gharbi a le pire taux du pays (47,2 %) mais n'est que 3e.** Elle compte
moins d'enfants et moins de pauvreté que Guidimakha.

Ces deux cas montrent que l'indice ne se contente pas de reclasser une seule
colonne.

---

## 6. Le mécanisme et le levier

Une règle explicite attribue à chaque wilaya un mécanisme dominant, et donc un
levier d'action.

```
part_aucune    = pct_aucune_instruction / taux_hors_ecole × 100
part_nationale = enfants_hors_ecole / total national × 100

si part_nationale ≥ 15 % et taux_hors_ecole < 33,1 %  →  Volume élevé
sinon si part_aucune < 50 %                           →  Substitution
sinon                                                 →  Exclusion
```

| Mécanisme | Signification | Levier | Wilayas |
|---|---|---|---|
| **Exclusion** | La majorité des enfants hors école ne reçoit aucune instruction | Créer de l'offre scolaire, cantines, transferts | Guidimakha, Gorgol, Brakna, Tagant, Dakhlet Nouadhibou, Tiris Zemmour |
| **Substitution** | La majorité est en coranique ou mahadra | Passerelles et équivalences | Hodh El Charghi, Hodh El Gharbi, Assaba, Trarza, Inchiri, Adrar |
| **Volume élevé** | Poids national fort, taux sous la moyenne | Capacité d'accueil | Nouakchott |

---

## 7. Le simulateur

### 7.1 Ce qu'il fait

L'utilisateur fixe une **capacité exprimée en enfants** — combien d'enfants il peut
scolariser — et choisit une règle de répartition. Aucune wilaya ne peut recevoir
plus de places qu'elle n'a d'enfants hors école ; le surplus est redistribué de
façon itérative.

| Règle | Principe |
|---|---|
| **Selon le nombre** | Part proportionnelle aux enfants hors école |
| **Les plus urgentes d'abord** | Ordre de l'indice, chaque wilaya réglée entièrement avant la suivante |
| **La même part pour chacune** | Partage égal entre les 13 |

### 7.2 Le résultat contre-intuitif

**Le taux national après simulation est identique pour les trois règles.** C'est
arithmétique : le nombre total d'enfants scolarisés ne dépend pas de la manière de
les répartir. Avec 100 000 places, il passe de 33,1 % à 24,2 % dans les trois cas.

Ce qui change est la **distribution** :

| 100 000 places | Wilayas entièrement réglées | La plus en retard reste à |
|---|---|---|
| Selon le nombre | 0 | 34,3 % |
| Les plus urgentes | 1 (Guidimakha à 0 %) | **47,2 %** (Hodh El Gharbi intact) |
| La même part | 5 (les petites) | 36,1 % |

Concentrer règle quelques wilayas et en laisse d'autres intactes. Étaler soulage
tout le monde sans régler personne. **L'arbitrage est politique, pas statistique.**
L'outil l'éclaire, il ne le tranche pas.

### 7.3 Pourquoi aucun coût n'est chiffré

Une place en école ne coûte pas ce que coûte une passerelle depuis une mahadra, et
nous ne disposons d'aucune donnée de coût fiable. Convertir des enfants en ouguiyas
serait une invention, pas une analyse.

### 7.4 Des enfants aux moyens matériels

Le simulateur convertit les places en moyens concrets à partir de **deux
hypothèses seulement**, toutes deux affichées à l'écran et modifiables :

| Hypothèse | Défaut | Source |
|---|---|---|
| Élèves par salle de classe | 40 | Normes minimales de l'INEE, maximum recommandé au primaire |
| Salles par école | 6 | Une salle par niveau du cycle fondamental |

Un enseignant est compté par salle. **Le type de moyen dépend du mécanisme** —
c'est ce qui distingue ce dimensionnement d'un simple produit en croix :

| Mécanisme | Moyen calculé | Raison |
|---|---|---|
| **Exclusion** et **Volume élevé** | Salles neuves **et** écoles pour les abriter | Voir la note ci-dessous |
| **Substitution** | Classes passerelles, mahadras à certifier | On ne construit pas une école pour un enfant qui apprend déjà : il lui faut une équivalence, pas un bâtiment |

**Pourquoi des constructions neuves dans les deux premiers cas.** Nous ne
disposons d'aucune donnée sur la capacité résiduelle des écoles existantes.
Supposer qu'elles pourraient absorber ces enfants serait une hypothèse que rien ne
soutient. Si le ministère connaît les places disponibles, son besoin de
construction sera inférieur au nôtre : **notre chiffre est un majorant, et c'est
volontaire.**

À 100 000 places réparties au prorata, cela donne 2 508 salles, 2 508 enseignants,
216 écoles neuves, et 49 205 enfants à faire passer de la mahadra vers le formel.

Si le ministère applique d'autres normes, il modifie les deux valeurs et
l'ensemble se recalcule. **Aucun coût n'est chiffré** — voir 7.3.

---

## 8. Les recommandations par wilaya

Trois à quatre actions chiffrées sont générées pour chaque wilaya à partir de ses
propres données, selon des règles fixes :

1. **Levier principal** — dicté par le mécanisme, chiffré en enfants et en salles
2. **Second volet éducatif** — l'autre catégorie, pour ne pas l'oublier
3. **Condition d'accès dominante** — pauvreté ≥ 35 % → lever l'obstacle du coût ;
   sinon ruralité ≥ 60 % → rapprocher l'école ; sinon cibler les quartiers
4. **Écart garçons-filles** — uniquement si l'écart atteint 4 points

Quatre wilayas déclenchent la quatrième action : Nouakchott (+6,5 points au
détriment des garçons), Trarza (+5,2), Tiris Zemmour (+5,2), Inchiri (+4,4).

Aucune recommandation creuse n'est produite là où l'écart n'est pas significatif.

---

## 9. Les résultats nationaux

| Indicateur | Valeur |
|---|---|
| Population 2019 | 4 077 347 |
| Part des 6-14 ans | 27,1 % |
| Enfants de 6 à 14 ans (somme des wilayas) | 1 095 211 |
| Enfants de 6 à 14 ans (estimation nationale directe) | 1 106 872 |
| **Enfants hors école formelle** | **365 231** |
| Taux hors école formelle | 33,1 % |
| dont coranique ou mahadra | 16,7 % — 194 075 enfants |
| dont aucune instruction | 16,4 % — 171 103 enfants |
| Concentration dans 5 wilayas | 71 % |
| Taux de pauvreté | 28,8 % |

### Répartition des 365 231 enfants hors école

| | Part | Effectif | Taux dans le groupe |
|---|---|---|---|
| Garçons | 52,4 % | 191 381 | 34,0 % |
| Filles | 47,6 % | 173 850 | 32,1 % |
| **Campagne** | **73,6 %** | **268 810** | **42,0 %** |
| Ville | 26,4 % | 96 421 | 20,8 % |

**La fracture n'est pas le genre — elle est territoriale.** L'écart garçons-filles
est de 1,9 point au niveau national ; l'écart ville-campagne est de 21,2 points,
soit plus du double de taux.

---

## 10. Limites

### 10.1 Précision de l'échantillon

L'EPCV est un échantillon. Les taux sont des estimations assorties d'une marge
d'erreur, calculée ici à 95 % de confiance.

| Wilaya | Enfants enquêtés | Taux | Marge |
|---|---|---|---|
| Nouakchott | 2 619 | 24,8 % | ± 1,7 |
| Hodh El Charghi | 2 293 | 40,7 % | ± 2,0 |
| Guidimakha | 1 879 | 44,4 % | ± 2,2 |
| Gorgol | 1 778 | 33,5 % | ± 2,2 |
| Assaba | 1 468 | 41,6 % | ± 2,5 |
| Brakna | 1 426 | 25,5 % | ± 2,3 |
| Hodh El Gharbi | 1 380 | 47,2 % | ± 2,6 |
| Trarza | 1 187 | 31,6 % | ± 2,6 |
| Adrar | 598 | 6,2 % | ± 1,9 |
| Dakhlet Nouadhibou | 594 | 21,2 % | ± 3,3 |
| Tagant | 483 | 30,2 % | ± 4,1 |
| Tiris Zemmour | 479 | 16,3 % | ± 3,3 |
| **Inchiri** | **267** | 16,9 % | **± 4,5** |

**Conséquence à assumer** : les écarts de rang entre wilayas voisines dans le
classement ne sont pas tous statistiquement significatifs. Guidimakha (44,4 ± 2,2)
et Hodh El Gharbi (47,2 ± 2,6) ont des intervalles qui se chevauchent.

### 10.2 Absence de pondération de sondage

L'extrait exploité **ne comporte pas de variable de pondération**. Les taux sont
calculés sur l'échantillon brut. Ils peuvent s'écarter légèrement des chiffres
officiels publiés par l'ANSADE.

**Conséquence mesurée.** L'échantillon n'est pas proportionnel à la population :
les petites wilayas y sont surreprésentées. Inchiri compte 24 425 habitants pour
267 enfants enquêtés, quand Nouakchott en compte 1 195 636 pour 2 619 enfants. Deux
façons d'estimer le nombre d'enfants de 6 à 14 ans divergent donc :

| Méthode | Résultat |
|---|---|
| Somme wilaya par wilaya — Σ(population_w × part_6_14_w) | **1 095 211** |
| Estimation nationale directe — population × part brute (27,15 %) | 1 106 872 |
| Écart | 11 661 enfants, soit 1,1 % |

**Nous retenons la première**, calculée wilaya par wilaya, parce qu'elle applique à
chaque territoire sa propre structure d'âge au lieu d'une moyenne nationale
influencée par la composition de l'échantillon.

Le chiffre central du projet — **365 231 enfants hors école** — est construit par
cette même méthode wilaya par wilaya. Il n'est pas affecté par ce biais.

En revanche, la formulation « 1 107 000 enfants en âge d'être scolarisés » qui
figure dans le document de soumission correspond à l'estimation nationale directe.
L'écart de 1,1 % avec la somme des wilayas doit être signalé si la question est
posée.

### 10.3 Ce que les données ne disent pas

- Les taux datent de **2019** et sont appliqués à la population 2019. Rien ne dit
  qu'ils sont encore valables aujourd'hui.
- `C2` mesure si l'enfant est **déjà allé** à l'école, pas s'il y est aujourd'hui
  ni ce qu'il y apprend. Un enfant inscrit mais absent est compté comme scolarisé.
- Aucune mesure de la **qualité** de l'enseignement, de la distance à l'école, de
  l'état des bâtiments ni du nombre d'enseignants disponibles.
- **Aucune prédiction.** EduFocus décrit une situation observée et la rend
  comparable ; il ne dit pas ce qui se passera si l'on investit.

---

## 11. Reproductibilité

```bash
pip install pyreadstat pandas openpyxl shapely
python analyse.py   # croisement, indicateurs, indice   → wilayas_detail.csv
python dataset.py   # noms et explications AR / EN      → wilayas.csv
python actions.py   # recommandations chiffrées         → wilayas.csv
python carte.py     # frontières Natural Earth          → carte.json
python build.py     # assemblage                        → index.html
python verif.py     # 59 tests automatisés
```

`analyse.py` affiche tous les contrôles nationaux à l'exécution. Le prototype lit
une source unique, `wilayas.csv` (13 lignes) : aucun indicateur n'est recalculé
dans l'interface, à l'exception assumée de l'allocation du simulateur.

**59 tests automatisés** couvrent la géométrie de la carte, l'absence de
débordement sur mobile et en RTL, la somme des grilles de 100, la conservation de
la capacité du simulateur sous les trois règles, la traduction des trois langues et
le comportement en cas de valeur manquante.

---

## 12. Sources

1. **Population par wilaya, 2013-2019.** Base fournie par l'organisation du
   hackathon — IndabaX Mauritanie, Édition 2026.

2. **Enquête Permanente sur les Conditions de Vie des ménages (EPCV 2019).**
   Agence Nationale de la Statistique et de l'Analyse Démographique et Économique
   (ANSADE), République Islamique de Mauritanie. Extrait exploité : 60 600
   individus, 13 wilayas. Base obtenue auprès de l'ANSADE, accessible sur demande
   auprès de l'Agence.

3. **Fond de carte** : Natural Earth, admin-1 (domaine public), simplifié à 1,2 km.

4. **Ressources open source** : polices Poppins, Nunito Sans, IBM Plex Sans Arabic
   et Amiri (SIL Open Font License 1.1). Aucune bibliothèque graphique externe :
   carte, anneaux et graphiques sont écrits en SVG.

5. **Normes minimales de l'INEE** (Inter-Agency Network for Education in
   Emergencies) : 40 élèves par enseignant au maximum en primaire. Utilisé comme
   hypothèse par défaut du simulateur, modifiable par l'utilisateur.
