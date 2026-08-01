# -*- coding: utf-8 -*-
"""Assemble index.html : gabarit + wilayas.csv + carte SVG."""
import json, pathlib, shutil

BASE = pathlib.Path('/home/claude/edufocus')
OUT = pathlib.Path('/mnt/user-data/outputs/edufocus')
OUT.mkdir(parents=True, exist_ok=True)

csv = (BASE / 'wilayas.csv').read_text(encoding='utf-8-sig')
# protège le littéral de gabarit JS
csv_js = csv.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
carte = json.dumps(json.load(open(BASE / 'carte.json')), ensure_ascii=False,
                   separators=(',', ':'))

html = (BASE / 'template.html').read_text(encoding='utf-8')
html = html.replace('__CSV__', csv_js).replace('__MAP__', carte)
(OUT / 'index.html').write_text(html, encoding='utf-8')

shutil.copy(BASE / 'wilayas.csv', OUT / 'wilayas.csv')
print(f"index.html   {len(html.encode()):>8,} octets")
print(f"wilayas.csv  {len(csv.encode()):>8,} octets")
