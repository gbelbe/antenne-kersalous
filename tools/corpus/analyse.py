import sys,json,re,html,collections
S=sys.argv[1]
d=json.load(open(S+"/data/index.json"))
def text(x):
    b=open(S+"/data/raw/"+x["file"],encoding="utf-8",errors="replace").read()
    t=re.sub(r"</p>\s*","\n",b[b.find("<Texte_Integral>"):]);t=re.sub(r"<[^>]+>","",t);return html.unescape(t)
def appel_info(t):
    h=t[:4500]
    m=re.search(r"([^.]{0,260}?)\b(relève(?:nt)? appel|interjette|forme(?:nt)? appel|se pourvoi|demande(?:nt)? à la cour|demande(?:nt)? au Conseil|demande(?:nt)? l'annulation du jugement|demande(?:nt)? d'annuler le jugement|demande(?:nt)? (?:à la cour )?(?:d'annuler|l'annulation) (?:du|le) jugement)",h)
    subj=m.group(1) if m else h[:300]
    if re.search(r"[Ll]a commune|[Ll]a communauté|[Ll]e maire",subj): a="collectivité"
    elif re.search(r"[Aa]ssociation|[Cc]ollectif|syndicat des copropri",subj): a="association/collectif"
    elif re.search(r"société|\bSAS\b|\bSA\b|SARL|\bSCI\b",subj) and re.search(r"Free|Orange|SFR|Bouygues|Cellnex|Hivory|TDF|Phoenix|Totem|ATC|Towercast|On Tower|FPS|Infracos|Axione|Altitude|Tower|Infrastructures|T[ée]l[ée]com|Mobile|Itas",subj): a="opérateur/société pylônes"
    elif re.search(r"\bM\.|\bMme\b|[Cc]onsorts|\bMM\.",subj): a="particuliers/riverains"
    else: a="indéterminé"
    r=re.search(r"tribunal administratif[^.]{0,200}?\b(a annulé|a rejeté|a fait droit|a donné satisfaction|annulant|rejetant|a enjoint)",h,re.I)
    ta=None
    if r:
        v=r.group(1).lower(); ta="annulé" if v in("a annulé","annulant","a fait droit","a enjoint") else "rejeté"
    return a,ta
def issue2(x,t):
    s=x["solution"]; win=s.startswith("Satisfaction"); lose=s.startswith("Rejet")
    if not(win or lose): return "sans décision au fond ("+s+")"
    a,ta=appel_info(t); x["appelant"]=a; x["ta_result"]=ta
    A=x["acte"]
    if ta is None: return "appel : sens indéterminé"
    if A.startswith("non-opposition"):
        first_ann = (ta=="annulé")  # TA a annulé la non-opposition
        if first_ann: return "PROJET ANNULÉ (annulation du TA confirmée)" if lose else "PROJET RÉTABLI (annulation du TA infirmée)"
        return "PROJET MAINTENU (rejet du TA confirmé)" if lose else "PROJET ANNULÉ EN APPEL"
    if A.startswith("opposition"):
        if ta=="annulé": return "PROJET AUTORISÉ (annulation de l'opposition confirmée)" if lose else "OPPOSITION RÉTABLIE (projet bloqué)"
        return "OPPOSITION CONFIRMÉE (projet bloqué)" if lose else "OPPOSITION ANNULÉE EN APPEL (projet autorisé)"
    if A=="permis de construire":
        if ta=="annulé": return "PROJET ANNULÉ (annulation du TA confirmée)" if lose else "PROJET RÉTABLI (annulation du TA infirmée)"
        return "PROJET MAINTENU (rejet du TA confirmé)" if lose else "PROJET ANNULÉ EN APPEL"
    return "autre/indéterminé"
def issue(x):
    P,A,s,CA=x["plaignant"],x["acte"],x["solution"],x["file"].startswith(("CA","CE"))
    win=s.startswith("Satisfaction")
    lose=s.startswith("Rejet")
    if not (win or lose): return "sans décision au fond ("+s+")"
    tiers=P in("particuliers/riverains","association/collectif","collectivité")
    op=P.startswith("opérateur")
    if not CA:
        if tiers and A=="non-opposition à DP": return "PROJET ANNULÉ/SUSPENDU" if win else "PROJET MAINTENU"
        if op and A in("retrait de non-opposition","certificat de non-opposition"): return "PROJET AUTORISÉ (retrait/refus de certificat annulé)" if win else "RETRAIT/REFUS MAINTENU (projet bloqué)"
        if op and A=="opposition à DP": return "PROJET AUTORISÉ (opposition annulée/suspendue)" if win else "OPPOSITION MAINTENUE (projet bloqué)"
        if tiers and A=="permis de construire": return "PROJET ANNULÉ/SUSPENDU" if win else "PROJET MAINTENU"
    else:
        # appel/cassation : le requérant a perdu en première instance (hypothèse)
        if op and A=="non-opposition à DP": return "ANNULATION INFIRMÉE (projet rétabli)" if win else "ANNULATION CONFIRMÉE (projet annulé)"
        if op and A in("retrait de non-opposition","certificat de non-opposition"): return "PROJET AUTORISÉ (retrait/refus de certificat annulé)" if win else "RETRAIT/REFUS MAINTENU (projet bloqué)"
        if op and A=="opposition à DP": return "OPPOSITION ANNULÉE EN APPEL (projet autorisé)" if win else "OPPOSITION CONFIRMÉE (projet bloqué)"
        if tiers and A in("non-opposition à DP","permis de construire"): return "PROJET ANNULÉ EN APPEL" if win else "PROJET MAINTENU EN APPEL"
        if (P=="collectivité") and A=="opposition à DP": return "OPPOSITION ANNULÉE EN APPEL (projet autorisé)" if not win else "OPPOSITION CONFIRMÉE (projet bloqué)"
    return "autre/indéterminé"
RURAL=re.compile(r"lieu-?dit|hameau|zone (?:A|N|Na|Nh|Ah|agricole|naturelle)\b|terres? agricole|champ|parcelle agricole|exploitation agricole|bocage|village|commune rurale",re.I)
URBAN=re.compile(r"toiture|toit-terrasse|terrasse de l'immeuble|copropriété|immeuble|cheminée|façade|en toiture|surélévation|syndicat des copropriétaires|local technique en toiture|clocher",re.I)
HAB=re.compile(r"habitations?|riverain|maisons?|voisin|domicile|résidence",re.I)
for x in d:
    t=text(x); x["_t_len"]=len(t)
    x["issue"]=issue(x) if not x["file"].startswith(("CA","CE")) else issue2(x,t)
    sc=0;why=[]
    if re.search(r"pylône|mât|treillis|autoportant|monopole|tubulaire",t,re.I): sc+=3;why.append("pylône")
    if RURAL.search(t): sc+=2;why.append("rural")
    if HAB.search(t): sc+=1;why.append("habitations")
    m=re.search(r"(\d{2,3}(?:,\d+)?)\s*(?:mètres|m)\s+de\s+haut|hauteur (?:totale |maximale |hors tout )?(?:de|d'environ|de plus de)\s+(\d{2,3}(?:,\d+)?)\s*(?:mètres|m)\b",t)
    if m:
        h=float(((m.group(1) or m.group(2))).replace(",","."));x["h"]=h
        if h>=20: sc+=2;why.append(f"h={h:g}")
    if URBAN.search(t) and not re.search(r"pylône",t,re.I): sc-=4;why.append("toiture")
    if re.search(r"Paris|Hauts-de-Seine|Seine-Saint-Denis|Val-de-Marne",x["juridiction"]): sc-=2
    if re.search(r"zone humide|espace boisé classé|boisement|haie",t,re.I): sc+=1;why.append("zh/eb")
    if re.search(r"monument historique|abords|architecte des bâtiments de France",t,re.I): sc+=1;why.append("abf")
    if re.search(r"34-9-1|dossier d'information|dossier préalable d'information",t): sc+=1;why.append("DIM")
    if x["plaignant"] in("particuliers/riverains","association/collectif"): sc+=3;why.append("tiers")
    x["score"]=sc;x["why"]=why
json.dump(d,open(S+"/data/scored.json","w"),ensure_ascii=False)
c=collections.Counter(x["issue"] for x in d)
for k,v in c.most_common(): print(v,k)
