import sys,os,re,zipfile,urllib.request,concurrent.futures as cf
S=sys.argv[1]; OUT=S+"/data/raw"
BASE="https://opendata.justice-administrative.fr"
# antenne-relais : "antenne" avec relais/radioélectrique/téléphonie/télécommunication/station de base/pylône
PAT=re.compile(r"antennes?[ -]relais|station[s]? radio-?électrique|station[s]? de base|pylône|opérateur de téléphonie|téléphonie mobile|installation radioélectrique|radiotéléphon",re.I)
PAT2=re.compile(r"antenne|pylône|radioélectr|téléphonie|télécommunic",re.I)
def job(item):
    d,f=item; m=re.match(r"(\w+?)_(\d{4})(\d{2})\.zip",f); y,mo=m.group(2),m.group(3)
    code=d[1:]; dest=f"{OUT}/{code}"; os.makedirs(dest,exist_ok=True)
    mark=f"{dest}/.done_{y}{mo}"
    if os.path.exists(mark): return item,0
    tmp=f"{S}/data/{f}"
    import subprocess
    for t in range(60):
        r=subprocess.run(["curl","-sfL","-C","-","--max-time","120","-o",tmp,f"{BASE}/{d}/{y}/{mo}/{f}"])
        if r.returncode==0: break
        if r.returncode==33: os.remove(tmp)
    else: return item,-1
    n=0
    with zipfile.ZipFile(tmp) as z:
        for nm in z.namelist():
            if not nm.lower().endswith(".xml"): continue
            b=z.read(nm).decode("utf-8","replace")
            if PAT.search(b) and re.search(r"déclaration préalable|permis de construire|urbanisme",b,re.I):
                open(f"{dest}/{os.path.basename(nm)}","w").write(b); n+=1
    os.remove(tmp); open(mark,"w").write(str(n)); return item,n
items=[]
for d,l in (("DCA","DCA.lst"),("DTA","DTA.lst"),("DCE","DCE.lst")):
    for f in open(S+"/od/"+l).read().split(): items.append((d,f))
# CE: only 2021+ ; all
with cf.ThreadPoolExecutor(10) as ex:
    for (d,f),n in ex.map(job,items): print(d,f,n,flush=True)
