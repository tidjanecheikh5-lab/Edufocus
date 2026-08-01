# -*- coding: utf-8 -*-
"""Extrait les 13 wilayas de Mauritanie -> chemins SVG compacts, sans dépendance externe."""
import json
from shapely.geometry import shape, mapping
from shapely.ops import transform

# nom Natural Earth -> nom EduFocus
NE2FR = {
    'Hodh ech Chargui': 'Hodh El Charghi', 'Hodh el Gharbi': 'Hodh El Gharbi',
    'Assaba': 'Assaba', 'Gorgol': 'Gorgol', 'Brakna': 'Brakna', 'Trarza': 'Trarza',
    'Adrar': 'Adrar', 'Dakhlet Nouadhibou': 'Dakhlet Nouadhibou', 'Tagant': 'Tagant',
    'Guidimaka': 'Guidimakha', 'Tiris Zemmour': 'Tiris Zemmour', 'Inchiri': 'Inchiri',
    'Nouakchott': 'Nouakchott'}

d = json.load(open('ne10.geojson'))
feats = [x for x in d['features'] if x['properties'].get('iso_a2') == 'MR']

geoms = {}
for f in feats:
    g = shape(f['geometry']).buffer(0)
    g = g.simplify(0.012, preserve_topology=True)          # ~2 km : largement suffisant
    geoms[NE2FR[f['properties']['name']]] = g

# --- projection : Mercator simple, cadrée sur le pays -------------------------
xs = [c[0] for g in geoms.values() for p in (g.geoms if g.geom_type == 'MultiPolygon' else [g])
      for c in p.exterior.coords]
ys = [c[1] for g in geoms.values() for p in (g.geoms if g.geom_type == 'MultiPolygon' else [g])
      for c in p.exterior.coords]
lon0, lon1, lat0, lat1 = min(xs), max(xs), min(ys), max(ys)
W, H, PAD = 1000, 780, 10
import math
def my(lat): return math.degrees(math.log(math.tan(math.pi/4 + math.radians(lat)/2)))
my0, my1 = my(lat0), my(lat1)
sx = (W - 2*PAD) / (lon1 - lon0)
sy = (H - 2*PAD) / (my1 - my0)
s = min(sx, sy)
ox = PAD + ((W - 2*PAD) - s*(lon1-lon0))/2
oy = PAD + ((H - 2*PAD) - s*(my1-my0))/2

def proj(lon, lat):
    return (ox + (lon-lon0)*s, oy + (my1-my(lat))*s)

def path_of(g):
    polys = g.geoms if g.geom_type == 'MultiPolygon' else [g]
    out = []
    for p in polys:
        if p.area < 0.005:            # supprime les micro-îlots invisibles
            continue
        for ring in [p.exterior] + list(p.interiors):
            pts = [proj(*c) for c in ring.coords]
            out.append('M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z')
    return ''.join(out)

paths, centres = {}, {}
for k, g in geoms.items():
    paths[k] = path_of(g)
    c = g.representative_point()
    centres[k] = [round(v, 1) for v in proj(c.x, c.y)]

json.dump({'w': W, 'h': H, 'paths': paths, 'centres': centres},
          open('carte.json', 'w'), ensure_ascii=False, separators=(',', ':'))

tot = sum(len(v) for v in paths.values())
print(f'13 wilayas -> {tot:,} caracteres de chemins SVG ({tot/1024:.0f} Ko)')
for k, v in sorted(paths.items(), key=lambda x: -len(x[1])):
    print(f'  {k:20} {len(v):6,}  centre {centres[k]}')
