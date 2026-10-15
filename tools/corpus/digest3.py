"""Motifs numérotés (début de chaque paragraphe) + dispositif. Usage : digest3.py <dépôt> <id> [max_caractères]"""
import sys,re,html,csv
repo,i=sys.argv[1:3]; mx=int(sys.argv[3]) if len(sys.argv)>3 else 3200
parts=i.split("-"); num=parts[2]; date=parts[3]
for r in csv.DictReader(open(f"{repo}/corpus/manifest.csv",encoding="utf-8")):
    if r["fichier"].lower().endswith(f"_{date}.xml") and num in re.sub(r"[^a-z0-9]","",r["fichier"].lower()): break
b=open(f"{repo}/{r['fichier']}",encoding="utf-8").read()
t=html.unescape(re.sub(r"<[^>]+>","\n",b[b.find("Texte_Integral"):]))
ps=[re.sub(r"\s+"," ",p).strip() for p in t.split("\n") if len(p.strip())>25]
print("=====",i,r["juridiction"],r["numero"],r["date_lecture"])
k=next((n for n,p in enumerate(ps) if re.match(r"1\. ",p) or p.startswith("Considérant")),0)
out=0
for p in ps[k:]:
    if re.match(r"(Article 1|D\s?E\s?C\s?I\s?D\s?E)",p): print("DISPO:",p[:200]); break
    s=p[:250] if re.match(r"\d+\. ",p) else p[:140]
    if out>mx: continue
    print("-",s); out+=len(s)
