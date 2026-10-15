"""Derniers paragraphes de motifs avant les frais et le dispositif (là où le juge conclut). Usage : motif.py <dépôt> <id>... """
import sys,re,html,csv
repo=sys.argv[1]
man=list(csv.DictReader(open(f"{repo}/corpus/manifest.csv",encoding="utf-8")))
for i in sys.argv[2:]:
    parts=i.split("-"); num=parts[2]; date=parts[3]
    r=next(r for r in man if r["fichier"].lower().endswith(f"_{date}.xml") and num in re.sub(r"[^a-z0-9]","",r["fichier"].lower()))
    b=open(f"{repo}/{r['fichier']}",encoding="utf-8").read()
    t=html.unescape(re.sub(r"<[^>]+>","\n",b[b.find("Texte_Integral"):]))
    ps=[re.sub(r"\s+"," ",p).strip() for p in t.split("\n") if len(p.strip())>40]
    e=next((n for n,p in enumerate(ps) if re.match(r"Article 1",p)),len(ps))
    mot=[p for p in ps[:e] if not p.startswith("- ")]
    # coupe avant « Sur les frais »
    f=next((n for n,p in enumerate(mot) if re.match(r"(?:\d+\. )?Sur les frais|Sur les frais",p)),len(mot))
    seg=[p for p in mot[:f] if re.search(r"fond[ée]e? à|à bon droit|à tort|ne sont pas fondée?s|n.est pas fondée|doit être (?:annulé|rejeté)|méconna|entach|vice|substitu",p)]
    print("==",i,r["juridiction"][-22:],r["numero"],r["date_lecture"])
    for p in (seg[-3:] if seg else mot[max(0,f-2):f]): print(" *",p[:360])
