import math, json, itertools
from playwright.sync_api import sync_playwright

URL = 'file:///mnt/user-data/outputs/edufocus/index.html'
ok, ko = [], []
def check(cond, label, detail=''):
    (ok if cond else ko).append(f"{label}{(' — ' + str(detail)) if detail else ''}")

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(1200)

    # ── 1. CARTE : géométrie des pastilles ────────────────────────────────
    pg.click('[data-go="map"]'); pg.wait_for_timeout(500)
    check(pg.locator('#mapbox path').count() == 13, '13 wilayas dessinées',
          pg.locator('#mapbox path').count())
    check(pg.locator('.lbl').count() == 13, '13 étiquettes de wilaya',
          pg.locator('.lbl').count())
    check(pg.locator('.chip').count() == 13, '13 noms cliquables',
          pg.locator('.chip').count())

    import itertools
    boxes = pg.eval_on_selector_all('.lbl', """els=>els.map(e=>{
        const r=e.getBoundingClientRect();
        return {n:e.dataset.w, r:e.querySelector('u').textContent.trim(),
                x:r.x, y:r.y, w:r.width, h:r.height};})""")
    chev = [(a['n'], c['n']) for a, c in itertools.combinations(boxes, 2)
            if a['x'] < c['x']+c['w'] and c['x'] < a['x']+a['w']
            and a['y'] < c['y']+c['h'] and c['y'] < a['y']+a['h']]
    check(not chev, 'aucune étiquette ne se chevauche (mobile)', chev[:3])
    check(sorted(int(x['r']) for x in boxes) == list(range(1, 14)),
          'rangs 1 à 13 présents une seule fois')

    svg = pg.eval_on_selector('#mapbox svg', "e=>{const r=e.getBoundingClientRect();"
                              "return{x:r.x,y:r.y,w:r.width,h:r.height}}")
    dehors = [x['n'] for x in boxes if x['x'] < svg['x']-3
              or x['x']+x['w'] > svg['x']+svg['w']+3]
    check(not dehors, 'toutes les étiquettes tiennent dans le cadre', dehors)

    # couleurs = niveaux de priorité
    fills = pg.eval_on_selector_all('#mapbox path',
        "els=>els.map(e=>[e.dataset.w, e.getAttribute('fill')])")
    check(len({f[1] for f in fills}) == 4, '4 couleurs de priorité utilisées',
          sorted({f[1] for f in fills}))

    # ── 2. ACCUEIL : compteur et tenue dans l'écran ───────────────────────
    pg.click('.tabs button[data-go="home"]'); pg.wait_for_timeout(1800)
    c = pg.inner_text('#counter')
    check(c.replace('\u202f', '').replace(' ', '') == '365231', 'compteur = 365 231', c)
    check(pg.locator('.tile').count() >= 7, 'tableau de bord : 7 tuiles ou plus',
          pg.locator('.tile').count())
    # pictogrammes de personnes
    mk = pg.eval_on_selector('#natWaffle i',
        "e=>getComputedStyle(e).webkitMaskImage || getComputedStyle(e).maskImage")
    check('svg' in (mk or ''), 'la grille utilise des silhouettes de personnes',
          (mk or 'aucun')[:44])
    bg = pg.eval_on_selector_all('#natWaffle i.f, #natWaffle i.m, #natWaffle i.n',
        "els=>[...new Set(els.map(e=>getComputedStyle(e).backgroundColor))]")
    check(len(bg) == 3, '3 couleurs de personnes distinctes', bg)
    # histogramme des 13 wilayas
    check(pg.locator('#cmpSegs button').count() == 3, '3 indicateurs comparables')
    check(pg.locator('#cmpBars .bar').count() == 13, 'histogramme : 13 wilayas')
    ordres = {}
    for k in ['taux_hors_ecole', 'taux_pauvrete', 'part_rurale']:
        pg.eval_on_selector(f'#cmpSegs button[data-k="{k}"]', 'e=>e.click()')
        pg.wait_for_timeout(400)
        v = pg.eval_on_selector_all('#cmpBars .bar-t i',
            "els=>els.map(e=>parseFloat(e.dataset.pc))")
        n = pg.eval_on_selector_all('#cmpBars .bar-n', "els=>els.map(e=>e.textContent.trim())")
        check(all(v[i] >= v[i+1] for i in range(len(v)-1)) and abs(v[0]-100) < 0.1,
              f'{k} : barres triées et normalisées', f'{v[0]}…{v[-1]}')
        ordres[k] = n[0]
    check(len(set(ordres.values())) >= 2,
          'changer d\'indicateur change le classement', ordres)
    check(pg.locator('.kpis div').count() == 3, '3 repères chiffrés en haut')
    kv = pg.eval_on_selector_all('.kpis b', "els=>els.map(e=>e.textContent.trim())")
    check(all(any(c.isdigit() for c in x) for x in kv), 'les 3 repères sont renseignés', kv)
    # les camemberts
    for did, lbl in [('dSex', 'sexe'), ('dMil', 'milieu')]:
        seg = pg.eval_on_selector_all(f'#{did} svg circle[stroke-dasharray]',
            "els=>els.map(e=>parseFloat(e.getAttribute('stroke-dasharray')))")
        check(len(seg) == 2 and abs(sum(seg) - 100) < 0.5,
              f'camembert {lbl} : 2 parts totalisant 100', [round(x,1) for x in seg])
    # aucune tuile ne doit rester à moitié vide
    creux = pg.eval_on_selector_all('.tile', """els=>els.filter(e=>{
        const h=e.getBoundingClientRect().height;
        let c=0; for(const k of e.children) c+=k.getBoundingClientRect().height;
        return h - c > 90;}).length""")
    check(creux == 0, 'aucune tuile avec un grand vide', creux)
    # l'en-tete ne doit pas se replier
    hb = pg.eval_on_selector('.brand', "e=>e.getBoundingClientRect().height")
    check(hb < 40, "le titre tient sur une ligne (mobile)", f'{hb:.0f}px')
    check(pg.locator('#natBars .bar').count() == 5, '5 barres de wilayas sur l\'accueil')
    pg.wait_for_timeout(900)
    larg = pg.eval_on_selector_all('#natBars .bar-t i',
        "els=>els.map(e=>parseFloat(e.style.width)||0)")
    check(larg and larg[0] > 95 and all(larg[i] >= larg[i+1] for i in range(len(larg)-1)),
          'barres animées et décroissantes', [round(x) for x in larg])
    sp = pg.eval_on_selector_all('#natSplit div', "els=>els.map(e=>e.textContent.trim())")
    check(len(sp) == 2 and all(sp), 'la barre mahadra / aucune instruction est remplie', sp)

    # ── 3. Aucun débordement horizontal sur aucun écran ───────────────────
    for tab, lbl in [('home', 'Accueil'), ('map', 'Carte'), ('rank', 'Classement'),
                     ('sim', 'Simulateur'), ('meth', 'Méthode')]:
        pg.click(f'.tabs button[data-go="{tab}"]'); pg.wait_for_timeout(350)
        ov = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(ov <= 0, f'pas de débordement horizontal — {lbl}', f'{ov}px')

    # ── 4. CLASSEMENT : tri et export ─────────────────────────────────────
    pg.click('.tabs button[data-go="rank"]'); pg.wait_for_timeout(400)
    check(pg.locator('#rankTable tbody tr').count() == 13, '13 lignes au classement')
    first = pg.inner_text('#rankTable tbody tr:first-child td:nth-child(2)')
    check('Guidimakha' in first, 'rang 1 = Guidimakha', first.strip())
    pg.click('#rankTable thead th[data-k="enfants_hors_ecole"]'); pg.wait_for_timeout(300)
    top = pg.inner_text('#rankTable tbody tr:first-child td:nth-child(2)')
    check('Nouakchott' in top, 'tri par nombre d\'enfants → Nouakchott en tête', top.strip())

    # ── 5. FICHE : grille de 100 et cohérence ─────────────────────────────
    pg.click('.tabs button[data-go="rank"]'); pg.wait_for_timeout(300)
    pg.click('#rankTable thead th[data-k="rang"]'); pg.wait_for_timeout(300)
    pg.click('#rankTable tbody tr:first-child'); pg.wait_for_timeout(600)
    w = pg.eval_on_selector_all('#sheet .waffle i', "els=>({n:els.length,"
        "f:els.filter(e=>e.classList.contains('f')).length,"
        "m:els.filter(e=>e.classList.contains('m')).length,"
        "x:els.filter(e=>e.classList.contains('n')).length})")
    check(w['n'] == 100, 'la grille contient exactement 100 carrés', w['n'])
    check(w['f'] + w['m'] + w['x'] == 100, 'les 3 catégories totalisent 100',
          f"école {w['f']} · mahadra {w['m']} · aucune {w['x']}")
    check(w['x'] == 42 and w['m'] == 2, 'Guidimakha : 42 sans instruction, 2 en mahadra',
          f"{w['x']} / {w['m']}")
    check('Guidimakha' in pg.inner_text('#sheet .why'), 'explication présente sur la fiche')
    acts = pg.eval_on_selector_all('#sheet .actlist li b', "els=>els.map(e=>e.textContent)")
    check(len(acts) >= 3, 'au moins 3 actions recommandées sur la fiche', acts)
    det = pg.eval_on_selector_all('#sheet .actlist li span', "els=>els.map(e=>e.textContent)")
    check(all(any(c.isdigit() for c in x) for x in det),
          'chaque action porte un chiffre', len(det))
    check('39' in pg.inner_text('#sheet .acts'),
          'Guidimakha : action chiffrée sur les 39 660 sans instruction')

    # ── 6. SIMULATEUR : les trois règles ──────────────────────────────────
    pg.click('.tabs button[data-go="sim"]'); pg.wait_for_timeout(500)
    check(pg.locator('#simSegs button').count() == 3, '3 règles de répartition proposées')

    def simule(cap, regle):
        pg.eval_on_selector('#simRange',
            f"e=>{{e.value={cap};e.dispatchEvent(new Event('input'))}}")
        pg.wait_for_timeout(120)
        pg.click(f'#simSegs button[data-r="{regle}"]'); pg.wait_for_timeout(250)
        return pg.evaluate("""()=>{
            const rng=document.getElementById('simRange');
            const bes=DATA.reduce((s,w)=>s+w.enfants_hors_ecole,0);
            const a=alloue(Math.min(+rng.value,bes), REGLE);
            const place=Object.values(a).reduce((s,v)=>s+v,0);
            const dep=DATA.filter(w=>a[w.wilaya] > w.enfants_hors_ecole+1).map(w=>w.wilaya);
            const enf=DATA.reduce((s,w)=>s+w.enfants_6_14,0);
            return {place, dep, nat:(bes-place)/enf*100,
                    reglees:DATA.filter(w=>w.enfants_hors_ecole-a[w.wilaya]<1).length,
                    lignes:document.querySelectorAll('#simTable tbody tr[data-w]').length};}""")

    nat = {}
    for reg in ['prorata', 'priorite', 'egal']:
        r = simule(100000, reg)
        check(abs(r['place'] - 100000) < 1, f'{reg} : toute la capacité est utilisée',
              f"{r['place']:.0f}")
        check(not r['dep'], f'{reg} : aucune wilaya ne dépasse son besoin', r['dep'])
        nat[reg] = round(r['nat'], 3)
    check(len(set(nat.values())) == 1,
          'le taux national est identique pour les 3 règles (arithmétique)', nat)

    rp = simule(100000, 'prorata'); rq = simule(100000, 'priorite')
    check(rq['reglees'] > rp['reglees'],
          'concentrer règle plus de wilayas qu\'étaler',
          f"priorité {rq['reglees']} · prorata {rp['reglees']}")
    check(rp['lignes'] > rq['lignes'],
          'étaler touche plus de wilayas que concentrer',
          f"prorata {rp['lignes']} · priorité {rq['lignes']}")

    plein = simule(400000, 'prorata')
    check(plein['reglees'] == 13, 'curseur au maximum → les 13 wilayas réglées',
          plein['reglees'])
    mini = simule(10000, 'priorite')
    check(abs(mini['place'] - 10000) < 1, 'capacité minimale : rien ne se perd',
          f"{mini['place']:.0f}")
    check('→' in pg.inner_text('#simTable tbody'), 'le tableau montre avant → après')

    # l'ordre du tableau doit suivre la règle choisie
    simule(100000, 'priorite')
    rgs = pg.eval_on_selector_all('#simTable tbody tr[data-w] td.rk',
        "els=>els.map(e=>+e.textContent.trim())")
    check(rgs == sorted(rgs), 'mode priorité : tableau trié par rang', rgs)
    simule(100000, 'prorata')
    pl = pg.eval_on_selector_all('#simTable tbody tr[data-w]',
        "els=>els.map(e=>+e.children[2].textContent.replace(/[^0-9]/g,''))")
    check(all(pl[i] >= pl[i+1] for i in range(len(pl)-1)),
          'mode prorata : tableau trié par places', pl[:4])

    # moyens à mobiliser
    simule(100000, 'prorata')
    check(pg.locator('#simMoyens div').count() == 3, '3 blocs de moyens')
    def moy():
        return pg.evaluate("""()=>{
            const cap=Math.min(+document.getElementById('simRange').value,
                DATA.reduce((s,w)=>s+w.enfants_hors_ecole,0));
            const a=alloue(cap, REGLE); let sa=0, ec=0, pa=0, pl=0;
            for(const w of DATA){ const p=a[w.wilaya]||0; if(p<1) continue;
              const m=moyens(w,p); sa+=m.salles; ec+=m.ecoles; pl+=p;
              if(m.type==='passerelles') pa+=p; }
            return {sa, ec, pa, pl,
              parSalle:+document.getElementById('hypSalle').value};}""")
    m = moy()
    check(m['sa'] >= m['pl']/m['parSalle'],
          'assez de salles pour tous les enfants placés',
          f"{m['sa']} salles pour {m['pl']:.0f} enfants à {m['parSalle']}/salle")
    # doubler les élèves par salle doit environ diviser les salles par deux
    pg.eval_on_selector('#hypSalle', "e=>{e.value=80;e.dispatchEvent(new Event('input'))}")
    pg.wait_for_timeout(300)
    m2 = moy()
    check(abs(m2['sa'] - m['sa']/2) / max(m['sa'], 1) < 0.05,
          'doubler les élèves par salle divise les salles par deux',
          f"{m['sa']} → {m2['sa']}")
    pg.eval_on_selector('#hypSalle', "e=>{e.value=40;e.dispatchEvent(new Event('input'))}")
    pg.wait_for_timeout(300)
    # seules les wilayas en Exclusion demandent des écoles neuves
    ec = pg.evaluate("""()=>{
        const cap=Math.min(+document.getElementById('simRange').value,
            DATA.reduce((s,w)=>s+w.enfants_hors_ecole,0));
        const a=alloue(cap, REGLE);
        return DATA.filter(w=>(a[w.wilaya]||0)>=1 && moyens(w,a[w.wilaya]).ecoles>0)
                   .map(w=>w.mecanisme);}""")
    check(ec and all(x == 'Exclusion' for x in ec),
          "écoles neuves réservées aux wilayas en Exclusion", sorted(set(ec)))
    txt = pg.inner_text('#simMoyens')
    check(any(c.isdigit() for c in txt) and 'salle' in txt.lower(),
          'les moyens sont chiffrés et libellés')

    # ── 7. COMPARATEUR : exemple par défaut ───────────────────────────────
    pg.click('.tabs button[data-go="rank"]'); pg.wait_for_timeout(300)
    pg.click('#rankTable tbody tr:first-child'); pg.wait_for_timeout(400)
    pg.click('#sheet [data-go="cmp"]'); pg.wait_for_timeout(600)
    a, bb = pg.input_value('#cmpA'), pg.input_value('#cmpB')
    check((a, bb) == ('Hodh El Gharbi', 'Guidimakha'), 'comparaison par défaut prête',
          f'{a} / {bb}')
    check(pg.locator('#cmpOut .waffle').count() == 2, '2 grilles côte à côte')

    # ── 8. TROIS LANGUES ──────────────────────────────────────────────────
    for lg, dirn, mot in [('ar', 'rtl', 'الخريطة'), ('en', 'ltr', 'Ranking'), ('fr', 'ltr', 'Classement')]:
        pg.click(f'.langs button[data-lang="{lg}"]'); pg.wait_for_timeout(600)
        check(pg.get_attribute('html', 'dir') == dirn, f'sens de lecture {lg} = {dirn}')
        check(mot in pg.inner_text('#tabs'), f'navigation traduite en {lg}', mot)
    pg.click(f'.langs button[data-lang="ar"]'); pg.wait_for_timeout(500)
    pg.click('.tabs button[data-go="rank"]'); pg.wait_for_timeout(300)
    pg.click('#rankTable tbody tr:first-child'); pg.wait_for_timeout(500)
    ar_act = pg.inner_text('#sheet .acts')
    check('مدارس' in ar_act or 'قاعة' in ar_act, 'actions traduites en arabe',
          ar_act[:40].replace('\n', ' '))
    pg.click('.tabs button[data-go="map"]'); pg.wait_for_timeout(500)
    ov = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check(ov <= 0, 'carte en arabe sans débordement', f'{ov}px')
    nb = pg.eval_on_selector_all('.lbl u', "els=>els.map(e=>e.textContent.trim())")
    check(sorted(int(x) for x in nb) == list(range(1, 14)), 'étiquettes intactes en RTL')

    # ── 9. VALEUR MANQUANTE : la page ne casse pas ────────────────────────
    pg.click('.langs button[data-lang="fr"]'); pg.wait_for_timeout(400)
    pg.evaluate("""()=>{ const w=DATA.find(x=>x.wilaya==='Tagant');
        w.taux_pauvrete=null; w.enfants_hors_ecole=null; w.explication=null;
        currentSheet='Tagant'; drawSheet(); go('sheet'); }""")
    pg.wait_for_timeout(400)
    txt = pg.inner_text('#sheet')
    check('—' in txt, 'valeur manquante affichée « — » sans planter')
    check(not errs, 'aucune erreur JavaScript', errs[:3])
    pg.close()

    # ── 10. RENDU SUR GRAND ÉCRAN ─────────────────────────────────────────
    pg = b.new_page(viewport={'width': 1400, 'height': 900})
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(1200)
    ov = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check(ov <= 0, 'aucun débordement horizontal sur grand écran', f'{ov}px')
    hero = pg.eval_on_selector('.hero', """e=>{const r=e.getBoundingClientRect();
        return {x:Math.round(r.x), w:Math.round(r.width),
                bg:getComputedStyle(e).backgroundImage.slice(0,18)};}""")
    check('gradient' in hero['bg'], 'bandeau d\'accroche en place', hero['bg'])
    check(hero['x'] >= -1, 'le bandeau ne déborde pas à gauche', hero['x'])
    pg.click('.tabs button[data-go="map"]'); pg.wait_for_timeout(700)
    noms = pg.eval_on_selector_all('#mapbox .lbl span',
        "els=>els.filter(e=>getComputedStyle(e).display!=='none').length")
    check(noms == 13, 'les 13 noms sont écrits sur la carte (grand écran)', noms)
    lb = pg.eval_on_selector_all('#mapbox .lbl', """els=>els.map(e=>{const r=e.getBoundingClientRect();
        return {n:e.dataset.w,x:r.x,y:r.y,w:r.width,h:r.height};})""")
    ch = [(a['n'], c['n']) for a, c in itertools.combinations(lb, 2)
          if a['x'] < c['x']+c['w'] and c['x'] < a['x']+a['w']
          and a['y'] < c['y']+c['h'] and c['y'] < a['y']+a['h']]
    check(not ch, 'aucun nom ne se chevauche (grand écran)', ch[:3])
    # disposition Atlas
    pg.click('.tabs button[data-go="home"]'); pg.wait_for_timeout(600)
    at = pg.eval_on_selector('.atlas', "e=>getComputedStyle(e).gridTemplateColumns")
    check(len(at.replace(', ', ',').split()) == 2,
          'accueil en deux colonnes sur grand écran', at)
    check(pg.eval_on_selector('.atlas-map', "e=>getComputedStyle(e).position") == 'sticky',
          'la carte reste fixe pendant le défilement')
    check(pg.locator('#homeMap .lbl').count() == 13,
          '13 wilayas cliquables sur la carte du tableau de bord')
    wr = pg.eval_on_selector('.wrap', "e=>Math.round(e.getBoundingClientRect().width)")
    check(wr > 1100, "la page s'élargit sur l'accueil", f'{wr}px')
    dg = pg.eval_on_selector('.atlas-flow .dashgrid', "e=>getComputedStyle(e).gridTemplateColumns")
    check(len(dg.replace(', ', ',').split()) == 2,
          'la colonne droite tient en deux colonnes', dg)
    hp = pg.eval_on_selector('.atlas-flow .waffle i',
        "e=>Math.round(e.getBoundingClientRect().height)")
    check(20 <= hp <= 60, 'personnes à taille raisonnable en colonne', f'{hp}px')
    creux = pg.eval_on_selector_all('.atlas-flow .tile', """els=>els.filter(e=>{
        const h=e.getBoundingClientRect().height; let c=0;
        for(const k of e.children) c+=k.getBoundingClientRect().height;
        return h - c > 95;}).length""")
    check(creux == 0, 'aucune tuile creuse en colonne droite', creux)
    # un clic sur la carte du tableau de bord ouvre la fiche
    pg.eval_on_selector('#homeMap .lbl[data-w="Guidimakha"]', 'e=>e.click()')
    pg.wait_for_timeout(500)
    check('Guidimakha' in pg.inner_text('#sheet'),
          'clic sur la carte du tableau de bord → fiche wilaya')
    # les autres écrans n'ont pas changé
    pg.click('.tabs button[data-go="map"]'); pg.wait_for_timeout(500)
    wr2 = pg.eval_on_selector('.wrap', "e=>Math.round(e.getBoundingClientRect().width)")
    check(wr2 < 1000, "les autres écrans gardent leur largeur d'origine", f'{wr2}px')
    check(pg.locator('#mapbox .lbl').count() == 13, "l'écran Carte est intact")
    # ── 11. CONTRASTE DU TEXTE SUR L'ÉCHELLE DE PRIORITÉ ─────────────────
    pg.click('.tabs button[data-go="map"]'); pg.wait_for_timeout(600)
    def lum(c):
        r, g, bl = [int(x)/255 for x in c[c.find('(')+1:c.find(')')].split(',')[:3]]
        f = lambda v: v/12.92 if v <= .03928 else ((v+.055)/1.055)**2.4
        return .2126*f(r) + .7152*f(g) + .0722*f(bl)
    duos = pg.eval_on_selector_all('#mapbox .lbl u', """els=>els.map(e=>{
        const s=getComputedStyle(e); return [s.backgroundColor, s.color];})""")
    ratios = []
    for bgc, fgc in duos:
        a, z = lum(bgc), lum(fgc)
        ratios.append(round((max(a, z)+.05)/(min(a, z)+.05), 2))
    check(min(ratios) >= 4.5,
          'texte lisible sur les 4 niveaux de priorité (contraste ≥ 4,5:1)',
          f'minimum {min(ratios)}:1')
    # ── 12. RIEN NE TRAVERSE LES BARRES FIXES ────────────────────────────
    lg = pg.eval_on_selector('#tabs', "e=>Math.round(e.getBoundingClientRect().width)")
    vp = pg.evaluate("document.documentElement.clientWidth")
    check(lg >= vp - 1, "la barre d'onglets occupe toute la largeur", f'{lg} / {vp}')
    hb = pg.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--barh')")
    reel = pg.eval_on_selector('.topbar', "e=>Math.ceil(e.getBoundingClientRect().height)")
    check(hb.strip() == f'{reel}px', "hauteur d'en-tête mesurée, pas devinée",
          f'{hb.strip()} vs {reel}px')

    for ecran in ['home', 'map', 'rank', 'sim', 'meth']:
        pg.click(f'.tabs button[data-go="{ecran}"]'); pg.wait_for_timeout(350)
        pg.evaluate("window.scrollTo(0, 700)"); pg.wait_for_timeout(300)
        intrus = pg.evaluate("""()=>{
            const bar=document.querySelector('.topbar').getBoundingClientRect();
            const tabs=document.getElementById('tabs').getBoundingClientRect();
            const bad=[];
            const W=document.documentElement.clientWidth;
            for(const [zone,r] of [['bar',bar],['tabs',tabs]])
              for(const x of [6, W*0.25, W*0.5, W*0.75, W-6]){
                const e=document.elementFromPoint(x, r.top+r.height/2);
                if(!e) { bad.push(zone+':vide'); continue; }
                if(!e.closest('.topbar') && !e.closest('#tabs')) bad.push(zone+':'+(e.className||e.tagName));
              }
            return bad;}""")
        check(not intrus, f'rien ne traverse les barres — écran {ecran}', intrus[:3])
    pg.evaluate("window.scrollTo(0,0)")

    # en arabe aussi
    pg.click('.langs button[data-lang="ar"]'); pg.wait_for_timeout(700)
    pg.evaluate("window.scrollTo(0, 700)"); pg.wait_for_timeout(300)
    intrus = pg.evaluate("""()=>{
        const tabs=document.getElementById('tabs').getBoundingClientRect(); const bad=[];
        const W=document.documentElement.clientWidth;
        for(const x of [6, W*0.25, W*0.5, W*0.75, W-6]){
          const e=document.elementFromPoint(x, tabs.top+tabs.height/2);
          if(e && !e.closest('.topbar') && !e.closest('#tabs')) bad.push(e.className||e.tagName);}
        return bad;}""")
    check(not intrus, 'rien ne traverse les barres en arabe', intrus[:3])
    pg.click('.langs button[data-lang="fr"]'); pg.wait_for_timeout(600)
    # ── 13. AUCUN ÉLÉMENT DE CONTENU NE DOIT ÊTRE COLLANT ────────────────
    # Une collision de noms de classe avait rendu chaque ligne de graphique
    # sticky, bleue et au-dessus de tout. Ce test l'aurait attrapée.
    pg.click('.tabs button[data-go="home"]'); pg.wait_for_timeout(500)
    colles = pg.evaluate("""()=>{
        const ok=['topbar','tabs','atlas-map'];
        return [...document.querySelectorAll('.wrap *')].filter(e=>{
          const s=getComputedStyle(e);
          if(s.position!=='sticky' && s.position!=='fixed') return false;
          if(e.tagName==='TH') return false;      // en-têtes de tableau : voulu
          return !ok.some(c=>e.classList.contains(c));
        }).map(e=>(e.className||e.tagName).toString().slice(0,26));}""")
    check(not colles, 'aucun élément de contenu collant hors des barres', colles[:4])
    plein = pg.eval_on_selector_all('.bars .bar', """els=>els.filter(e=>{
        const b=getComputedStyle(e).backgroundColor;
        return b!=='rgba(0, 0, 0, 0)' && b!=='transparent';}).length""")
    check(plein == 0, 'les lignes de graphique restent transparentes', plein)
    zz = pg.eval_on_selector_all('.wrap *', """els=>els.map(e=>parseInt(getComputedStyle(e).zIndex))
        .filter(v=>!isNaN(v) && v>=29)""")
    check(not zz, "aucun contenu au niveau des barres dans l'ordre d'empilement", zz[:5])
    check(not errs, 'aucune erreur JavaScript sur grand écran', errs[:3])

    b.close()

print(f"\n{'='*70}\nRÉUSSIS {len(ok)}   ÉCHOUÉS {len(ko)}\n{'='*70}")
for x in ok: print('  ✓', x)
if ko:
    print('\n  ÉCHECS :')
    for x in ko: print('  ✗', x)
