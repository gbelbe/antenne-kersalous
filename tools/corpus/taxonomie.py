"""Écrit antenne-contentieux.ttl : schémas SKOS du contentieux + termes d'ontologie utilisés par les décisions.
Usage : python3 -I tools/corpus/taxonomie.py <dépôt>   (la spécification est dans taxo_spec.py)"""
import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import taxo_spec as T
repo=sys.argv[1]
def q(s): return '"'+s.replace("\\","\\\\").replace('"','\\"')+'"@fr'
out=["""@prefix ant:  <https://kersalous.bzh/ontology/antenne#> .
@prefix skt:  <https://kersalous.bzh/taxonomie/> .
@prefix dos:  <https://kersalous.bzh/dossier/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix note: <https://example.org/ontology/kai-internal-knowledge#> .

# ═══════════════════════════════════════════════════════════════
#  TAXONOMIE DU CONTENTIEUX DES ANTENNES-RELAIS
#  Fichier GÉNÉRÉ par tools/corpus/taxonomie.py à partir de tools/corpus/taxo_spec.py : ne pas modifier à la main.
#  Onze schémas SKOS à facettes ; une décision (ant:Jurisprudence) est reliée à un ou plusieurs concepts de chacun.
#  Les références d'articles sont de mémoire de l'auteur et à vérifier à la source avant toute citation.
# ═══════════════════════════════════════════════════════════════
"""]
n=0
for name,(label,code,desc) in T.SCHEMES.items():
    items=T.ALL[name]
    tops=[i[0] for i in items if i[1] is None]
    out.append(f"skt:{name} a skos:ConceptScheme ;\n    rdfs:label {q(label)} ;\n    skos:prefLabel {q(label)} ;\n    skos:definition {q(desc)} ;\n    skos:notation \"{code}\" ;\n    skos:hasTopConcept "+", ".join("skt:"+t for t in tops)+" .\n")
    kids={}
    for cid,par,*_ in items: kids.setdefault(par,[]).append(cid)
    num={}
    def walk(par,prefix):
        for k,c in enumerate(kids.get(par,[]),1):
            num[c]=f"{prefix}{k}"; walk(c,num[c]+".")
    walk(None,code)
    for cid,par,lab,defi,rx in items:
        s=f"skt:{cid} a skos:Concept ;\n    rdfs:label {q(lab)} ;\n    skos:prefLabel {q(lab)} ;\n    skos:definition {q(defi)} ;\n    skos:notation \"{num[cid]}\" ;\n    skos:inScheme skt:{name}"
        s+=(" ;\n    skos:broader skt:"+par) if par else (" ;\n    skos:topConceptOf skt:"+name)
        if cid in kids: s+=" ;\n    skos:narrower "+", ".join("skt:"+k for k in kids[cid])
        if cid in T.EXPLICATIONS: s+=" ;\n    skos:scopeNote "+q(T.EXPLICATIONS[cid])
        out.append(s+" .\n"); n+=1
out.append("""# ═══════════════════════════════════════════════════════════════
#  TERMES D'ONTOLOGIE POUR LES DÉCISIONS
# ═══════════════════════════════════════════════════════════════
ant:concordeAvecConcept a owl:ObjectProperty ;
    rdfs:label "correspond au concept du corpus"@fr ;
    rdfs:domain ant:MoyenJuridique ; rdfs:range skos:Concept ;
    note:note "Relie un moyen du dossier aux concepts de la taxonomie du contentieux, pour retrouver les décisions qui évoquent, retiennent ou écartent un moyen comparable." .

ant:aPourConcept a owl:ObjectProperty ;
    rdfs:label "est classée sous le concept"@fr ;
    rdfs:domain ant:Jurisprudence ; rdfs:range skos:Concept ;
    note:note "Propriété mère de toutes les facettes : interroger celle-ci retrouve une décision par n'importe quel axe." .
""")
props=[("moyenEvoque","moyen évoqué","Moyens","Moyen cité ou discuté dans la décision, repéré par expression régulière. Ne dit rien du sort du moyen."),
 ("moyenRetenu","moyen retenu","Moyens","Moyen que le juge a accueilli. Renseigné seulement pour les décisions lues."),
 ("moyenEcarte","moyen écarté","Moyens","Moyen que le juge a écarté (rejeté ou inopérant). Renseigné seulement pour les décisions lues."),
 ("resultat","résultat","Resultat","Dispositif de la décision."),
 ("effetProjet","effet sur le projet","EffetProjet","Conséquence pour le projet d'antenne."),
 ("acteAttaque","acte attaqué","ActeAttaque","Décision administrative en cause."),
 ("voieDeDroit","voie de droit","Procedure","Recours au fond, référé, appel, cassation, avis."),
 ("mecanismeProcedural","mécanisme procédural","Procedure","Outil procédural évoqué : régularisation, urgence présumée, frais, recours abusif."),
 ("typeRequerant","type de requérant","Requerant","Nature du demandeur."),
 ("contexteSite","contexte du site","ContexteSite","Territoire, ouvrage, distance aux habitations."),
 ("niveauJuridiction","niveau de juridiction","Niveau","Premier ressort, appel, cassation."),
 ("proximiteKersalous","proximité avec Kersalous","Proximite","Ressemblance calculée avec le dossier."),
 ("transferabilite","transférabilité à Kersalous","Transferabilite","Le motif décisif s'applique-t-il ici ? Renseigné pour les décisions lues."),
 ("niveauLecture","niveau de lecture","NiveauLecture","Ce qui a été fait sur cette décision."),
 ("statutLoiLittoral","statut de la commune au regard de la loi Littoral","LoiLittoral","Commune littorale, estuarienne ou non littorale. Renseigné pour les décisions des tribunaux de Rennes et Nantes dont la commune est dans le Finistère."),
 ("communeLittorale","commune du Finistère concernée","LoiLittoral","Commune du Finistère citée comme lieu du projet (liste officielle des communes littorales).")]
for p,lab,sch,desc in props:
    out.append(f"ant:{p} a owl:ObjectProperty ;\n    rdfs:label {q(lab)} ;\n    rdfs:subPropertyOf ant:aPourConcept ;\n    rdfs:domain ant:Jurisprudence ;\n    note:note {q(desc+' Concepts du schéma skt:'+sch+'.')} .\n")
out.append("""ant:moyenEcarteDeduit a owl:ObjectProperty ;
    rdfs:label "moyen écarté (déduit du rejet)"@fr ;
    rdfs:subPropertyOf ant:moyenEcarte ;
    rdfs:domain ant:Jurisprudence ;
    note:note "Déduit automatiquement : la décision rejette entièrement la requête et ce moyen est discuté dans les motifs, donc écarté. Aucune lecture humaine ; les moyens évoqués dans les visas seulement ne sont pas inclus." .

ant:scoreProximite a owl:DatatypeProperty, owl:FunctionalProperty ;
    rdfs:label "score de proximité avec Kersalous (0 à 100)"@fr ;
    rdfs:domain ant:Jurisprudence ; rdfs:range xsd:integer .

ant:detailScore a owl:DatatypeProperty ;
    rdfs:label "détail du calcul du score"@fr ;
    rdfs:domain ant:Jurisprudence ; rdfs:range xsd:string ;
    note:note "Liste des critères qui ont fait monter ou baisser le score, pour pouvoir le contester." .

ant:requerantNomme a owl:ObjectProperty ;
    rdfs:label "association ou collectif requérant"@fr ;
    rdfs:domain ant:Jurisprudence ; rdfs:range ant:Association ;
    note:note "Association ou collectif nommé dans le texte de la décision. Les particuliers sont pseudonymisés par la juridiction : ils ne figurent jamais ici." .

ant:Avocat a owl:Class ;
    rdfs:label "Avocat ou cabinet"@fr ;
    rdfs:subClassOf ant:Organisation ;
    note:note "Nom tel qu'il apparaît dans la décision. Ne dit rien de la compétence. Un nom de famille seul peut recouvrir plusieurs avocats homonymes." .

ant:avocatRequerant a owl:ObjectProperty ;
    rdfs:label "avocat du requérant"@fr ;
    rdfs:domain ant:Jurisprudence ; rdfs:range ant:Avocat .

ant:avocatAdverse a owl:ObjectProperty ;
    rdfs:label "avocat de la partie adverse"@fr ;
    rdfs:domain ant:Jurisprudence ; rdfs:range ant:Avocat .

ant:cheminLocal a owl:DatatypeProperty ;
    rdfs:label "chemin du fichier dans le dépôt"@fr ; rdfs:range xsd:string .

ant:empreinteSha256 a owl:DatatypeProperty ;
    rdfs:label "empreinte SHA-256 du fichier"@fr ; rdfs:range xsd:string .

ant:archiveOrigine a owl:DatatypeProperty ;
    rdfs:label "archive mensuelle d'origine"@fr ; rdfs:range xsd:anyURI .

ant:avocatOpenData a owl:DatatypeProperty ;
    rdfs:label "avocat selon la métadonnée de l'open data"@fr ; rdfs:range xsd:string ;
    note:note "Champ Avocat_Requerant de la juridiction, recopié tel quel. Souvent l'avocat de l'opérateur, pas celui des riverains : le côté n'est pas garanti." .
""")
out.append("# ── Moyens du dossier reliés à la taxonomie ──")
for m,cs in T.MOYEN_DOSSIER.items(): out.append(f"{m} ant:concordeAvecConcept "+", ".join("skt:"+c for c in cs)+" .")
open(f"{repo}/antenne-contentieux.ttl","w",encoding="utf-8").write("\n".join(out))
print(n,"concepts")
