# -*- coding: utf-8 -*-
"""Infographie EduFocus — A3 vertical (3508 x 4961 px à 300 dpi), rendue depuis SVG."""
import json, math, cairosvg, pandas as pd

C = json.load(open('/home/claude/edufocus/carte.json'))
d = pd.read_csv('/home/claude/edufocus/wilayas.csv').sort_values('rang')

W, H = 1200, 1697                      # A3 en unités SVG (ratio 1:1.414)
ACC, ACC2, ACC0 = '#1A4A6B', '#2A6B94', '#163F5C'
P1, P2, P3, P4 = '#1C4E70', '#3E799E', '#8FB3C9', '#CBDCE6'
OR, RI, FOND, TRAIT, ENCRE, GRIS = '#C08A2E', '#A6413B', '#F5F7F8', '#E2E6EA', '#171B1F', '#6A7480'
NIV = lambda r: P1 if r <= 3 else P2 if r <= 6 else P3 if r <= 9 else P4
fr = lambda n: f"{int(n):,}".replace(',', ' ')

s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"'
     f' font-family="Poppins, Trebuchet MS, sans-serif">']
s.append(f'<rect width="{W}" height="{H}" fill="{FOND}"/>')

def txt(x, y, t, size=16, fill=ENCRE, w='400', anchor='start', ls=0, op=1):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{w}" '
            f'text-anchor="{anchor}" letter-spacing="{ls}" opacity="{op}">{t}</text>')
def card(x, y, w, h, fill='#FFFFFF'):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" '
            f'stroke="{TRAIT}" stroke-width="1.5"/>')
def lab(x, y, t):
    return txt(x, y, t.upper(), 15, GRIS, '700', ls=2.4)

# ══ BANDEAU ═══════════════════════════════════════════════════════════
s.append(f'''<defs><radialGradient id="g" cx="50%" cy="0%" r="130%">
<stop offset="0" stop-color="{ACC2}"/><stop offset="55%" stop-color="{ACC}"/>
<stop offset="100%" stop-color="{ACC0}"/></radialGradient></defs>''')
s.append(f'<rect width="{W}" height="430" fill="url(#g)"/>')
s.append(txt(W/2, 74, 'INDABAX MAURITANIE 2026  ·  EQUIPE DATASPHERE'.replace('EQUIPE','ÉQUIPE'), 16,
             '#fff', '700', 'middle', 3.6, .62))
s.append(txt(W/2, 154, 'EduFocus', 78, '#fff', '800', 'middle', -2))
s.append(txt(W/2, 196, "De la démographie à la décision : où investir dans l'éducation en Mauritanie",
             21, '#fff', '400', 'middle', 0, .85))
s.append(txt(W/2, 326, '365 231', 128, '#fff', '800', 'middle', -6))
s.append(txt(W/2, 366, "enfants de 6 à 14 ans ne sont jamais allés à l'école formelle",
             23, '#fff', '600', 'middle', 0, .92))
# trois repères, chacun centré dans son tiers du bandeau
for i, (v, t) in enumerate([('33,1 %', "de cette classe d'âge"),
                            ('71 %', 'dans 5 wilayas seulement'),
                            ('7 sur 10', 'vivent à la campagne')]):
    x = W/6 + i*W/3
    s.append(txt(x, 404, v, 30, '#fff', '800', 'middle', -.8))
    s.append(txt(x, 414, t, 15, '#fff', '400', 'middle', 0, .72))
s.append(f'<rect y="424" width="{W*0.67}" height="6" fill="{P3}"/>')
s.append(f'<rect x="{W*0.67}" y="424" width="{W*0.17}" height="6" fill="{OR}"/>')
s.append(f'<rect x="{W*0.84}" y="424" width="{W*0.16}" height="6" fill="{RI}"/>')

# ══ 1 · LE PARADOXE ═══════════════════════════════════════════════════
y0 = 462
s.append(lab(56, y0 + 4, '1 · Le paradoxe que le classement ne voit pas'))
s.append(card(56, y0 + 22, W - 112, 250))
s.append(txt(88, y0 + 66, 'Deux wilayas, presque le même taux.', 25, ENCRE, '700'))
s.append(txt(88, y0 + 96, 'Tout les oppose.', 25, RI, '700'))
for i, (nom, taux, mah, auc, lev) in enumerate([
        ('Hodh El Gharbi', '47,2 %', '32,9 %', '14,3 %', 'Passerelles'),
        ('Guidimakha', '44,4 %', '1,9 %', '42,5 %', 'Écoles')]):
    x = 620 + i*270
    s.append(txt(x, y0 + 64, nom, 17, ENCRE, '700', 'middle'))
    s.append(txt(x, y0 + 104, taux, 34, ACC, '800', 'middle', -1))
    s.append(txt(x, y0 + 122, 'hors école formelle', 13, GRIS, '400', 'middle'))
    s.append(txt(x, y0 + 168, mah, 25, OR if i == 0 else GRIS, '800', 'middle'))
    s.append(txt(x, y0 + 188, 'mahadra / coranique', 13, GRIS, '400', 'middle'))
    s.append(txt(x, y0 + 228, auc, 25, GRIS if i == 0 else RI, '800', 'middle'))
    s.append(txt(x, y0 + 248, 'aucune instruction', 13, GRIS, '400', 'middle'))
    s.append(f'<rect x="{x-105}" y="{y0+262}" width="210" height="26" rx="13" '
             f'fill="{OR if i==0 else RI}" opacity=".14"/>')
    s.append(txt(x, y0 + 280, lev, 15, OR if i == 0 else RI, '700', 'middle'))
s.append(txt(88, y0 + 168, 'Au Hodh El Gharbi les enfants', 16, GRIS, '400'))
s.append(txt(88, y0 + 190, 'apprennent, sans diplôme reconnu.', 16, ENCRE, '600'))
s.append(txt(88, y0 + 224, 'Au Guidimakha ils ne sont', 16, GRIS, '400'))
s.append(txt(88, y0 + 246, 'nulle part.', 16, ENCRE, '600'))

# ══ 2 · CARTE + 100 ENFANTS ═══════════════════════════════════════════
y1 = y0 + 290
s.append(lab(56, y1 + 4, '2 · Les 13 wilayas classées par priorité'))
s.append(card(56, y1 + 22, 630, 400))
sc = 504 / C['w']
s.append(f'<g transform="translate(112,{y1+46}) scale({sc:.4f})">')
for k, path in C['paths'].items():
    r = d[d.wilaya == k]
    s.append(f'<path d="{path}" fill="{NIV(int(r.rang.iloc[0])) if len(r) else TRAIT}" '
             f'stroke="#fff" stroke-width="3"/>')
s.append('</g>')
for i, (nm, col) in enumerate([('Très élevée', P1), ('Élevée', P2),
                               ('Moyenne', P3), ('Faible', P4)]):
    x = 92 + i*152
    s.append(f'<rect x="{x}" y="{y1+380}" width="15" height="15" rx="3" fill="{col}"/>')
    s.append(txt(x + 22, y1 + 392, nm, 14, GRIS, '500'))

s.append(card(706, y1 + 22, W - 762, 400))
s.append(lab(738, y1 + 54, 'Sur 100 enfants de 6 à 14 ans'))
per = ("<circle cx='6' cy='3.3' r='3.05'/><path d='M6 7.5c3.3 0 6 2.7 6 6V16H0v-2.5"
       "c0-3.3 2.7-6 6-6z'/>")
for i in range(100):
    c = P3 if i < 67 else OR if i < 84 else RI
    x = 740 + (i % 10)*40
    yy = y1 + 70 + (i // 10)*25
    s.append(f'<g transform="translate({x},{yy}) scale(1.35)" fill="{c}">{per}</g>')
for i, (n, c, t) in enumerate([(67, P3, "vont à l'école"), (17, OR, 'mahadra ou coranique'),
                               (16, RI, "n'apprennent nulle part")]):
    yy = y1 + 330 + i*26
    s.append(f'<g transform="translate(742,{yy}) scale(1.3)" fill="{c}">{per}</g>')
    s.append(txt(768, yy + 17, f'<tspan font-weight="800">{n}</tspan> {t}', 15, ENCRE, '400'))

# ══ 3 · MÉTHODE ═══════════════════════════════════════════════════════
y2 = y1 + 442
s.append(lab(56, y2 + 4, '3 · Comment nous transformons des pourcentages en enfants'))
s.append(card(56, y2 + 22, W - 112, 148))
etapes = [('Base population', '4 077 347\nhabitants'), ('EPCV 2019 · ANSADE', '60 600\nindividus'),
          ('Croisement', 'taux ×\npopulation'), ('Indice de priorité', '45 · 35 · 20')]
for i, (t, v) in enumerate(etapes):
    x = 92 + i*272
    s.append(f'<rect x="{x}" y="{y2+44}" width="228" height="104" rx="11" fill="{FOND}" '
             f'stroke="{TRAIT}" stroke-width="1.5"/>')
    s.append(txt(x + 114, y2 + 68, t, 14, GRIS, '700', 'middle'))
    for j, ligne in enumerate(v.split('\n')):
        s.append(txt(x + 114, y2 + 100 + j*24, ligne, 20, ACC, '800', 'middle', -.5))
    if i < 3:
        s.append(txt(x + 250, y2 + 104, '→', 24, GRIS, '400', 'middle'))

# ══ 4 · CE QUE L'OUTIL DIT DE FAIRE ═══════════════════════════════════
y3 = y2 + 168
s.append(lab(56, y3 + 4, "4 · Pour chaque wilaya, le levier d'action"))
s.append(card(56, y3 + 22, W - 112, 168))
mec = [('Exclusion', "La majorité ne reçoit aucune instruction", 'Créer des écoles', RI,
        '6 wilayas'),
       ('Substitution', "La majorité est en mahadra ou coranique", 'Ouvrir des passerelles', OR,
        '6 wilayas'),
       ('Volume élevé', "Poids national fort, taux sous la moyenne", "Capacité d'accueil", ACC2,
        '1 wilaya')]
for i, (m, expl, lev, col, n) in enumerate(mec):
    yy = y3 + 54 + i*40
    s.append(f'<rect x="88" y="{yy-24}" width="6" height="38" rx="3" fill="{col}"/>')
    s.append(txt(108, yy, m, 19, ENCRE, '700'))
    s.append(txt(108, yy + 20, expl, 14, GRIS, '400'))
    s.append(txt(700, yy, lev, 19, col, '700'))
    s.append(txt(W - 88, yy, n, 15, GRIS, '500', 'end'))

# ══ PIED ══════════════════════════════════════════════════════════════
yf = H - 118
s.append(f'<rect y="{yf}" width="{W}" height="118" fill="{ACC}"/>')
QR = open('/home/claude/edufocus/qr_inner.txt').read()
s.append(f'<rect x="52" y="{yf+16}" width="86" height="86" rx="10" fill="#fff"/>')
s.append(f'<g transform="translate(57,{yf+21}) scale({76/33:.4f})">{QR}</g>')
s.append(txt(158, yf + 46, 'edufocuspro.netlify.app', 22, '#fff', '700'))
s.append(txt(158, yf + 72, 'github.com/tidjanecheikh5-lab/Edufocus', 15, '#fff', '400', 'start', 0, .72))
s.append(txt(158, yf + 94, 'Scannez pour ouvrir le prototype', 13, '#fff', '400', 'start', 0, .55))
s.append(txt(W - 56, yf + 44, 'Équipe DataSphere', 20, '#fff', '700', 'end', 0, .95))
s.append(txt(W - 56, yf + 70, '13 wilayas · 3 langues · 103 tests automatisés',
             15, '#fff', '500', 'end', 0, .78))
s.append(txt(W - 56, yf + 94, 'Sources : base population 2013-2019 (hackathon) · EPCV 2019 (ANSADE)',
             12.5, '#fff', '400', 'end', 0, .55))
s.append('</svg>')

svg = ''.join(s)
open('/home/claude/edufocus/infographie.svg', 'w').write(svg)
cairosvg.svg2png(url='/home/claude/edufocus/infographie.svg',
                 write_to='/mnt/user-data/outputs/edufocus/EduFocus_Infographie.png',
                 output_width=2480, output_height=3508)          # A3 à 210 dpi
cairosvg.svg2pdf(url='/home/claude/edufocus/infographie.svg',
                 write_to='/mnt/user-data/outputs/edufocus/EduFocus_Infographie.pdf')
print('infographie generee')
