# -*- coding: utf-8 -*-
"""Planche UI/UX EduFocus — A3 vertical. Captures grandes et lisibles."""
import base64, pathlib
from PIL import Image

W, H = 1200, 1697
ACC, ACC2, ACC0 = '#B85C1E', '#D97428', '#8C4315'
OR, RI, OK = '#E5A82E', '#C0392B', '#3FA79B'
FOND, TRAIT, ENCRE, GRIS, PAPIER = '#FBF6EE', '#EBE0CE', '#1E170F', '#7A6E5E', '#FFFFFF'
s = []

def txt(x, y, t, size=15, fill=ENCRE, w='400', anchor='start', ls=0, op=1):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{w}" '
            f'text-anchor="{anchor}" letter-spacing="{ls}" opacity="{op}">{t}</text>')
def lab(x, y, t): return txt(x, y, t.upper(), 14, GRIS, '700', ls=2.4)
def card(x, y, w, h, f=PAPIER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="13" fill="{f}" stroke="{TRAIT}" stroke-width="1.5"/>'

N = [0]
def shot(chemin, x, y, larg, haut, titre='', sous=''):
    """Insère une capture à l'échelle : on l'ajuste en largeur, on rogne le bas."""
    im = Image.open(chemin).convert('RGB')
    iw, ih = im.size
    cible_w, cible_h = larg*2, haut*2
    r = cible_w / iw
    im = im.resize((cible_w, int(ih*r)), Image.LANCZOS)
    if im.size[1] > cible_h: im = im.crop((0, 0, cible_w, cible_h))
    tmp = f'/tmp/_s{N[0]}.jpg'; N[0] += 1
    im.save(tmp, 'JPEG', quality=90)
    d = 'data:image/jpeg;base64,' + base64.b64encode(open(tmp, 'rb').read()).decode()
    hh = min(haut, im.size[1]/2)
    out = [f'<clipPath id="k{N[0]}"><rect x="{x}" y="{y}" width="{larg}" height="{hh}" rx="9"/></clipPath>',
           f'<image xlink:href="{d}" x="{x}" y="{y}" width="{larg}" height="{im.size[1]/2}" clip-path="url(#k{N[0]})"/>',
           f'<rect x="{x}" y="{y}" width="{larg}" height="{hh}" rx="9" fill="none" stroke="{TRAIT}" stroke-width="1.5"/>']
    if titre: out.append(txt(x, y + hh + 22, titre, 16, ENCRE, '700'))
    if sous:  out.append(txt(x, y + hh + 41, sous, 12.5, GRIS, '400'))
    return ''.join(out), hh

s.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
         f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Poppins, sans-serif">')
s.append(f'<rect width="{W}" height="{H}" fill="{FOND}"/>')

# ══ BANDEAU ═══════════════════════════════════════════════════════════
s.append(f'''<defs><radialGradient id="g" cx="50%" cy="0%" r="130%">
<stop offset="0" stop-color="{ACC2}"/><stop offset="55%" stop-color="{ACC}"/>
<stop offset="100%" stop-color="{ACC0}"/></radialGradient></defs>''')
s.append(f'<rect width="{W}" height="196" fill="url(#g)"/>')
s.append('<g transform="translate(80,38) scale(0.72)">'
 '<circle cx="32" cy="17" r="11" fill="#fff"/>'
 '<path d="M32 32c11.6 0 21 9.4 21 21v9H11v-9c0-11.6 9.4-21 21-21z" fill="#fff"/>'
 '<circle cx="32" cy="17" r="5.4" fill="#E5A82E"/>'
 '<path d="M23 46h18M23 53h12" stroke="#B85C1E" stroke-width="3.4" stroke-linecap="round"/></g>')
s.append(txt(130, 72, 'EduFocus', 38, '#fff', '800', 'start', -1.2))
s.append(txt(130, 97, 'Interface et parcours utilisateur', 15, '#fff', '400', 'start', 0, .8))
s.append(txt(W-80, 62, 'ÉQUIPE DATASPHERE', 13, '#fff', '700', 'end', 2.4, .68))
s.append(txt(W-80, 88, 'IndabaX Mauritanie 2026', 15, '#fff', '400', 'end', 0, .8))
s.append(txt(80, 148, 'Comprendre en 5 secondes, décider en 3 clics', 24, '#fff', '700', 'start', -.5))
s.append(txt(80, 174, 'Trois langues · silhouettes plutôt que pourcentages · une explication écrite pour chaque wilaya',
            14, '#fff', '400', 'start', 0, .8))
s.append(f'<rect y="190" width="{W*0.67}" height="6" fill="{OK}"/>')
s.append(f'<rect x="{W*0.67}" y="190" width="{W*0.17}" height="6" fill="{OR}"/>')
s.append(f'<rect x="{W*0.84}" y="190" width="{W*0.16}" height="6" fill="{RI}"/>')

# ══ 1 · ÉCRAN D'ACCUEIL, EN GRAND ═════════════════════════════════════
y = 238
s.append(lab(80, y, '1 · L’accueil — la carte reste à gauche, les données défilent à droite'))
a, ha = shot('crops/accueil_carte.png', 80, y+18, 386, 408)
s.append(a)
b, hb = shot('crops/accueil_droite.png', 486, y+18, 634, 408)
s.append(b)
s.append(txt(80, y+18+408+24, 'Carte des priorités, toujours visible', 15, ENCRE, '700'))
s.append(txt(486, y+18+408+24, 'Repères, 100 personnes, anneaux, histogrammes', 15, ENCRE, '700'))

# ══ 2 · FICHE ET SIMULATEUR ═══════════════════════════════════════════
y = 730
s.append(lab(80, y, '2 · La fiche wilaya et le simulateur'))
c, hc = shot('crops/fiche.png', 80, y+18, 512, 340)
s.append(c)
d, hd = shot('crops/simu.png', 608, y+18, 512, 340)
s.append(d)
s.append(txt(80, y+382, '« Pourquoi cette wilaya ? » et les actions chiffrées', 15, ENCRE, '700'))
s.append(txt(80, y+402, 'Un texte écrit à partir de ses propres chiffres', 12.5, GRIS, '400'))
s.append(txt(608, y+382, 'Trois règles de répartition, moyens à mobiliser', 15, ENCRE, '700'))
s.append(txt(608, y+402, 'Salles, écoles et enseignants, hypothèses modifiables', 12.5, GRIS, '400'))

# ══ 3 · MOBILE ET PRINCIPES ═══════════════════════════════════════════
y = 1160
s.append(lab(80, y, '3 · Mobile et trois langues'))
for i, (f, t) in enumerate([('caps/mob_accueil.png', 'Accueil'),
                            ('caps/mob_carte.png', 'Carte'),
                            ('caps/mob_arabe.png', 'العربية · RTL')]):
    e, he = shot(f, 80 + i*176, y+18, 158, 262)
    s.append(e)
    s.append(txt(80 + i*176 + 79, y+300, t, 13, GRIS, '600', 'middle'))

s.append(card(620, y+18, 500, 262))
s.append(lab(648, y+48, 'Quatre principes d’interface'))
princ = [('Des silhouettes, pas des pourcentages', 'Cent personnes colorées : on compte les rouges.'),
         ('Une couleur, un seul sens', 'Le rouge ne dit qu’une chose : aucune instruction.'),
         ('Une gradation, pas un feu tricolore', 'La priorité est ordonnée : une teinte, quatre intensités.'),
         ('Trois langues, dont l’arabe RTL', 'Toute la mise en page se retourne, carte comprise.')]
for i, (t, dd) in enumerate(princ):
    yy = y + 82 + i*50
    s.append(f'<rect x="648" y="{yy-13}" width="4" height="36" rx="2" fill="{ACC}"/>')
    s.append(txt(666, yy, t, 14, ENCRE, '700'))
    s.append(txt(666, yy+18, dd, 11.5, GRIS, '400'))

# ══ 4 · LA DÉMONSTRATION ══════════════════════════════════════════════
y = 1492
s.append(card(80, y, W-160, 76, PAPIER))
s.append(txt(104, y+30, 'Hodh El Gharbi 47,2 %   ·   Guidimakha 44,4 %', 17, ENCRE, '700'))
s.append(txt(104, y+54, 'Presque le même taux. 33 % en mahadra dans l’une, 42,5 % sans aucune instruction dans l’autre.',
            13, GRIS, '400'))
s.append(txt(W-104, y+44, 'Passerelles / Écoles', 18, ACC, '700', 'end'))

# ══ PIED ══════════════════════════════════════════════════════════════
yf = H - 118
s.append(f'<rect y="{yf}" width="{W}" height="118" fill="{ACC}"/>')
def qr(fichier, x, yy, taille, legende):
    vb, inner = open(fichier).read().split('|', 1)
    s.append(f'<rect x="{x}" y="{yy}" width="{taille+10}" height="{taille+10}" rx="9" fill="#fff"/>')
    s.append(f'<g transform="translate({x+5},{yy+5}) scale({taille/int(vb):.4f})">{inner}</g>')
    s.append(txt(x+(taille+10)/2, yy+taille+26, legende, 12, '#fff', '600', 'middle', 0, .82))
qr('/home/claude/edufocus/qr_site_inner.txt', 52, yf+14, 68, 'Prototype')
qr('/home/claude/edufocus/qr_code_inner.txt', 148, yf+14, 68, 'Code source')
s.append(txt(256, yf+44, 'edufocuspro.netlify.app', 21, '#fff', '700'))
s.append(txt(256, yf+68, 'github.com/tidjanecheikh5-lab/Edufocus', 15, '#fff', '400', 'start', 0, .72))
s.append(txt(256, yf+92, 'Scannez pour ouvrir', 13, '#fff', '400', 'start', 0, .55))
s.append(txt(W-56, yf+44, 'Équipe DataSphere', 20, '#fff', '700', 'end', 0, .95))
s.append(txt(W-56, yf+70, '7 écrans · 3 langues · 103 tests automatisés', 15, '#fff', '500', 'end', 0, .78))
s.append(txt(W-56, yf+94, 'Captures réelles de l’application', 12.5, '#fff', '400', 'end', 0, .55))
s.append('</svg>')

svg = ''.join(s)
pathlib.Path('/home/claude/edufocus/uiux.svg').write_text(svg)
import cairosvg
cairosvg.svg2png(url='/home/claude/edufocus/uiux.svg',
                 write_to='/mnt/user-data/outputs/edufocus/EduFocus_UIUX.png',
                 output_width=2480, output_height=3508)
cairosvg.svg2pdf(url='/home/claude/edufocus/uiux.svg',
                 write_to='/mnt/user-data/outputs/edufocus/EduFocus_UIUX.pdf')
print('planche UI/UX refaite')
