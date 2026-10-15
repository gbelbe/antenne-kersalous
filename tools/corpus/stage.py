"""Copie les XML de l'open data retenus dans corpus/decisions/ et écrit corpus/manifest.csv.
Usage : python3 -I tools/corpus/stage.py <dossier data/raw> <dépôt>"""
import csv,sys,os,re,shutil,hashlib
raw,repo=sys.argv[1:3]
BASE="https://opendata.justice-administrative.fr"
LEVEL={"TA":("TA","DTA"),"CA":("CAA","DCA"),"CE":("CE","DCE")}
rows=[]
for x in csv.DictReader(open(f"{repo}/corpus/index_decisions.csv",encoding="utf-8")):
    sub,name=x["fichier_opendata"].split("/")
    lvl,d=LEVEL[sub]
    m=re.search(r"_(\d{4})(\d{2})(\d{2})\.xml$",name); y,mo=m.group(1),m.group(2)
    dest=f"corpus/decisions/{lvl}/{y}/{name}"
    os.makedirs(os.path.dirname(f"{repo}/{dest}"),exist_ok=True)
    shutil.copyfile(f"{raw}/{x['fichier_opendata']}",f"{repo}/{dest}")
    h=hashlib.sha256(open(f"{repo}/{dest}","rb").read()).hexdigest()
    rows.append(dict(fichier=dest,sha256=h,niveau=lvl,juridiction=x["juridiction"],numero=x["num"],date_lecture=x["date"],
        archive_url=f"{BASE}/{d}/{y}/{mo}/{lvl}_{y}{mo}.zip",membre_archive=name,date_collecte="2026-10-15",licence="Licence Ouverte 2.0"))
w=csv.DictWriter(open(f"{repo}/corpus/manifest.csv","w",newline="",encoding="utf-8"),fieldnames=list(rows[0]))
w.writeheader(); w.writerows(rows); print(len(rows))
