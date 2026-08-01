# -*- coding: utf-8 -*-
"""Un point = 100 enfants hors école. Les points sont tirés au hasard À L'INTÉRIEUR
du polygone de leur wilaya : la densité visible est donc la densité réelle."""
import json, math, random
import pandas as pd
from shapely.geometry import shape, Point

random.seed(7)
NE2FR = {'Hodh ech Chargui':'Hodh El Charghi','Hodh el Gharbi':'Hodh El Gharbi',
  'Assaba':'Assaba','Gorgol':'Gorgol','Brakna':'Brakna','Trarza':'Trarza','Adrar':'Adrar',
  'Dakhlet Nouadhibou':'Dakhlet Nouadhibou','Tagant':'Tagant','Guidimaka':'Guidimakha',
  'Tiris Zemmour':'Tiris Zemmour','Inchiri':'Inchiri','Nouakchott':'Nouakchott'}

ne = json.load(open('/home/claude/edufocus/ne10.geojson'))
geo = {NE2FR[f['properties']['name']]: shape(f['geometry']).buffer(0)
       for f in ne['features'] if f['properties'].get('iso_a2') == 'MR'}
carte = json.load(open('/home/claude/edufocus/carte.json'))
W, H = carte['w'], carte['h']

# même projection que carte.py
xs, ys = [], []
for g in geo.values():
    for p in (g.geoms if g.geom_type == 'MultiPolygon' else [g]):
        xs += [c[0] for c in p.exterior.coords]; ys += [c[1] for c in p.exterior.coords]
lon0, lon1, lat0, lat1 = min(xs), max(xs), min(ys), max(ys)
my = lambda la: math.degrees(math.log(math.tan(math.pi/4 + math.radians(la)/2)))
PAD = 10
s = min((W-2*PAD)/(lon1-lon0), (H-2*PAD)/(my(lat1)-my(lat0)))
ox = PAD + ((W-2*PAD) - s*(lon1-lon0))/2
oy = PAD + ((H-2*PAD) - s*(my(lat1)-my(lat0)))/2
proj = lambda lo, la: (ox + (lo-lon0)*s, oy + (my(lat1)-my(la))*s)

d = pd.read_csv('/home/claude/edufocus/wilayas.csv')
RUR = json.load(open('/home/claude/edufocus/rural_hors.json'))   # part rurale des enfants hors école
PAR_POINT = 100
pts = []
for r in d.itertuples():
    g = geo[r.wilaya]
    n = round(r.enfants_hors_ecole / PAR_POINT)
    x0, y0, x1, y1 = g.bounds
    # Effectifs exacts, pas de tirage : les proportions affichées sont justes.
    n_mah = round(n * r.pct_mahadra / r.taux_hors_ecole)
    n_rur = round(n * RUR.get(r.wilaya, r.part_rurale) / 100)
    coords, garde = [], 0
    while len(coords) < n and garde < n * 400:
        garde += 1
        lo = random.uniform(x0, x1); la = random.uniform(y0, y1)
        if g.contains(Point(lo, la)):
            coords.append(proj(lo, la))
    for i, (X, Y) in enumerate(coords):
        pts.append([round(X, 1), round(Y, 1),
                    1 if i < n_mah else 2,        # 1 mahadra/coranique · 2 aucune instruction
                    r.rang,
                    1 if i % n < n_rur else 0])   # 1 campagne · 0 ville
    got = len(coords)
    print(f"{r.wilaya:20} {got:5} points  ({r.enfants_hors_ecole:6,} enfants)")

random.shuffle(pts)
json.dump({'w': W, 'h': H, 'parPoint': PAR_POINT, 'pts': pts,
           'centres': carte['centres'], 'paths': carte['paths']},
          open('/home/claude/edufocus/points.json', 'w'), separators=(',', ':'))

n_mah = sum(1 for p in pts if p[2] == 1)
n_rur = sum(1 for p in pts if p[4] == 1)
print(f"\nTOTAL {len(pts)} points = {len(pts)*PAR_POINT:,} enfants")
print(f"  mahadra/coranique : {n_mah}  ({n_mah/len(pts)*100:.1f} %)")
print(f"  aucune instruction: {len(pts)-n_mah}  ({(len(pts)-n_mah)/len(pts)*100:.1f} %)")
print(f"  campagne          : {n_rur}  ({n_rur/len(pts)*100:.1f} %)")
print(f"Poids fichier : {len(json.dumps(pts))/1024:.0f} Ko")
