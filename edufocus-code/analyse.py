# -*- coding: utf-8 -*-
"""
EduFocus — IndabaX Mauritanie 2026
Croisement EPCV 2019 (ANSADE, 60 600 individus) x Base population par wilaya 2013-2019
Sortie : wilayas.csv / wilayas.xlsx (13 lignes, 17 colonnes)
"""
import pyreadstat, pandas as pd, numpy as np, json

SAV = '/mnt/user-data/uploads/Projet_1_SPSS___Base_de_données__255012.sav'
XLS = '/mnt/user-data/uploads/Population.xlsx'

df, meta = pyreadstat.read_sav(SAV)
lab_w = meta.variable_value_labels['wilaya']

# ---------------------------------------------------------------- 1. POPULATION
pop = pd.read_excel(XLS, sheet_name='Data', header=0)
pop.columns = ['region'] + [str(int(float(c))) for c in pop.columns[1:]]
pop = pop[['region', '2013', '2019']].dropna()
pop['2019'] = pop['2019'].astype(int)

MAP = {  # libellé EPCV -> libellé base population
    'Hodh charghy': 'El Hodh El Charghi', 'Hodh Gharby': 'El Hodh El Gharbi',
    'Assaba': 'Assaba', 'Gorgol': 'Gorgol', 'Brakna': 'Brakna', 'Trarza': 'Trarza',
    'Adrar': 'Adrar', 'Dakhlett Nouadibou': 'D. Nouadhibou', 'Tagant': 'Tagant',
    'Guidimagha': 'Guidimakha', 'Tirs-ezemour': 'Tiris Zemour', 'Inchiri': 'Inchiri',
    'Nouakchott': 'Nouakchott'}
# noms d'affichage définitifs (français)
NOM = {
    'Hodh charghy': 'Hodh El Charghi', 'Hodh Gharby': 'Hodh El Gharbi', 'Assaba': 'Assaba',
    'Gorgol': 'Gorgol', 'Brakna': 'Brakna', 'Trarza': 'Trarza', 'Adrar': 'Adrar',
    'Dakhlett Nouadibou': 'Dakhlet Nouadhibou', 'Tagant': 'Tagant', 'Guidimakha': 'Guidimakha',
    'Guidimagha': 'Guidimakha', 'Tirs-ezemour': 'Tiris Zemmour', 'Inchiri': 'Inchiri',
    'Nouakchott': 'Nouakchott'}

pop2019 = dict(zip(pop['region'], pop['2019']))
pop2013 = dict(zip(pop['region'], pop['2013']))

# ---------------------------------------------------------------- 2. TAUX EPCV
df['w'] = df['wilaya'].map(lab_w)
enf = df[df['Groupe_age'] == 2].copy()          # 6-14 ans

# Définitions
#  formel        : C2 = 3 (école formelle seule) ou 4 (formelle + coranique)
#  mahadra/cor.  : C2 = 1 (coranique seul) ou 2 (mahadra seule)
#  aucune instr. : C2 = 5 (jamais allé nulle part)
enf['formel']  = enf['C2'].isin([3, 4]).astype(int)
enf['mahadra'] = enf['C2'].isin([1, 2]).astype(int)
enf['aucune']  = (enf['C2'] == 5).astype(int)
enf['hors']    = 1 - enf['formel']

rows = []
for code, lib in lab_w.items():
    d_all = df[df['wilaya'] == code]
    d_enf = enf[enf['wilaya'] == code]
    nom_pop = MAP[lib]
    P19 = pop2019[nom_pop]

    part_614   = (d_all['Groupe_age'] == 2).mean()
    enfants614 = int(round(P19 * part_614))

    t_hors = d_enf['hors'].mean() * 100
    t_mah  = d_enf['mahadra'].mean() * 100
    t_auc  = d_enf['aucune'].mean() * 100
    g = d_enf[d_enf['B2'] == 1]['hors'].mean() * 100
    f = d_enf[d_enf['B2'] == 2]['hors'].mean() * 100

    t_pauv  = d_all['pauv'].mean() * 100
    p_rural = (d_all['milieu'] == 2).mean() * 100

    jeunes  = d_all['Groupe_age'].isin([1, 2]).sum()       # 0-14
    actifs  = d_all['Groupe_age'].isin([3, 4]).sum()       # 15-59
    ratio   = jeunes / actifs * 100

    rows.append(dict(
        wilaya=NOM[lib], n_epcv=len(d_all), n_enf=len(d_enf),
        population_2019=P19, pop_2013=pop2013[nom_pop],
        part_614=part_614 * 100, enfants_6_14=enfants614,
        enfants_hors_ecole=int(round(enfants614 * t_hors / 100)),
        taux_hors_ecole=t_hors, taux_pauvrete=t_pauv, part_rurale=p_rural,
        taux_garcons=g, taux_filles=f,
        pct_mahadra=t_mah, pct_aucune_instruction=t_auc, ratio_dependance=ratio))

w = pd.DataFrame(rows)

# ---------------------------------------------------------------- 3. INDICE
def nrm(s):                                   # min-max 0-100
    return (s - s.min()) / (s.max() - s.min()) * 100

w['n_volume']        = nrm(w['enfants_hors_ecole'])
w['n_intensite']     = nrm(w['taux_hors_ecole'])
w['n_vulnerabilite'] = nrm(w['taux_pauvrete'])
w['indice_brut'] = 0.45 * w['n_volume'] + 0.35 * w['n_intensite'] + 0.20 * w['n_vulnerabilite']
w['indice'] = w['indice_brut'].round().astype(int)
w = w.sort_values('indice_brut', ascending=False).reset_index(drop=True)
w['rang'] = np.arange(1, len(w) + 1)

def niveau(r):
    return 'Très élevée' if r <= 3 else 'Élevée' if r <= 6 else 'Moyenne' if r <= 9 else 'Faible'
w['niveau_priorite'] = w['rang'].map(niveau)

# ---------------------------------------------------------------- 4. MÉCANISME
# part de l'exclusion "sèche" dans le total hors école formelle
w['part_aucune'] = w['pct_aucune_instruction'] / w['taux_hors_ecole'] * 100
tot_national = w['enfants_hors_ecole'].sum()
w['part_nationale'] = w['enfants_hors_ecole'] / tot_national * 100

def meca(r):
    # Volume élevé : la wilaya pèse >=15% du besoin national ET son taux est
    # sous la moyenne nationale -> le problème est la taille, pas l'intensité
    if r['part_nationale'] >= 15 and r['taux_hors_ecole'] < 33.10:
        return 'Volume élevé'
    return 'Substitution' if r['part_aucune'] < 50 else 'Exclusion'
w['mecanisme'] = w.apply(meca, axis=1)

LEVIER = {'Substitution': 'Passerelles et équivalences vers le formel',
          'Exclusion': "Création d'offre scolaire, cantines, transferts",
          'Volume élevé': "Capacité d'accueil : salles de classe, enseignants"}
w['levier'] = w['mecanisme'].map(LEVIER)

# ---------------------------------------------------------------- 5. EXPLICATION
def fr(n):
    return f"{n:,}".replace(',', '\u202f')
def pc(x, d=1):
    return f"{x:.{d}f}".replace('.', ',') + ' %'

def explique(r):
    t = (f"{r['wilaya']} est classé en priorité {r['niveau_priorite'].lower()} "
         f"(rang {r['rang']} sur 13). {fr(r['enfants_hors_ecole'])} enfants de 6 à 14 ans "
         f"n'ont jamais fréquenté l'école formelle, soit {pc(r['taux_hors_ecole'])} de cette "
         f"classe d'âge. Le taux de pauvreté y atteint {pc(r['taux_pauvrete'],0)} et "
         f"{pc(r['part_rurale'],0)} de la population vit en milieu rural. ")
    if r['mecanisme'] == 'Exclusion':
        t += (f"{pc(r['pct_aucune_instruction'])} des enfants ne reçoivent aucune instruction, "
              f"contre {pc(r['pct_mahadra'])} en mahadra ou école coranique : ces enfants sont "
              f"hors de tout circuit d'apprentissage. Le levier prioritaire est la création "
              f"d'offre scolaire.")
    elif r['mecanisme'] == 'Substitution':
        t += (f"{pc(r['pct_mahadra'])} des enfants suivent une mahadra ou une école coranique "
              f"et {pc(r['pct_aucune_instruction'])} seulement ne reçoivent aucune instruction : "
              f"la majorité apprend déjà, mais hors du système reconnu. Le levier prioritaire "
              f"est la passerelle vers le formel.")
    else:
        t += (f"La wilaya concentre à elle seule {pc(r['part_nationale'])} des enfants hors "
              f"école du pays alors que son taux reste sous la moyenne nationale "
              f"({pc(33.10)}) : le problème est un problème de masse. Le levier prioritaire "
              f"est la capacité d'accueil.")
    return t
w['explication'] = w.apply(explique, axis=1)

# ---------------------------------------------------------------- 6. EXPORT
COLS = ['wilaya', 'population_2019', 'enfants_6_14', 'enfants_hors_ecole', 'taux_hors_ecole',
        'taux_pauvrete', 'part_rurale', 'taux_garcons', 'taux_filles', 'pct_mahadra',
        'pct_aucune_instruction', 'ratio_dependance', 'indice', 'rang', 'niveau_priorite',
        'mecanisme', 'explication']
out = w[COLS].copy()
for c in ['taux_hors_ecole', 'taux_pauvrete', 'part_rurale', 'taux_garcons', 'taux_filles',
          'pct_mahadra', 'pct_aucune_instruction']:
    out[c] = out[c].round(1)
out['ratio_dependance'] = out['ratio_dependance'].round().astype(int)

out.to_csv('/home/claude/edufocus/wilayas.csv', index=False, encoding='utf-8-sig')
w.to_csv('/home/claude/edufocus/wilayas_detail.csv', index=False, encoding='utf-8-sig')
out.to_json('/home/claude/edufocus/wilayas.json', orient='records', force_ascii=False, indent=1)

# ---------------------------------------------------------------- 7. CONTRÔLES
pop_nat = pop2019['Mauritania']
part_nat = (df['Groupe_age'] == 2).mean()
enf_nat = pop_nat * part_nat
print('=' * 78)
print('CONTRÔLES NATIONAUX')
print('=' * 78)
print(f"Population 2019                    : {fr(pop_nat)}")
print(f"Part des 6-14 ans (EPCV)           : {pc(part_nat*100)}")
print(f"Enfants 6-14 ans (national)        : {fr(int(round(enf_nat)))}")
print(f"Taux hors école formelle national  : {pc(enf['hors'].mean()*100)}")
print(f"  dont mahadra/coranique seule     : {pc(enf['mahadra'].mean()*100)}")
print(f"  dont aucune instruction          : {pc(enf['aucune'].mean()*100)}")
print(f"Enfants hors école (somme wilayas) : {fr(tot_national)}")
top5 = w.nlargest(5, 'enfants_hors_ecole')
print(f"Concentration top 5 wilayas        : {pc(top5['enfants_hors_ecole'].sum()/tot_national*100,0)}"
      f"  -> {', '.join(top5['wilaya'])}")
print(f"Taux de pauvreté national          : {pc(df['pauv'].mean()*100)}")
print(f"Ratio dép. Gorgol / Nouakchott     : "
      f"{w.loc[w.wilaya=='Gorgol','ratio_dependance'].iloc[0]:.0f} / "
      f"{w.loc[w.wilaya=='Nouakchott','ratio_dependance'].iloc[0]:.0f}")
cro = (pop2019['Nouakchott']-pop2013['Nouakchott'])/(pop_nat-pop2013['Mauritania'])*100
print(f"Part de Nouakchott dans la croissance 2013-2019 : {pc(cro,0)}")
print()
print('=' * 78)
print('CLASSEMENT')
print('=' * 78)
show = w[['rang','wilaya','indice','enfants_hors_ecole','taux_hors_ecole','pct_mahadra',
          'pct_aucune_instruction','taux_pauvrete','part_rurale','taux_garcons','taux_filles',
          'ratio_dependance','niveau_priorite','mecanisme','n_enf']].copy()
for c in show.select_dtypes('float').columns: show[c]=show[c].round(1)
print(show.to_string(index=False))
