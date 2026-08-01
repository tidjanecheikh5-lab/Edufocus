import re, os, glob
from PIL import ImageFont
FR={'400':'Poppins-Regular.ttf','500':'Poppins-Medium.ttf','600':'Poppins-SemiBold.ttf',
    '700':'Poppins-Bold.ttf','800':'Poppins-ExtraBold.ttf'}
BASE=os.path.dirname(glob.glob('/usr/share/fonts/**/Poppins-Regular.ttf',recursive=True)[0])
def pol(w,sz):
    p=os.path.join(BASE,FR.get(str(w),'Poppins-Regular.ttf'))
    return ImageFont.truetype(p if os.path.exists(p) else os.path.join(BASE,'Poppins-Regular.ttf'),int(sz))

def analyse(f,nom,W=1200):
    svg=open(f).read()
    # tous les rectangles conteneurs (cards, cadres d'image, tuiles internes)
    rects=[]
    for m in re.finditer(r'<rect x="([\d.-]+)" y="([\d.-]+)" width="([\d.]+)" height="([\d.]+)" rx="(\d+)"',svg):
        x,y,w,h,rx=[float(v) for v in m.groups()]
        if w>60 and h>40: rects.append((x,y,w,h))
    txts=[]
    for m in re.finditer(r'<text x="([\d.]+)" y="([\d.]+)" font-size="([\d.]+)" fill="[^"]*" '
                         r'font-weight="(\d+)" text-anchor="(\w+)" letter-spacing="([-\d.]+)"[^>]*>([^<]*)</text>',svg):
        x,y,fs,w,anc,ls,t=m.groups(); x,y,fs,ls=float(x),float(y),float(fs),float(ls)
        c=re.sub('<[^>]+>','',t)
        if not c.strip(): continue
        lg=pol(w,fs).getlength(c)+ls*max(0,len(c)-1)
        x0=x if anc=='start' else x-lg/2 if anc=='middle' else x-lg
        txts.append({'t':c[:46],'x0':x0,'x1':x0+lg,'y':y,'fs':fs})
    # pour chaque texte, le plus petit rect qui contient son point d'ancrage
    pb=[]
    for z in txts:
        cand=[r for r in rects if r[0]<=z['x0']+3<=r[0]+r[2] and r[1]<=z['y']<=r[1]+r[3]]
        if not cand: continue
        r=min(cand,key=lambda r:r[2]*r[3])
        marge=6
        if z['x1']>r[0]+r[2]-marge:
            pb.append((round(z['x1']-(r[0]+r[2]))," dépasse à droite de",z['t']))
        if z['x0']<r[0]+marge-4:
            pb.append((round(r[0]-z['x0'])," dépasse à gauche de",z['t']))
    print(f"\n=== {nom} · {len(txts)} textes, {len(rects)} cadres")
    print(f"  textes qui sortent de leur cadre : {len(pb)}")
    for d,s_,t in sorted(pb,reverse=True)[:12]: print(f"     {d:>4} px{s_} : « {t} »")
    return pb

analyse('infographie.svg','INFOGRAPHIE')
analyse('uiux.svg','UI/UX')
