# -*- coding: utf-8 -*-
import json
from reportlab.pdfbase.pdfmetrics import stringWidth
CH = {f['field_id']: f['rect'] for f in json.load(open('fields.json'))}
PG = {f['field_id']: f['page'] for f in json.load(open('fields.json'))}
LIEN = 'https://edufocuspro.netlify.app'

V = {
'equipe': 'DataSphere',
'date_jour': '01',
'date_mois': '08',

'contexte_probleme':
"La démographie ne décrit pas seulement une population : elle détermine où apparaîtront les besoins publics "
"de demain. En Mauritanie, pays où 63 % de la population a moins de 25 ans, ces besoins concernent d'abord "
"l'éducation.\n\n"
"Pourtant, la population est inégalement répartie. Alors que Nouakchott concentre une grande partie de la "
"croissance démographique, plusieurs wilayas rurales supportent la plus forte pression des jeunes "
"générations. Notre analyse montre que 365 231 enfants n'ont jamais fréquenté l'école formelle, dont 71 % "
"vivent dans seulement cinq wilayas.\n\n"
"Les données existent, mais elles restent difficiles à transformer en décision. La base démographique décrit "
"les populations, l'EPCV décrit les situations sociales : séparées, elles ne répondent pas à la question "
"essentielle : où faut-il investir en priorité, et pourquoi ?\n\n"
"Un pourcentage ne construit pas une école. Un décideur planifie pour des enfants, pas pour des taux. "
"EduFocus répond précisément à cette question en transformant des données démographiques en décisions "
"publiques.",

'description_solution':
"EduFocus est une plateforme interactive d'aide à la décision qui transforme des données démographiques en "
"recommandations opérationnelles. À partir des données de population et de l'EPCV, l'application classe les "
"13 wilayas selon un Indice de Priorité Éducative et explique, pour chacune, les causes de son classement "
"et les actions les plus adaptées. Elle comprend un tableau de bord national, une carte interactive, un "
"classement, une fiche détaillée par wilaya, un comparateur et un simulateur.\n\n"
"Sa principale innovation est son approche explicative : EduFocus ne montre pas uniquement où intervenir, il "
"explique pourquoi et comment. Deux wilayas présentant un niveau d'exclusion similaire peuvent ainsi "
"recevoir des recommandations totalement différentes selon leur contexte démographique et social.",

'approche_technique':
"Deux sources ont été combinées : la base démographique fournie dans le cadre du hackathon et l'EPCV 2019 de "
"l'ANSADE.\n\n"
"Un pipeline Python assure la préparation des données, leur fusion par wilaya, la conversion des "
"pourcentages en effectifs réels, le calcul de l'Indice de Priorité Éducative puis la génération automatique "
"des diagnostics et recommandations.\n\n"
"L'application sépare entièrement le traitement statistique de l'interface utilisateur : les calculs sont "
"réalisés en amont, tandis que l'application affiche les résultats dans une interface HTML/CSS/JavaScript "
"légère, fonctionnant hors connexion et sans dépendance externe. Cette architecture facilite les futures "
"mises à jour des données sans remettre en cause l'application elle-même.",

'resultats_obtenus':
"EduFocus identifie 365 231 enfants hors école, établit un classement complet des 13 wilayas et fournit, "
"pour chacune, un diagnostic, une explication et un levier d'action.\n\n"
"L'analyse montre surtout que les inégalités éducatives en Mauritanie sont avant tout territoriales : un "
"même taux peut cacher des réalités très différentes. En croisant les données démographiques et sociales, "
"EduFocus transforme des statistiques dispersées en décisions directement exploitables.",

'impact_perspectives':
"EduFocus transforme des données démographiques en un outil d'aide à la décision permettant de prioriser "
"objectivement les investissements publics. En identifiant où les besoins sont les plus importants, il aide "
"les décideurs à mieux cibler les ressources, réduire les inégalités territoriales et maximiser l'impact des "
"investissements éducatifs.\n\n"
"Au-delà de l'éducation, la même approche est applicable à d'autres politiques publiques dépendantes de la "
"répartition de la population, notamment la santé, les infrastructures et la protection sociale.\n\n"
"Conçue pour évoluer, la plateforme pourra intégrer de nouvelles enquêtes statistiques, des indicateurs "
"d'infrastructures et une analyse à l'échelle des moughataas afin d'accompagner durablement la planification "
"publique en Mauritanie.\n\n"
"Prototype : " + LIEN + "     Code source : github.com/tidjanecheikh5-lab/Edufocus",
}

def lignes(txt, larg, taille=9):
    n = 0
    for para in txt.split('\n'):
        cur, l = '', 1
        for m in para.split(' '):
            essai = (cur + ' ' + m).strip()
            if stringWidth(essai, 'Helvetica', taille) > larg - 8:
                l += 1; cur = m
            else:
                cur = essai
        n += l
    return n

print(f"{'champ':24}{'lignes':>8}{'capacité':>10}   état")
ok = True
for k, v in V.items():
    l, b, r, t = CH[k]
    dispo = int((t - b - 4) / 10.4)
    n = lignes(v, r - l)
    if n > dispo: ok = False
    print(f"{k:24}{n:>8}{dispo:>10}   {'OK' if n<=dispo else f'DEBORDE de {n-dispo}'}")
print('\nTOUT TIENT' if ok else '\nA RACCOURCIR')
json.dump([{'field_id': k, 'page': PG[k], 'description': k, 'value': v} for k, v in V.items()],
          open('field_values.json', 'w'), ensure_ascii=False, indent=1)
