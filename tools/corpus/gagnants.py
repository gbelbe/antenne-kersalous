"""Moyens accueillis : paragraphes qui retiennent un vice + dispositif. Usage : gagnants.py <dépôt> <id>..."""
import sys,re,html,csv
repo=sys.argv[1]
man=list(csv.DictReader(open(f"{repo}/corpus/manifest.csv",encoding="utf-8")))
KEY=re.compile(r"sont fondés à|est fondé à|moyen[^.]{0,60}(?:est fondé|est de nature|doit être accueilli|est établi)|méconna(?:ît|issent|it)|est entaché|entachée? d'(?:illégalité|erreur)|est illégale?|doute sérieux quant à la légalité[^.]{0,80}(?:est|sont) de nature|a commis une erreur|doit être annulé|susceptible d'être régularisé|vice",re.I)
for i in sys.argv[2:]:
    parts=i.split("-"); num=parts[2]; date=parts[3]
    r=next(r for r in man if r["fichier"].lower().endswith(f"_{date}.xml") and num in re.sub(r"[^a-z0-9]","",r["fichier"].lower()))
    b=open(f"{repo}/{r['fichier']}",encoding="utf-8").read()
    t=html.unescape(re.sub(r"<[^>]+>","\n",b[b.find("Texte_Integral"):]))
    ps=[re.sub(r"\s+"," ",p).strip() for p in t.split("\n") if len(p.strip())>40]
    k=next((n for n,p in enumerate(ps) if re.match(r"(?:1\. |Considérant|Sur les conclusions)",p)),0)
    mot=[p for p in ps[k:] if not p.startswith("- ")]
    e=next((n for n,p in enumerate(mot) if re.match(r"Article 1",p)),len(mot))
    hit=[p for p in mot[:e] if KEY.search(p) and not re.match(r"(?:\d+\. )?(?:Aux termes|Il résulte des dispositions|En vertu)",p)]
    req=next((p for p in ps if re.search(r"\bdemand(?:e|ent)\b",p)),"")
    print("=====",i,r["juridiction"][-22:],r["numero"],r["date_lecture"])
    print("REQ:",req[:260])
    n=0
    for p in hit[-4:]:
        print(" *",p[:420]); n+=420
    d=mot[e] if e<len(mot) else ""
    print(" D:",d[:230])
