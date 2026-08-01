# -*- coding: utf-8 -*-
"""wilayas.csv enrichi : noms + explications en français, arabe et anglais."""
import pandas as pd, json

w = pd.read_csv('/home/claude/edufocus/wilayas_detail.csv')

AR = {'Hodh El Charghi': 'الحوض الشرقي', 'Hodh El Gharbi': 'الحوض الغربي', 'Assaba': 'لعصابة',
      'Gorgol': 'كوركول', 'Brakna': 'لبراكنة', 'Trarza': 'الترارزة', 'Adrar': 'أدرار',
      'Dakhlet Nouadhibou': 'داخلة نواذيبو', 'Tagant': 'تكانت', 'Guidimakha': 'كيدي ماغة',
      'Tiris Zemmour': 'تيرس زمور', 'Inchiri': 'إنشيري', 'Nouakchott': 'نواكشوط'}
EN = {k: k for k in AR}
EN['Hodh El Charghi'] = 'Hodh Ech Chargui'

NIV_AR = {'Très élevée': 'قصوى', 'Élevée': 'عالية', 'Moyenne': 'متوسطة', 'Faible': 'منخفضة'}
NIV_EN = {'Très élevée': 'very high', 'Élevée': 'high', 'Moyenne': 'medium', 'Faible': 'low'}

def n_fr(v): return f"{int(v):,}".replace(',', '\u202f')
def n_en(v): return f"{int(v):,}"
def p_fr(v, d=1): return f"{v:.{d}f}".replace('.', ',') + ' %'
def p_en(v, d=1): return f"{v:.{d}f} %"

rows = []
for _, r in w.iterrows():
    nom, m = r['wilaya'], r['mecanisme']
    # ---------------------------------------------------------------- FRANÇAIS
    fr = (f"{nom} est classé en priorité {r['niveau_priorite'].lower()} "
          f"(rang {r['rang']} sur 13). {n_fr(r['enfants_hors_ecole'])} enfants de 6 à 14 ans "
          f"n'ont jamais fréquenté l'école formelle, soit {p_fr(r['taux_hors_ecole'])} de cette "
          f"classe d'âge. Le taux de pauvreté y atteint {p_fr(r['taux_pauvrete'],0)} et "
          f"{p_fr(r['part_rurale'],0)} de la population vit en milieu rural. ")
    en = (f"{EN[nom]} ranks {r['rang']} of 13, {NIV_EN[r['niveau_priorite']]} priority. "
          f"{n_en(r['enfants_hors_ecole'])} children aged 6 to 14 have never attended formal "
          f"school — {p_en(r['taux_hors_ecole'])} of that age group. The poverty rate reaches "
          f"{p_en(r['taux_pauvrete'],0)} and {p_en(r['part_rurale'],0)} of the population lives "
          f"in rural areas. ")
    ar = (f"تُصنَّف ولاية {AR[nom]} ضمن أولوية {NIV_AR[r['niveau_priorite']]} "
          f"(الرتبة {r['rang']} من 13). {n_en(r['enfants_hors_ecole'])} طفلاً تتراوح أعمارهم بين 6 و14 سنة "
          f"لم يلتحقوا قط بالمدرسة النظامية، أي {p_en(r['taux_hors_ecole'])} من هذه الفئة العمرية. "
          f"يبلغ معدل الفقر {p_en(r['taux_pauvrete'],0)} ويعيش {p_en(r['part_rurale'],0)} من السكان "
          f"في الوسط الريفي. ")

    if m == 'Exclusion':
        fr += (f"{p_fr(r['pct_aucune_instruction'])} des enfants ne reçoivent aucune instruction, "
               f"contre {p_fr(r['pct_mahadra'])} en mahadra ou école coranique : ces enfants sont "
               f"hors de tout circuit d'apprentissage. Le levier prioritaire est la création "
               f"d'offre scolaire.")
        en += (f"{p_en(r['pct_aucune_instruction'])} of children receive no instruction at all, "
               f"against {p_en(r['pct_mahadra'])} in mahadra or Quranic school: these children are "
               f"outside every learning path. The priority is to build schools.")
        ar += (f"{p_en(r['pct_aucune_instruction'])} من الأطفال لا يتلقون أي تعليم، مقابل "
               f"{p_en(r['pct_mahadra'])} في المحظرة أو الكتّاب: هؤلاء الأطفال خارج كل مسار تعليمي. "
               f"الأولوية هي بناء المدارس.")
    elif m == 'Substitution':
        fr += (f"{p_fr(r['pct_mahadra'])} des enfants suivent une mahadra ou une école coranique "
               f"et {p_fr(r['pct_aucune_instruction'])} seulement ne reçoivent aucune instruction : "
               f"la majorité apprend déjà, mais hors du système reconnu. Le levier prioritaire est "
               f"la passerelle vers le formel.")
        en += (f"{p_en(r['pct_mahadra'])} of children attend a mahadra or Quranic school and only "
               f"{p_en(r['pct_aucune_instruction'])} receive no instruction: most are already "
               f"learning, but outside the recognised system. The priority is bridges into formal "
               f"schooling.")
        ar += (f"{p_en(r['pct_mahadra'])} من الأطفال يدرسون في المحظرة أو الكتّاب و"
               f"{p_en(r['pct_aucune_instruction'])} فقط لا يتلقون أي تعليم: الأغلبية تتعلم بالفعل "
               f"لكن خارج النظام المعترف به. الأولوية هي إنشاء جسور نحو التعليم النظامي.")
    else:
        fr += (f"La wilaya concentre à elle seule {p_fr(r['part_nationale'])} des enfants hors "
               f"école du pays alors que son taux reste sous la moyenne nationale (33,1 %) : "
               f"le problème est un problème de masse. Le levier prioritaire est la capacité "
               f"d'accueil.")
        en += (f"The wilaya alone holds {p_en(r['part_nationale'])} of the country's out-of-school "
               f"children while its rate stays below the national average (33.1 %): this is a "
               f"problem of scale. The priority is intake capacity.")
        ar += (f"تضم الولاية وحدها {p_en(r['part_nationale'])} من أطفال البلد خارج المدرسة، رغم أن "
               f"معدلها يبقى دون المعدل الوطني (33.1 %): المشكلة هنا مشكلة حجم. الأولوية هي الطاقة "
               f"الاستيعابية.")

    rows.append(dict(
        wilaya=nom, wilaya_ar=AR[nom], wilaya_en=EN[nom],
        population_2019=int(r['population_2019']), enfants_6_14=int(r['enfants_6_14']),
        enfants_hors_ecole=int(r['enfants_hors_ecole']),
        taux_hors_ecole=round(r['taux_hors_ecole'], 1),
        taux_pauvrete=round(r['taux_pauvrete'], 1), part_rurale=round(r['part_rurale'], 1),
        taux_garcons=round(r['taux_garcons'], 1), taux_filles=round(r['taux_filles'], 1),
        pct_mahadra=round(r['pct_mahadra'], 1),
        pct_aucune_instruction=round(r['pct_aucune_instruction'], 1),
        ratio_dependance=int(round(r['ratio_dependance'])), indice=int(r['indice']),
        rang=int(r['rang']), niveau_priorite=r['niveau_priorite'], mecanisme=m,
        explication=fr, explication_ar=ar, explication_en=en,
        n_echantillon=int(r['n_enf']), part_nationale=round(r['part_nationale'], 1)))

out = pd.DataFrame(rows)
out.to_csv('/home/claude/edufocus/wilayas.csv', index=False, encoding='utf-8-sig')
out.to_json('/home/claude/edufocus/wilayas.json', orient='records', force_ascii=False)
print(out[['rang', 'wilaya', 'wilaya_ar', 'indice', 'enfants_hors_ecole',
           'niveau_priorite', 'mecanisme']].to_string(index=False))
print('\nExemple FR :', out.iloc[0]['explication'][:150], '...')
print('Exemple AR :', out.iloc[0]['explication_ar'][:110], '...')
