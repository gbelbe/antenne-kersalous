import sys,json,re,html
S=sys.argv[1]; ids=sys.argv[2].split(","); mx=int(sys.argv[3]) if len(sys.argv)>3 else 9
d={x["num"]+"|"+x["date"]:x for x in json.load(open(S+"/data/scored.json"))}
CUE=re.compile(r"par suite|dès lors|il résulte|en conséquence|doit être (?:écarté|accueilli|rejeté)|ne peut qu'être|est fondé|sont fondés|n'est pas fondé|ne sont pas fondés|est entaché|inopérant|n'est pas établi|ne ressort pas|manque en fait|est de nature|n'est pas de nature|sursis|régularis|annul",re.I)
def paras(x):
    b=open(S+"/data/raw/"+x["file"],encoding="utf-8",errors="replace").read()
    t=re.sub(r"</p>\s*","\n",b[b.find("<Texte_Integral>"):]);t=re.sub(r"<[^>]+>","",t);t=html.unescape(t)
    return [re.sub(r"\s+"," ",p.strip()) for p in t.split("\n") if p.strip()]
for i in ids:
    x=d[i];ps=paras(x);txt=" ".join(ps)
    print(f"\n#### {x['juridiction'].replace('Tribunal Administratif','TA').replace('Cour administrative d\'appel','CAA')[:22]} {x['date']} n°{x['num']} [{x['stade']}] {x['plaignant'][:7]}|{x['acte'][:11]}|{x['solution'][:12]}|{x['avocat_req'][:24]}|{','.join(x['ops'])}")
    m=re.search(r"(?:pylône|mât)[^.]{0,200}?(?:\d+(?:,\d+)? ?m(?:ètres)?)[^.]{0,80}\.",txt)
    if m: print("OBJET:",m.group(0)[:200])
    z=re.findall(r"[^.]{0,50}(?:zone\s+(?:U[A-Za-z]*|AU[a-z]*|A[a-z]*|N[a-z]*)\b)[^.]{0,50}",txt)[:1]
    if z:print("ZONE:",z[0][:120])
    out=[]
    for p in ps:
        if p.startswith("DÉCIDE"):break
        if not re.match(r"\d+\. ",p): continue
        if re.search(r"761-1|frais exposés|fin de non-recevoir|intérêt (?:pour )?agir|qualité pour agir|recevable",p): continue
        if re.match(r"\d+\. (?:Aux termes|Il résulte de ces dispositions|Il résulte des dispositions|D'une part, aux termes)",p) and not re.search(r"Par suite|dès lors|en l'espèce|il ressort",p[100:],re.I): continue
        if CUE.search(p) and (re.search(r"fondé|accueilli|écarté|inopérant|illégal|méconn|entach|erreur|régulari|annul",p[-300:],re.I)):
            out.append("  - "+p[:60].strip()+" … "+(p[-210:] if len(p)>270 else p[60:]))
    print("\n".join(out[-mx:]))
