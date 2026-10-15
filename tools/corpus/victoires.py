"""Repère les décisions où une autorisation d'urbanisme (non-opposition, permis) est annulée, suspendue ou soumise à régularisation,
quel que soit le requérant détecté. Usage : victoires.py <dépôt>  -> /tmp/victoires.json"""
import sys,re,html,csv,json
repo=sys.argv[1]
sys.path.insert(0,f"{repo}/tools/corpus")
from lectures_map import LU,PARTIEL
idx={x["fichier_opendata"].split("/")[1]:x for x in csv.DictReader(open(f"{repo}/corpus/index_decisions.csv",encoding="utf-8"))}
OUT=[]
for r in csv.DictReader(open(f"{repo}/corpus/manifest.csv",encoding="utf-8")):
    x=idx[r["fichier"].split("/")[-1]]
    b=open(f"{repo}/{r['fichier']}",encoding="utf-8").read()
    t=html.unescape(re.sub(r"<[^>]+>","\n",b[b.find("Texte_Integral"):]))
    ps=[re.sub(r"\s+"," ",p).strip() for p in t.split("\n") if len(p.strip())>20]
    k=next((n for n,p in enumerate(ps) if re.match(r"Article 1",p)),None)
    if k is None: continue
    dispo=" ".join(ps[k:k+4])[:900]
    num=x["num"]
    lvl=r["niveau"]
    # acte attaqué à l'origine : dernier « annuler/suspendre ... » de la requête (ou du jugement attaqué en appel)
    head=" ".join(ps[:k])
    m=re.findall(r"(?:d.annuler|annuler|de suspendre|suspendre)[^;]{0,420}",head)
    attaque=" ".join(m)[:1500]
    fav=re.search(r"ne s.est pas opposé|n.a pas fait opposition|non[- ]opposition|décision tacite|a accordé|accordant|a délivré|permis de construire (?:n°|du|délivré)|a autorisé|autorisant",attaque,re.I)
    defav=re.search(r"(?<!pas )s.est opposé|a refusé|refus|opposition à|retrait|retiré|a fait opposition",attaque,re.I)
    cond_fav=bool(fav) and not defav
    win=False; kind=""
    if lvl=="TA":
        if cond_fav and re.search(r"\b(?:est|sont) (?:annulée?s?|suspendue?s?)\b|annulée? en tant|sursis à statuer",dispo,re.I):
            win=True; kind="annulation/suspension/sursis"
    else:
        tx=" ".join(ps)
        ta_annule=re.search(r"a annulé[^.]{0,300}(?:ne s.est pas opposé|n.a pas fait opposition|permis|non[- ]opposition|décision tacite)",tx,re.I)
        if ta_annule and not re.search(r"(?<!pas )s.est opposé|a refusé|refus de",ta_annule.group(0),re.I) and re.search(r"requête[^.]{0,80}est rejetée|rejette|annule le jugement",dispo,re.I):
            win=True; kind="appel"
    if win and num not in LU and num not in PARTIEL:
        n=len(re.findall(r"antenne|pylône|radiotéléphon|téléphonie|station relais",t,re.I))
        OUT.append(dict(num=num,niveau=lvl,date=r["date_lecture"],jur=r["juridiction"],kind=kind,n=n,fichier=r["fichier"],plaig=x["plaignant"]))
json.dump(OUT,open("/tmp/victoires.json","w"),ensure_ascii=False)
import collections
print(len(OUT),collections.Counter((o["niveau"],o["kind"]) for o in OUT), 'pertinentes (n>=8):',sum(o["n"]>=8 for o in OUT))
