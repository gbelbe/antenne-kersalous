"""Paragraphes complets d'une décision contenant un motif. Usage : para.py <dépôt> <id> <regex> [max]"""
import sys,re,html,csv
repo,i,rx=sys.argv[1:4]; mx=int(sys.argv[4]) if len(sys.argv)>4 else 700
parts=i.split("-"); num=parts[2]; date=parts[3]
for r in csv.DictReader(open(f"{repo}/corpus/manifest.csv",encoding="utf-8")):
    if r["fichier"].lower().endswith(f"_{date}.xml") and num in re.sub(r"[^a-z0-9]","",r["fichier"].lower()): break
b=open(f"{repo}/{r['fichier']}",encoding="utf-8").read()
t=html.unescape(re.sub(r"<[^>]+>","\n",b[b.find("Texte_Integral"):]))
for p in [re.sub(r"\s+"," ",p).strip() for p in t.split("\n")]:
    if re.search(rx,p,re.I) and not p.startswith("- ") : print("*",p[:mx]); print()
