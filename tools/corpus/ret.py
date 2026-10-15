import sys,json,re,html
S=sys.argv[1]; ids=sys.argv[2].split(",")
d={x["num"]+"|"+x["date"]:x for x in json.load(open(S+"/data/scored.json"))}
POS=re.compile(r"(?<!il y a lieu de faire application)fondée?s? à (?:soutenir|se prévaloir|demander|invoquer)|doit être accueilli|sont? entachée?s?|est entaché|a (?:commis une erreur|méconnu|fait une inexacte|entaché)|méconnaît|méconnu|illégalité|doit être annulé|sont? illégal|vice",re.I)
NEG=re.compile(r"n'est pas fondé|ne sont pas fondés|doit être écarté|ne peut qu'être écarté|inopérant|aucune erreur|n'est pas établi|n'est pas entaché|ne méconnaît pas|n'a pas méconnu|ne sont pas établis|pas fondé",re.I)
def paras(x):
    b=open(S+"/data/raw/"+x["file"],encoding="utf-8",errors="replace").read()
    t=re.sub(r"</p>\s*","\n",b[b.find("<Texte_Integral>"):]);t=re.sub(r"<[^>]+>","",t);t=html.unescape(t)
    return [re.sub(r"\s+"," ",p.strip()) for p in t.split("\n") if p.strip()]
for i in ids:
    x=d[i];ps=paras(x);txt=" ".join(ps)
    print(f"\n#### {x['juridiction'].replace('Tribunal Administratif','TA').replace('Cour administrative d\'appel','CAA').replace('COUR ADMINISTRATIVE D\'','CAA ').replace('Cour administrative d\'','CAA ')[:20]} {x['date']} n°{x['num']} {x['stade']} {x['plaignant'][:6]}|{x['acte'][:9]}|{x['solution'][:12]}|{x['avocat_req'][:22]}|{','.join(x['ops'])}")
    m=re.search(r"(?:pylône|mât)[^.]{0,160}?(?:\d+(?:,\d+)? ?m(?:ètres)?)[^.]{0,60}\.",txt)
    if m: print("OBJET:",m.group(0)[:170])
    z=re.findall(r"[^.]{0,40}(?:zone\s+(?:U[A-Za-z]*|AU[a-z]*|A[a-z]*|N[a-z]*)\b)[^.]{0,40}",txt)[:1]
    if z:print("ZONE:",z[0][:100])
    dd=re.findall(r"[^.]{0,60}\b\d+\s*(?:mètres|m)\b[^.]{0,30}(?:habitation|maison|domicile|propriété|résid)[^.]{0,40}",txt)[:1]
    if dd:print("DIST:",dd[0][:140])
    dec=next((k for k,p in enumerate(ps) if p.startswith("DÉCIDE")),len(ps))
    n=0
    sel=[]
    for p in ps[:dec]:
        if not re.match(r"\d+\. ",p): continue
        if re.search(r"fin de non-recevoir|intérêt (?:pour )?agir|761-1|frais exposés|L\. 600-4-1",p) and not re.search(r"fondée?s? à",p): continue
        if re.search(r"fondée?s? à (?:soutenir|se prévaloir|demander|invoquer)|doit être accueilli|est entaché|a commis une erreur|a fait une inexacte|a méconnu|méconnaît|ne pouvait|aurait dû|devait",p) and not NEG.search(p[-260:]) and not re.match(r"\d+\. Il résulte de (?:ces|tout|ce qui)",p) and not re.search(r"600-5|L\. 761",p[:200]):
            sel.append(p)
    for p in sel[-2:]:
        print("  RET:",p[:110].strip(),"…",p[-250:] if len(p)>360 else p[110:])
