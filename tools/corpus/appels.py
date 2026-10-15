"""Classe les arrêts de cour d'appel et décisions du Conseil d'État : sens du jugement de première instance, acte en cause, résultat de l'appel.
Usage : appels.py <dépôt> -> /tmp/appels.json"""
import sys,re,html,csv,json,collections
repo=sys.argv[1]
idx={x["fichier_opendata"].split("/")[1]:x for x in csv.DictReader(open(f"{repo}/corpus/index_decisions.csv",encoding="utf-8"))}
FAV=re.compile(r"ne s.est pas opposée?|n.a pas (?:fait )?opposition|non[- ]opposition|décision tacite|a accordé|a délivré|délivrant|a autorisé|autorisant|permis de construire (?:n°|délivré|accordé|tacite)|permis tacite",re.I)
UNF=re.compile(r"(?<!pas )(?<!pas fait )s.est opposée?|a fait opposition|décision d.opposition|a refusé|refus|a retiré|retrait|sursis à statuer|prescription|interruptif",re.I)
OP=re.compile(r"\b(?:Free|Orange|Bouygues|SFR|Cellnex|Hivory|ATC|Totem|TDF|Phoenix|Towercast|On Tower|Telco|Axians|Infracos|FPS|Altitude|Itas|Circet|Eiffage)\b|société[^,.]{0,40}(?:infrastructure|télécom|mobile|tower)",re.I)
out=[]
for r in csv.DictReader(open(f"{repo}/corpus/manifest.csv",encoding="utf-8")):
    if r["niveau"]=="TA": continue
    x=idx[r["fichier"].split("/")[-1]]
    b=open(f"{repo}/{r['fichier']}",encoding="utf-8").read()
    t=html.unescape(re.sub(r"<[^>]+>","\n",b[b.find("Texte_Integral"):]))
    ps=[re.sub(r"\s+"," ",p).strip() for p in t.split("\n") if len(p.strip())>15]
    full=" ".join(ps)
    n=len(re.findall(r"antenne|pylône|radiotéléphon|téléphonie|station relais|radioélectrique",full,re.I))
    if n<6: continue
    k=next((i for i,p in enumerate(ps) if re.match(r"Article 1",p)),None)
    dispo=" ".join(ps[k:k+4])[:900] if k is not None else ""
    # jugement de première instance : phrase qui suit « jugement ... du ..., le tribunal administratif de X a »
    m=re.search(r"(?:jugement|ordonnance)[^.]{0,120}?(?:tribunal administratif|juge des référés)[^.]{0,80}?\b(a annulé|a rejeté|a fait droit|a suspendu|a donné acte|a prononcé un non-lieu|a enjoint|a sursis|a mis fin|annulé|rejeté)[^.]{0,420}",full)
    ta_verb=m.group(1) if m else ""
    ta_seg=m.group(0) if m else ""
    ta_fav=bool(FAV.search(ta_seg)) and not UNF.search(ta_seg)
    ta_unf=bool(UNF.search(ta_seg)) and not FAV.search(ta_seg)
    ta_dir="annule" if ta_verb in("a annulé","a fait droit","a suspendu","annulé") else "rejette" if ta_verb in("a rejeté","rejeté") else ta_verb or "?"
    rev=bool(re.search(r"(?:jugement|ordonnance)[^.]{0,140}(?:est annulée?|sont annulés?)|annule (?:le|l.) (?:jugement|ordonnance)|arrêt[^.]{0,60}est annulé",dispo,re.I))
    rej=bool(re.search(r"(?:requête|pourvoi|appel)[^.]{0,160}(?:est rejetée?|n.est pas admis|sont rejetés?)|rejette|non admis",dispo,re.I)) and not rev
    # qui fait appel
    ap=re.search(r"(?:Par une requête|Par un pourvoi|Par une requête sommaire)[^,]{0,140},?([^.]{0,260}?)\b(?:demande|demandent|conclut|conclu)",full)
    appelant=ap.group(1) if ap else ""
    apc="operateur" if OP.search(appelant) else "commune" if re.search(r"commune|ville|métropole|communauté",appelant,re.I) else "ministre/prefet" if re.search(r"ministre|préfet",appelant,re.I) else "tiers" if re.search(r"\bM\. |\bMme |consorts|association|syndicat|SCI",appelant) else "?"
    out.append(dict(num=x["num"],niveau=r["niveau"],date=r["date_lecture"],jur=r["juridiction"],sol=x["solution"],ta_dir=ta_dir,ta_fav=ta_fav,ta_unf=ta_unf,rev=rev,rej=rej,appelant=apc,dispo=dispo[:260],fichier=r["fichier"],n=n))
json.dump(out,open("/tmp/appels.json","w"),ensure_ascii=False)
print(len(out),"décisions d'appel ou de cassation sur antennes")
c=collections.Counter((o["niveau"],o["ta_dir"],"FAV" if o["ta_fav"] else "UNF" if o["ta_unf"] else "?","reforme" if o["rev"] else "maintient" if o["rej"] else "autre") for o in out)
for k,v in sorted(c.items(),key=lambda kv:-kv[1])[:30]: print(k,v)
