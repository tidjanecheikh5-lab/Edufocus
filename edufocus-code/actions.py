# -*- coding: utf-8 -*-
"""Ajoute à wilayas.csv des recommandations d'action chiffrées, propres à chaque
wilaya, en français, arabe et anglais.

Chaque action est écrite « titre::détail ». Les actions sont séparées par « | ».
Hypothèse affichée dans l'application : 40 élèves par salle de classe.
"""
import pandas as pd

ELEVES_PAR_SALLE = 40
d = pd.read_csv('/home/claude/edufocus/wilayas.csv')

def n_fr(v): return f"{int(round(v)):,}".replace(',', '\u202f')
def n_en(v): return f"{int(round(v)):,}"
def p_fr(v, k=0): return f"{v:.{k}f}".replace('.', ',') + ' %'
def p_en(v, k=0): return f"{v:.{k}f} %"

lignes = []
for r in d.itertuples():
    sans   = round(r.pct_aucune_instruction / 100 * r.enfants_6_14)
    mahad  = round(r.pct_mahadra / 100 * r.enfants_6_14)
    salles = round(r.enfants_hors_ecole / ELEVES_PAR_SALLE)
    s_sans = round(sans / ELEVES_PAR_SALLE)
    ecart  = r.taux_garcons - r.taux_filles
    fr, ar, en = [], [], []

    # ── Action 1 : le levier principal, selon le mécanisme ────────────────
    if r.mecanisme == 'Exclusion':
        fr.append((f"Ouvrir des écoles",
            f"{n_fr(sans)} enfants ne reçoivent aucune instruction. Il faut environ "
            f"{n_fr(s_sans)} salles de classe pour les accueillir."))
        en.append(("Open schools",
            f"{n_en(sans)} children receive no instruction at all. About {n_en(s_sans)} "
            f"classrooms are needed to take them in."))
        ar.append(("فتح مدارس",
            f"{n_en(sans)} طفلاً لا يتلقون أي تعليم. يلزم نحو {n_en(s_sans)} قاعة دراسية "
            f"لاستقبالهم."))
    elif r.mecanisme == 'Substitution':
        fr.append((f"Créer des passerelles",
            f"{n_fr(mahad)} enfants sont en mahadra ou école coranique. Ils apprennent déjà : "
            f"il faut reconnaître leurs acquis et leur ouvrir l'accès au diplôme."))
        en.append(("Build bridges",
            f"{n_en(mahad)} children attend a mahadra or Quranic school. They are already "
            f"learning: recognise what they know and open the path to a qualification."))
        ar.append(("إنشاء جسور",
            f"{n_en(mahad)} طفلاً يدرسون في المحظرة أو الكتّاب. هم يتعلمون بالفعل: يجب "
            f"الاعتراف بمكتسباتهم وفتح الطريق أمامهم نحو الشهادة."))
    else:
        fr.append((f"Augmenter la capacité d'accueil",
            f"{n_fr(r.enfants_hors_ecole)} enfants hors école, soit environ {n_fr(salles)} "
            f"salles de classe et les enseignants qui vont avec."))
        en.append(("Increase intake capacity",
            f"{n_en(r.enfants_hors_ecole)} children out of school — about {n_en(salles)} "
            f"classrooms and the teachers to staff them."))
        ar.append(("رفع الطاقة الاستيعابية",
            f"{n_en(r.enfants_hors_ecole)} طفلاً خارج المدرسة، أي نحو {n_en(salles)} قاعة "
            f"دراسية والمدرسين اللازمين لها."))

    # ── Action 2 : le second volet éducatif ───────────────────────────────
    if r.mecanisme == 'Substitution' and sans > 0:
        fr.append((f"Ne pas oublier les enfants sans aucune instruction",
            f"{n_fr(sans)} enfants ne sont nulle part, ni à l'école ni en mahadra. Les "
            f"passerelles ne les atteindront pas : il leur faut une école."))
        en.append(("Do not forget children with no instruction",
            f"{n_en(sans)} children are nowhere — neither school nor mahadra. Bridges will "
            f"not reach them: they need a school."))
        ar.append(("عدم نسيان الأطفال بلا أي تعليم",
            f"{n_en(sans)} طفلاً ليسوا في أي مكان، لا في المدرسة ولا في المحظرة. الجسور لن "
            f"تصل إليهم: يحتاجون إلى مدرسة."))
    elif mahad > 0:
        fr.append((f"S'appuyer sur les mahadras existantes",
            f"{n_fr(mahad)} enfants y suivent déjà un enseignement. Les certifier coûte moins "
            f"cher que de construire, et donne un résultat plus vite."))
        en.append(("Build on the existing mahadras",
            f"{n_en(mahad)} children already study there. Certifying them costs less than "
            f"building and delivers results faster."))
        ar.append(("الاعتماد على المحاظر القائمة",
            f"{n_en(mahad)} طفلاً يدرسون فيها بالفعل. اعتمادها أقل كلفة من البناء ويعطي "
            f"نتيجة أسرع."))

    # ── Action 3 : la condition d'accès dominante ─────────────────────────
    if r.taux_pauvrete >= 35:
        fr.append((f"Lever l'obstacle du coût",
            f"{p_fr(r.taux_pauvrete)} de la population vit dans la pauvreté. Cantines "
            f"scolaires, gratuité des fournitures et transferts aux familles conditionnent "
            f"la fréquentation réelle."))
        en.append(("Remove the cost barrier",
            f"{p_en(r.taux_pauvrete)} of the population lives in poverty. School canteens, "
            f"free supplies and cash transfers to families decide whether children actually "
            f"attend."))
        ar.append(("رفع عائق التكلفة",
            f"{p_en(r.taux_pauvrete)} من السكان يعيشون في فقر. المطاعم المدرسية ومجانية "
            f"اللوازم والتحويلات للأسر هي ما يحدد الحضور الفعلي."))
    elif r.part_rurale >= 60:
        fr.append((f"Rapprocher l'école des familles",
            f"{p_fr(r.part_rurale)} de la population vit à la campagne. Mieux vaut plusieurs "
            f"petites écoles de proximité qu'un grand établissement loin de tout."))
        en.append(("Bring school closer to families",
            f"{p_en(r.part_rurale)} of the population lives in rural areas. Several small "
            f"local schools work better than one large one far from everything."))
        ar.append(("تقريب المدرسة من الأسر",
            f"{p_en(r.part_rurale)} من السكان يعيشون في الريف. عدة مدارس صغيرة قريبة أفضل "
            f"من مؤسسة كبيرة بعيدة عن كل شيء."))
    else:
        fr.append((f"Cibler les quartiers, pas la wilaya",
            f"Le milieu est majoritairement urbain ({p_fr(100-r.part_rurale)}). Le besoin "
            f"n'est pas réparti également : il se concentre dans les quartiers périphériques."))
        en.append(("Target neighbourhoods, not the wilaya",
            f"The area is mostly urban ({p_en(100-r.part_rurale)}). The need is not evenly "
            f"spread: it concentrates in outlying neighbourhoods."))
        ar.append(("استهداف الأحياء لا الولاية",
            f"الوسط حضري في معظمه ({p_en(100-r.part_rurale)}). الحاجة ليست موزعة بالتساوي: "
            f"إنها تتركز في الأحياء الطرفية."))

    # ── Action 4 : l'écart garçons-filles, seulement s'il est net ─────────
    if abs(ecart) >= 4:
        qui_fr, qui_en, qui_ar = ("les garçons", "boys", "الأولاد") if ecart > 0 \
                            else ("les filles", "girls", "البنات")
        e = abs(ecart)
        fr.append((f"Viser d'abord {qui_fr}",
            f"L'écart atteint {e:.1f} points au détriment de {qui_fr}".replace('.', ',') +
            f". C'est l'un des écarts les plus marqués du pays : une campagne ciblée est justifiée."))
        en.append((f"Target {qui_en} first",
            f"The gap reaches {e:.1f} points against {qui_en}. It is one of the widest in the "
            f"country: a targeted campaign is warranted."))
        ar.append((f"استهداف {qui_ar} أولاً",
            f"يبلغ الفارق {e:.1f} نقطة على حساب {qui_ar}. وهو من أوسع الفوارق في البلاد: "
            f"حملة موجّهة لها ما يبررها."))

    j = lambda xs: ' | '.join(f"{a}::{b}" for a, b in xs)
    lignes.append((j(fr), j(ar), j(en), sans, mahad, salles))

d['actions'], d['actions_ar'], d['actions_en'], \
    d['enfants_sans_instruction'], d['enfants_mahadra'], d['salles_necessaires'] = zip(*lignes)

d.to_csv('/home/claude/edufocus/wilayas.csv', index=False, encoding='utf-8-sig')
print(f"{len(d)} wilayas · {sum(x[0].count('::') for x in lignes)} actions générées\n")
for r in d.sort_values('rang').head(3).itertuples():
    print(f"═══ {r.wilaya} ({r.mecanisme})")
    for a in r.actions.split(' | '):
        ti, de = a.split('::')
        print(f"   ▸ {ti}\n     {de}")
    print()
