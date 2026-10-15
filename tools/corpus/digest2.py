"""Résumé de lecture d'une décision : paragraphes qui tranchent un moyen + dispositif. Usage : digest2.py <dépôt> <id>..."""
import sys,re,html,csv
repo=sys.argv[1]
rows={}
for r in csv.DictReader(open(f"{repo}/corpus/manifest.csv",encoding="utf-8")):
    rows[(r["niveau"].lower(),r["numero"].replace(" ","-").lower().replace("/","").replace("--","-"))]=r
def load(i):
    parts=i.split("-"); lvl=parts[1]; num=parts[2]; date=parts[3]
    for r in csv.DictReader(open(f"{repo}/corpus/manifest.csv",encoding="utf-8")):
        if r["fichier"].lower().endswith(f"_{date}.xml") and re.search(rf"_{num}[_ ]",r["fichier"].lower()) or (r["fichier"].lower().endswith(f"_{date}.xml") and num in re.sub(r"[^a-z0-9]","",r["fichier"].lower())):
            return r
for i in sys.argv[2:]:
    r=load(i)
    if not r: print("??",i); continue
    b=open(f"{repo}/{r['fichier']}",encoding="utf-8").read()
    t=html.unescape(re.sub(r"<[^>]+>","\n",b[b.find("Texte_Integral"):]))
    ps=[re.sub(r"\s+"," ",p).strip() for p in t.split("\n") if len(p.strip())>40]
    print("=====",i,r["juridiction"],r["numero"],r["date_lecture"])
    head=[p for p in ps if re.search(r"\bdemand(e|ent)\b|doivent être regardés",p)][:1]
    print("REQ:",head[0][:520] if head else ps[0][:300])
    key=[p for p in ps if re.search(r"écart|inopérant|n'est pas fondé|est fondé|accueill|doit être rejeté|doit être écarté|annul|entache|illégal|irrecevab|intérêt (?:pour )?agir|opposition|ne peut qu'être|soutiennent|soutient|sursis|régularis|suspend|doute sérieux|urgence",p,re.I) and not p.startswith(("Vu ","Considérant"))]
    out=0
    for p in key:
        if out>2300: break
        print("-",p[:330]); out+=min(len(p),330)
    dec=[p for p in ps if re.match(r"(Article 1|D\s?E\s?C\s?I\s?D\s?E|Art\. 1)",p)]
    print("DISPO:",(dec[0][:260] if dec else ps[-8][:260]))
