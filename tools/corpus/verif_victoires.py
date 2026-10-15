"""Vérifie le repérage des victoires de tiers (riverains, associations, préfet) contre une autorisation en croisant
(A) la solution enregistrée par la juridiction (métadonnée) et (B) la nature de l'acte annulé ou suspendu dans le dispositif.
Usage : verif_victoires.py <dépôt>  -> /tmp/verif.json"""
import sys,re,html,csv,json,collections
repo=sys.argv[1]
idx={x["fichier_opendata"].split("/")[1]:x for x in csv.DictReader(open(f"{repo}/corpus/index_decisions.csv",encoding="utf-8"))}
FAV=re.compile(r"ne s.est pas opposée?|n.a pas (?:fait )?opposition|n.a pas fait opposition|non[- ]opposition|décision tacite|a accordé|a délivré|délivrant|accordant|a autorisé|autorisant|permis de construire n°|permis de construire (?:délivré|accordé)",re.I)
UNF=re.compile(r"(?<!pas )(?<!pas fait )s.est opposée?|a fait opposition|décision d.opposition|portant opposition|arrêté d.opposition|a refusé|refus|a retiré|retrait|sursis à statuer sur la demande|a rejeté la demande|arrêté interruptif|opposition à la déclaration",re.I)
rows=[]
for r in csv.DictReader(open(f"{repo}/corpus/manifest.csv",encoding="utf-8")):
    x=idx[r["fichier"].split("/")[-1]]
    b=open(f"{repo}/{r['fichier']}",encoding="utf-8").read()
    t=html.unescape(re.sub(r"<[^>]+>","\n",b[b.find("Texte_Integral"):]))
    ps=[re.sub(r"\s+"," ",p).strip() for p in t.split("\n") if len(p.strip())>15]
    k=next((n for n,p in enumerate(ps) if re.match(r"Article 1",p)),None)
    dispo=" ".join(ps[k:k+5])[:1500] if k is not None else ""
    # phrase du dispositif qui annule / suspend
    sent=[s for s in re.split(r"(?<=[.;])\s+|Article \d+(?:er)? ?:",dispo) if re.search(r"annul|suspend|sursis",s,re.I)]
    sj=" ".join(sent)[:700]
    f=bool(FAV.search(sj)); u=bool(UNF.search(sj))
    act="favorable" if f and not u else "defavorable" if u and not f else "mixte" if f and u else "inconnu"
    head=" ".join(ps[:(k or 12)])
    ta_ann=re.search(r"a annulé[^.]{0,350}",head)
    ta_act="inconnu"
    if ta_ann:
        tf=bool(FAV.search(ta_ann.group(0))); tu=bool(UNF.search(ta_ann.group(0)))
        ta_act="favorable" if tf and not tu else "defavorable" if tu and not tf else "inconnu"
    rows.append(dict(num=x["num"],niveau=r["niveau"],date=r["date_lecture"],jur=r["juridiction"],sol=x["solution"],stade=x["stade"],
        act=act,ta_act=ta_act,plaig=x["plaignant"],dispo=sj[:300],fichier=r["fichier"]))
json.dump(rows,open("/tmp/verif.json","w"),ensure_ascii=False)
SAT=("Satisfaction totale","Satisfaction partielle","Suspension accordée","Sursis à statuer")
c=collections.Counter()
for r in rows:
    sat=r["sol"] in SAT
    c[(r["niveau"],"satisfaction" if sat else "autre",r["act"] if r["niveau"]=="TA" else r["ta_act"])]+=1
for k,v in sorted(c.items()): print(k,v)
