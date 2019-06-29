#--- importazione di interi moduli
import getopt
import os.path
import sys
#--- importazione di parti di modulo
from whoosh.filedb.filestore import FileStorage
from search_tk import src

# Questo programma si aspetta di avere in ixs i percorsi degli indici con i nomi che si vogliono dare ai corrispondenti file dei risultati(come chiavi).
# Le uniche cose che cambiano sono gli indici e il numero di campi.
# Si potrbbe espandere cambiando anche altri parametri ma non e' nello scopo di questo (mini) progetto
# (inoltre se si aggiungono altre variazioni e' necessario cambiare il modo in cui vengono assegnati i nomi ai file dei risultati, in search_tk.py, per comprendere tutti i cambiamenti e non sovrascrivere file gia' creati)
#
# Nel ciclo for vengono effettuate le ricerche con le query del file in quer, in tutto sono 12 (4 indici e 3 combinazioni di campi)

ixs = {"BASELINE":"../indice_baseline","STOP1":"../indice_stop1","STOP2":"../indice_stop2","STOP3":"../indice_stop3"}
fields = ["1","2","3"]
quer = "./query.ohsu.1-63.xml"                                                  # file delle query
tag = ""
for ix in ixs:
    tag = ix
    if not os.path.exists(ixs[ix]):                                                                 # controlla se l'indice non c'e'
        print ixs[ix],"does not exist"                                                              # esci se non esiste
    else:                                                                                           # altrimenti procedi
        for flds in fields:
            src(ixs[ix],quer=quer,dsc=True,flds=flds,lim = 100, resdir="../Benchmarking/res",run=tag)   # Richiama la funzione src per effettuare la ricerca
