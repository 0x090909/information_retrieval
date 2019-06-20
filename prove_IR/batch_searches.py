#--- importazione di interi moduli
import getopt
import os.path
#--- importazione di parti di modulo
from whoosh.filedb.filestore import FileStorage
from search_tk import src

ixs = {"BASELINE":"./indice_baseline","STOP1":"./indice_stop1","STOP2":"./indice_stop2","STOP3":"./indice_stop3"}
fields = ["1","2","3"]
quer = "./query.ohsu.1-63.xml"#sys.argv[2]                                                  # file delle query
tag = ""
for ix in ixs:
    tag = ix
    if not os.path.exists(ixs[ix]):                                                             # controlla se l'indice non c'e'
        print ixs[ix],"does not exist"                                                          # esci se non esiste
    else:                                                                                       # altrimenti procedi
        fst = FileStorage(ixs[ix])                                                              # cartella indice
        for flds in fields:
            src(fst,quer=quer,dsc=True,flds=flds,lim = 1000, resdir="./res",run=tag)
        
#provo a rimettere therapy?
