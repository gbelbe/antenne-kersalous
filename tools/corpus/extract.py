import sys,os,re,json,glob,html
S=sys.argv[1]
def tag(b,t):
    m=re.search(rf"<{t}>(.*?)</{t}>",b,re.S); return html.unescape(m.group(1).strip()) if m else ""
RELAIS=re.compile(r"antennes?[ -]relais|antennes? de (?:radio|télé)(?:téléphonie|communication)|antennes? de téléphonie|station[s]? (?:de base|radioélectrique)|pylône[s]? (?:de|pour) (?:téléphonie|antenne|radio)|installation[s]? radioélectrique|relais de téléphonie|antennes? 4G|antennes? 5G|réseau de téléphonie mobile|pylône.{0,80}antennes?",re.I)
URBA=re.compile(r"déclaration préalable|permis de construire|code de l'urbanisme|ne s'est pas opposé|s'est opposé",re.I)
OPS={"Free":r"\bFree\b","Orange":r"\bOrange\b","SFR":r"\bSFR\b|Société Française du Radiotéléphone","Bouygues":r"Bouygues","TDF":r"\bTDF\b","Cellnex/Hivory":r"Cellnex|Hivory","Phoenix":r"Phoenix","Totem":r"\bTotem\b","ATC":r"\bATC\b|American Tower","Towercast":r"Towercast","On Tower":r"On Tower","FPS Towers":r"FPS Towers","Infracos":r"Infracos","RTE/autres":r"\bRTE\b"}
GROUNDS={
 "DIM (dossier d'information, L.34-9-1 CPCE)":r"34-9-1|20-13-1|dossier d'information|dossier préalable d'information",
 "Paysage/site (R.111-27)":r"R\.? ?111-27|111-27|atteinte.{0,40}(?:paysage|caractère ou à l'intérêt des lieux)|intérêt des lieux avoisinants",
 "Santé/salubrité (R.111-2)":r"R\.? ?111-2\b|salubrité|sécurité publique",
 "Principe de précaution":r"principe de précaution|article 5 de la charte de l'environnement|charte de l'environnement",
 "Santé/ondes/exposition":r"ondes|champs? électromagnétique|exposition du public|valeurs limites d'exposition|ANFR|décret n° 2002-775|rayonnement",
 "PC requis au lieu de DP (R.421-1/-9, emprise, surface)":r"R\.? ?421-9|R\.? ?421-1\b|aurait dû être soumis à permis|permis de construire.{0,60}(?:requis|nécessaire|exigé)|emprise au sol|surface de plancher",
 "Dossier incomplet/fraude (R.431-, R.431-36, L.600-)":r"dossier.{0,30}incomplet|insuffisant|fraude|R\.? ?431-|R\.? ?423-|inexact|erronée",
 "ABF / monument historique":r"architecte des bâtiments de France|monument historique|abords|site patrimonial|AVAP|SPR",
 "Règlement PLU":r"plan local d'urbanisme|règlement du PLU|PLU|plan d'occupation des sols|\bPOS\b",
 "Loi Littoral":r"loi littoral|L\.? ?121-\d+|littoral",
 "Zone agricole/naturelle":r"zone (?:A|N|Nh|Ah|agricole|naturelle)\b|zone [AN]\b|espaces? naturel",
 "Environnement/biodiversité":r"Natura 2000|ZNIEFF|zone humide|biodiversité|espèces protégées",
 "Habitations/riverains proximité":r"habitations?|riverains?|maisons?|voisin",
 "Intérêt à agir (L.600-1-2)":r"intérêt (?:pour )?agir|L\.? ?600-1-2|qualité pour agir|recevabilité|irrecevab",
 "Affichage/délais de recours (R.600-)":r"R\.? ?600-2|R\.? ?600-1|affichage|notification|délai de recours|tardi",
 "Régularisation (L.600-5, 5-1, sursis)":r"L\.? ?600-5|600-5-1|sursis à statuer|régularis",
 "Droit des tiers/propriété/servitude":r"servitude|droit de propriété|titre|autorisation du propriétaire|propriétaire du terrain|L\.? ?424-",
 "Bruit/ventilation":r"\bbruit|nuisance",
 "Hauteur/volumétrie":r"hauteur|mètres de haut|volumétrie",
 "Sécurité/hélicoptère/aérodrome":r"aérodrome|aéronef|hélicoptère|aviation|incendie|SDIS",
 "Mutualisation/alternative de site":r"mutualis|autre site|autre emplacement|partage de site|pylône existant|co-?localis",
 "Couverture/besoin":r"couverture|zone blanche|new deal|besoin|défaut de couverture|intérêt général|qualité de service",
 "Pouvoirs du maire (police)":r"pouvoirs de police|police générale|police spéciale|L\.? ?2212-2|L\.? ?2212",
 "Compétence/signature":r"incompétence|compétence|délégation de signature",
 "Motivation/procédure":r"motivation|motivé|contradictoire",
}

OPRE=r"(?:Free|Orange|SFR|Bouygues|Cellnex|Hivory|TDF|Phoenix|Totem|ATC|Towercast|On Tower|FPS|Infracos|Axione|Altitude|Itas|IPT|Telecom|Télécom|Mobile|Réseau|Reseau|Tower|Infrastructures)"
def plaintiff(t):
    i=re.search(r"\bdemand(?:e|ent)\b|\bconclu",t)
    head=t[:i.start()] if i else t[:600]
    head=head[-700:]
    if re.search(OPRE,head,re.I) and re.search(r"soci[ée]t[ée]|\bSAS\b|\bSA\b|\bSARL\b|SASU|SCI",head): return "opérateur/société pylônes"
    if re.search(r"[Aa]ssociation|[Cc]ollectif|syndicat des copropriétaires|[Ff]édération",head): return "association/collectif"
    if re.search(r"[Ll]a commune de|[Ll]a communauté|[Ll]e département",head): return "collectivité"
    if re.search(r"\bM\.|\bMme\b|[Cc]onsorts|\bMM\.",head): return "particuliers/riverains"
    return "indéterminé"
def acte(t):
    m=re.search(r"(?:annuler|annulation|suspension|suspendre)[^;]{0,500}",t[:5000],re.I)
    h=m.group(0) if m else t[:2500]
    if re.search(r"retir[ée]|retrait",h[:400],re.I) and re.search(r"non[- ]opposition|déclaration préalable",h,re.I): return "retrait de non-opposition"
    if re.search(r"certificat de (?:non[- ]opposition|décision)",h[:400],re.I): return "certificat de non-opposition"
    if re.search(r"ne s'est pas opposé|non[- ]opposition|décision tacite de non|tacite de non",h,re.I): return "non-opposition à DP"
    if re.search(r"(?:s'est opposé|fait opposition|opposition à (?:la|sa) déclaration|arrêté d'opposition|opposé)",h,re.I): return "opposition à DP"
    if re.search(r"permis de construire",h,re.I): return "permis de construire"
    if re.search(r"raccordement|réseau électrique",h,re.I): return "raccordement"
    if re.search(r"déclaration préalable",h,re.I): return "DP (sens ?)"
    return "autre"
def instance(t,j):
    h=t[:2500]
    return "référé" if re.search(r"juge des référés|L\.? ?521-1|L\.? ?521-2",h) else "fond"
def dispositif(t):
    i=t.rfind("DÉCIDE"); 
    if i<0: i=t.rfind("ORDONNE")
    return t[i:i+900] if i>=0 else t[-700:]
def commune_zone(t):
    m=re.search(r"(?:maire|commune|préfet)[^.]{0,30}(?:de|d'|du)\s+((?:[A-ZÉÈ][\w'’-]+)(?:[- ](?:[A-ZÉÈ][\w'’-]+|de|du|la|le|les|sur|en|sous|d'))*)",t[:3000])
    z=re.findall(r"zone\s+((?:U[A-Za-z]*|AU[a-z]*|A[a-z]*|N[a-z]*|1AU|2AU))\b",t)
    dist=re.findall(r"(?:à|a)\s+(?:moins de\s+|environ\s+|plus de\s+)?(\d[\d  ]*)\s*(?:mètres|m)\b(?:\s+(?:de|des)\s+(?:la |l'|leur|leurs )?(?:habitations?|maisons?|propriété|domicile|résidence|logements?))?",t)
    h=re.findall(r"(\d+(?:,\d+)?)\s*(?:mètres|m)\s+de\s+haut|hauteur (?:totale |maximale )?(?:de|d'environ)\s+(\d+(?:,\d+)?)\s*(?:mètres|m)\b",t)
    return (m.group(1) if m else ""),sorted(set(z))[:4],dist[:4],[a or b for a,b in h][:3]
OUT=[]
for f in glob.glob(S+"/data/raw/*/*.xml"):
    b=open(f,encoding="utf-8",errors="replace").read()
    t=tag(b,"Texte_Integral"); t=re.sub(r"</p>\s*","\n",t); t=re.sub(r"<[^>]+>","",t); t=html.unescape(t)
    if not RELAIS.search(t) or not URBA.search(t): continue
    n=len(RELAIS.findall(t))
    d={"file":os.path.relpath(f,S+"/data/raw"),"juridiction":tag(b,"Nom_Juridiction"),"num":tag(b,"Numero_Dossier"),
       "date":tag(b,"Date_Lecture"),"avocat_req":tag(b,"Avocat_Requerant"),"recours":tag(b,"Type_Recours"),
       "solution":tag(b,"Solution"),"publi":tag(b,"Code_Publication"),"nrelais":n,"plaignant":plaintiff(t),"acte":acte(t),"stade":instance(t,tag(b,"Nom_Juridiction")),"commune_zone":commune_zone(t),"dispositif":dispositif(t),"len":len(t),
       "ops":[k for k,v in OPS.items() if re.search(v,t)],
       "grounds":[k for k,v in GROUNDS.items() if re.search(v,t,re.I)]}
    OUT.append(d)
json.dump(OUT,open(S+"/data/index.json","w"),ensure_ascii=False)
print(len(OUT))
