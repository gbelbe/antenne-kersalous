"""Taux de réussite des tiers (riverains, associations, syndicats, préfet, communes) contre une autorisation d'antenne, tribunaux administratifs.
Croise le type de requérant (lu dans le texte), l'acte attaqué (dispositif et première mention) et la solution enregistrée.
Usage : taux.py <dépôt>   (après verif_victoires.py et build_decisions.py)"""
import sys,json,re,collections,html
repo=sys.argv[1]
V=json.load(open("/tmp/verif2.json")); C={x["id"]:x for x in json.load(open(f"{repo}/corpus/classement.json"))}
SAT=("Satisfaction totale","Satisfaction partielle","Suspension accordée","Sursis à statuer")
tab=collections.defaultdict(collections.Counter); n=0
rows=[]
for r in V:
    if r["niveau"]!="TA": continue
    did=f"dec-ta-{re.sub(r'[^a-z0-9]+','-',r['num'].lower()).strip('-')}-{r['date'].replace('-','')}"
    c=C.get(did)
    if not c: continue
    fav=r["act"]=="favorable" or (r["act"] in("inconnu","mixte","defavorable") and r["first"]=="favorable")
    if not fav: continue
    b=open(f"{repo}/{r['fichier']}",encoding="utf-8").read()
    if len(re.findall(r"antenne|pylône|radiotéléphon|téléphonie|station relais",b,re.I))<8: continue
    t=c["req"][0]
    if t in("q-operateur","q-indetermine"): continue
    sol=r["sol"]
    out=("gagné (annulation totale)" if sol=="Satisfaction totale" else "gagné en partie" if sol=="Satisfaction partielle" else "sursis pour régulariser" if sol=="Sursis à statuer" else "suspension" if sol=="Suspension accordée"
         else "désistement ou non-lieu" if sol.startswith(("Désistement","Non-lieu")) else "irrecevable" if "irrecev" in sol.lower() else "rejeté")
    tab[t][out]+=1; tab["TOUS"][out]+=1; tab["TOUS_"+r["stade"]][out]+=1
    rows.append((did,t,out,r["stade"]))
names={"q-riverains":"riverains","q-association":"association/collectif","q-syndicat":"syndicat/SCI","q-prefet":"préfet (déféré)","q-commune":"commune","TOUS":"TOUS","TOUS_fond":"dont au fond","TOUS_référé":"dont en référé"}
cols=["gagné (annulation totale)","gagné en partie","sursis pour régulariser","suspension","rejeté","irrecevable","désistement ou non-lieu"]
print("| requérant | n | "+" | ".join(cols)+" | gagné ou sursis |")
for k in ["q-riverains","q-association","q-syndicat","q-prefet","q-commune","TOUS","TOUS_fond","TOUS_référé"]:
    c=tab[k]; tot=sum(c.values())
    if not tot: continue
    w=c["gagné (annulation totale)"]+c["gagné en partie"]+c["sursis pour régulariser"]+c["suspension"]
    print(f"| {names[k]} | {tot} | "+" | ".join(str(c[x]) for x in cols)+f" | {w} ({100*w/tot:.0f} %) |")
json.dump(rows,open("/tmp/taux_rows.json","w"))
out=[]
for k in ["q-riverains","q-association","q-syndicat","q-prefet","q-commune","TOUS","TOUS_fond","TOUS_référé"]:
    c=tab[k]; tot=sum(c.values())
    if tot: out.append({"requerant":names[k],"n":tot,**{x:c[x] for x in cols},"gagne":c["gagné (annulation totale)"]+c["gagné en partie"]+c["sursis pour régulariser"]+c["suspension"]})
json.dump({"colonnes":cols,"lignes":out,"date":"2026-10-15"},open(f"{repo}/corpus/taux.json","w"),ensure_ascii=False,indent=1)
