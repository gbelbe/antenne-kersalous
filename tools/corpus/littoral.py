"""Écrit antenne-littoral.ttl : taxonomie SKOS des communes du Finistère au regard de la loi Littoral.
Source : corpus/communes_littorales_29.csv (liste DDTM 29, article R.321-1 du code de l'environnement, mise à jour 2019-06-19 ;
noms de communes de l'API geo.api.gouv.fr). Usage : python3 -I tools/corpus/littoral.py <dépôt>"""
import sys,csv
repo=sys.argv[1]
def q(s): return '"'+s.replace("\\","\\\\").replace('"','\\"')+'"@fr'
rows=list(csv.DictReader(open(f"{repo}/corpus/communes_littorales_29.csv",encoding="utf-8")))
out=["""@prefix ant:  <https://kersalous.bzh/ontology/antenne#> .
@prefix dos:  <https://kersalous.bzh/dossier/> .
@prefix skt:  <https://kersalous.bzh/taxonomie/> .
@prefix src:  <https://kersalous.bzh/provenance/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix note: <https://example.org/ontology/kai-internal-knowledge#> .

# ═══════════════════════════════════════════════════════════════
#  COMMUNES DU FINISTÈRE ET LOI LITTORAL
#  Fichier GÉNÉRÉ par tools/corpus/littoral.py depuis corpus/communes_littorales_29.csv : ne pas modifier à la main.
#  La loi Littoral (L.121-1 et suivants du code de l'urbanisme) ne s'applique qu'aux communes littorales ou estuariennes
#  au sens de l'article L.321-2 du code de l'environnement. Liste DDTM 29 du 19 juin 2019, téléchargée le 2026-10-15.
# ═══════════════════════════════════════════════════════════════
skt:LoiLittoral a skos:ConceptScheme ;
    rdfs:label "Communes du Finistère et loi Littoral"@fr ;
    skos:prefLabel "Communes du Finistère et loi Littoral"@fr ;
    skos:definition "Statut de chaque commune du Finistère au regard de la loi Littoral, d'après la liste officielle des communes littorales et estuariennes (article R.321-1 du code de l'environnement)."@fr ;
    skos:notation "K" ;
    skos:hasTopConcept skt:ll-littorale, skt:ll-estuarienne, skt:ll-non-littorale ;
    prov:wasDerivedFrom src:ddtm29-communes-littorales .
"""]
nl=[r for r in rows if r["statut"]=="littorale"]; ne=[r for r in rows if r["statut"]=="estuarienne"]
def top(cid,label,defi,notation,kids):
    s=f"skt:{cid} a skos:Concept ;\n    rdfs:label {q(label)} ;\n    skos:prefLabel {q(label)} ;\n    skos:definition {q(defi)} ;\n    skos:notation \"{notation}\" ;\n    skos:inScheme skt:LoiLittoral ;\n    skos:topConceptOf skt:LoiLittoral"
    if kids: s+=" ;\n    skos:narrower "+", ".join(f"skt:ll-{k}" for k in kids)
    return s+" .\n"
out.append(top("ll-littorale","Commune littorale (soumise à la loi Littoral)","Commune riveraine de la mer ou de l'océan : la loi Littoral s'applique en entier (continuité de l'urbanisation, espaces proches du rivage, coupures d'urbanisation).","K1",[r["insee"] for r in nl]))
out.append(top("ll-estuarienne","Commune estuarienne (soumise à la loi Littoral)","Commune riveraine d'un estuaire en aval de la limite de salure des eaux, classée par décret (2004-311) : la loi Littoral s'applique.","K2",[r["insee"] for r in ne]))
out.append(top("ll-non-littorale","Commune non soumise à la loi Littoral","Commune absente de la liste officielle, même proche de la côte. Seules les communes du Finistère de la liste sont décrites ici ; aucune autre commune n'est listée sauf Plonéour-Lanvern, commune du dossier.","K3",["29174"]))
for i,r in enumerate(rows,1):
    parent="ll-littorale" if r["statut"]=="littorale" else "ll-estuarienne"
    out.append(f"skt:ll-{r['insee']} a skos:Concept ;\n    rdfs:label {q(r['nom'])} ;\n    skos:prefLabel {q(r['nom'])} ;\n    skos:notation \"{r['insee']}\" ;\n    skos:inScheme skt:LoiLittoral ;\n    skos:broader skt:{parent} ;\n    prov:wasDerivedFrom src:ddtm29-communes-littorales .\n")
out.append("""skt:ll-29174 a skos:Concept ;
    rdfs:label "Plonéour-Lanvern"@fr ;
    skos:prefLabel "Plonéour-Lanvern"@fr ;
    skos:notation "29174" ;
    skos:inScheme skt:LoiLittoral ;
    skos:broader skt:ll-non-littorale ;
    prov:wasDerivedFrom src:ddtm29-communes-littorales ;
    note:note "Commune du projet. Absente de la liste officielle (vérifié le 2026-10-15) : la loi Littoral ne s'applique pas à Kersalous, malgré la proximité de la côte. Ne pas confondre avec Plounéour-Brignogan-plages (29021), commune littorale du nord du Finistère." .

dos:commune-ploneour ant:statutLoiLittoral skt:ll-non-littorale ; ant:communeLittorale skt:ll-29174 .
""")
open(f"{repo}/antenne-littoral.ttl","w",encoding="utf-8").write("\n".join(out))
print(len(rows),"communes")
