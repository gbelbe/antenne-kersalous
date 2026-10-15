"""Intertitres de motifs + dispositif, très court. Usage : titres.py <dépôt> <id>..."""
import sys,re,html,csv
repo=sys.argv[1]
man=list(csv.DictReader(open(f"{repo}/corpus/manifest.csv",encoding="utf-8")))
for i in sys.argv[2:]:
    parts=i.split("-"); num=parts[2]; date=parts[3]
    r=next(r for r in man if r["fichier"].lower().endswith(f"_{date}.xml") and num in re.sub(r"[^a-z0-9]","",r["fichier"].lower()))
    b=open(f"{repo}/{r['fichier']}",encoding="utf-8").read()
    t=html.unescape(re.sub(r"<[^>]+>","\n",b[b.find("Texte_Integral"):]))
    ps=[re.sub(r"\s+"," ",p).strip() for p in t.split("\n") if len(p.strip())>15]
    print("==",i,r["juridiction"][-18:],r["numero"],r["date_lecture"])
    hs=[p[:105] for p in ps if re.match(r"(?:\d+\. )?(?:En ce qui concerne|S.agissant|Sur le moyen|Sur (?:la|le|l.)|En (?:premier|deuxième|troisième|quatrième|cinquième|sixième|dernier) lieu)",p) and not p.startswith("Sur les conclusions")][:9]
    for h in hs: print(" -",h)
    fond=[p[:170] for p in ps if re.search(r"sont fondés à|est fondé à|moyen.{0,40}(?:est fondé|doit être accueilli)|doute sérieux quant à la légalité.{0,60}(?:est de nature|sont de nature)|est de nature à faire naître",p)][:3]
    for f in fond: print(" !",f)
    d=[p for p in ps if re.match(r"Article 1",p)]; print(" D:",d[0][:150] if d else "")
