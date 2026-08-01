import re, sys
from PIL import ImageFont
FR = {'400':'Poppins-Regular.ttf','500':'Poppins-Medium.ttf','600':'Poppins-SemiBold.ttf',
      '700':'Poppins-Bold.ttf','800':'Poppins-ExtraBold.ttf'}
import glob, os
BASE = os.path.dirname(glob.glob('/usr/share/fonts/**/Poppins-Regular.ttf', recursive=True)[0])
def police(w, size):
    f = FR.get(str(w), 'Poppins-Regular.ttf')
    p = os.path.join(BASE, f)
    if not os.path.exists(p): p = os.path.join(BASE, 'Poppins-Regular.ttf')
    return ImageFont.truetype(p, int(size))

def boites(svg):
    out = []
    for m in re.finditer(
        r'<text x="([\d.]+)" y="([\d.]+)" font-size="([\d.]+)" fill="[^"]*" '
        r'font-weight="(\d+)" text-anchor="(\w+)" letter-spacing="([-\d.]+)" opacity="[\d.]+">([^<]*)</text>', svg):
        x, y, fs, w, anc, ls, t = m.groups()
        x, y, fs, ls = float(x), float(y), float(fs), float(ls)
        clean = re.sub('<[^>]+>', '', t)
        if not clean.strip(): continue
        lg = police(w, fs).getlength(clean) + ls * max(0, len(clean) - 1)
        x0 = x if anc == 'start' else x - lg/2 if anc == 'middle' else x - lg
        out.append({'t': clean[:44], 'x0': x0, 'x1': x0+lg, 'y0': y-fs*0.78, 'y1': y+fs*0.24, 'fs': fs})
    return out

def check(fichier, W, nom):
    svg = open(fichier).read()
    b = boites(svg)
    hors = [z for z in b if z['x0'] < 12 or z['x1'] > W-12]
    col = []
    for i, a in enumerate(b):
        for c in b[i+1:]:
            if a['x0'] < c['x1']-1 and c['x0'] < a['x1']-1 and a['y0'] < c['y1']-1 and c['y0'] < a['y1']-1:
                col.append((a['t'], c['t']))
    print(f'\n=== {nom} · {len(b)} textes')
    print(f'  hors cadre : {len(hors)}')
    for z in hors[:8]: print(f"     [{z['x0']:.0f} -> {z['x1']:.0f}]  {z['t']}")
    print(f'  chevauchements : {len(col)}')
    for a, c in col[:10]: print(f"     « {a} »  X  « {c} »")
    return hors, col

check('infographie.svg', 1200, 'INFOGRAPHIE')
check('uiux.svg', 1200, 'UI/UX')
