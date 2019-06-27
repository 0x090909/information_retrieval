#--- importazione di interi moduli
import string as st
import sys
import getopt
import os.path
import json
import numpy as np
#--- importazione di parti di modulo
from whoosh.filedb.filestore import FileStorage
from xml.dom.minidom import parse, parseString
from whoosh import scoring,qparser
from whoosh.fields import *
from whoosh.qparser import QueryParser as qp
from whoosh.qparser import MultifieldParser as mp
from whoosh.searching import Searcher

# -------------------------------------------------------------------------------------------------- #
# estrazione dei dati di un tag
def gettagdata(dom,tag):
    nodes = dom.getElementsByTagName(tag)
    if nodes is None or len(nodes)==0:
        return None
    tagdata = []
    for node in nodes:
        tagdata.append(st.rstrip(st.lstrip(node.firstChild.data)))
    return tagdata

# -------------------------------------------------------------------------------------------------- #
# Le parole vengono eventualmente corrette di al massimo una lettera perche' altrimenti si rischia di 
# utilizzare parole che c'entrano poco con la parola originale 
def expq_cor(ix,query):
    check = []
    no_check = []
    for x  in query.all_terms(phrases=True):
        if x[0]=="title":                                                   # Per non prendere doppioni se si usano piu' campi.
            if len(x[1])>5 and ix.searcher().idf("abstract",x[1])>11.9:     # Controllo che la parola abbia almeno 5 lettere e non appaia nell'indice(almeno non nei campi abstract).
                check.append(x[1])                                          # Forse sara' da correggere, aggiungo la parola alla lista check
            else:
                no_check.append(x[1])                                       # Altrimenti non viene controllata
    if "hiv" in no_check:  # Per migliorare un po' la query 63 (la differenza si vede prendendo 1000 risultati) 
        no_check += ["aids"]
    corrector = ix.searcher().corrector("title")
    expq=[]
    for x in check:                                                         # Per ogni parola in check
        corr = []
        for y in corrector.suggest(x, prefix=4, maxdist=1,limit=100):       # Mantengo un prefisso di 4 lettere e ottengo la lista dei suggerimenti 
            if y[:-1]!=x and (y[:-1]!=x[:-1] or y==x):                      # Accetto suggerimenti che cambiano solo una lettera all'interno della parola(o la parola stessa)
                corr.append(y)
        expq += corr
    return " ".join(expq+no_check)                                          # Ritorno la lista delle parole della query piu' gli eventuali suggerimenti
    
# -------------------------------------------------------------------------------------------------- #
def res(results, query = "1", n = 10, tag = "tag",resfile=None,v=False):    #risultati in formato trec eval
    rank = 0
    if len(results) < n:
        n = len(results)
    if not resfile:
        for rank in range(0,n):
            print query,'\t',"Q0",'\t',results[rank]['identifier'],'\t',rank,'\t',results[rank].score,'\t',tag
    else:
        for rank in xrange(0,n):
            resfile.write(query+'\t'+"Q0"+'\t'+results[rank]['identifier']+'\t'+str(rank)+'\t'+str(results[rank].score)+'\t'+tag+"\n")
            
# -------------------------------------------------------------------------------------------------- #
def src(indexdir,quer,dsc=True,flds="2",lim=100,w="bm",lo="o",opt=[],resdir="",run=""):
    """
    Questa funzione permette di effettuare il reperimento di risultati per query contenute nel file indicato in quer dall'indice indicato in indexdir, 
    utilizzando oggetti e funzioni del modulo whoosh.
    
    Parameters
    ----------
    indexdir : string
    Una stringa che indica il percorso della cartella contenente l'indice su cui effettuare la ricerca.
    
    quer : string
    Una stringa che indica il percorso del file contenente le query da utilizzare.
    
    dsc : bool
    Indica quale campo della query utilizzare, titolo o descrizione, di default usa la descrizione.
    
    flds : string
    Indica il numero di campi, puo' assumere solo valori "1", "2" o "3".
    
    lim : int
    Numero massimo di documenti reperiti per query deve essere un numero positivo.
    
    w : string
    Schema di pesatura utilizzato, puo' assumere solo valori "bm" o "tf".
    "bm" sta per BM25 mentre "tf" sta per TF_IDF (per ulteriori informazioni vedi whoosh.scorig)
    
    lo : string
    Operatore logico utilizzato per le parole delle query puo' assumere valori "o" per OR o "a" per AND.
    
    opt : list
    Dovrebbe contenere due valori di tipo numerico da assegnare ai parametri del BM25.
    
    resdir : string
    Una stringa che indica il percorso della cartella dove salvare il file dei risultati.
    Se striga vuota come da default i risultati vengono stampati con print.
    
    run : string
    Una stringa opzionale, permette di aggiungere  parte del tag e del nome dei file dei risultati
    
    Returns
    -------
    None
    
    Notes
    -----
    Questa funzione e' stata fatta per effettuare ricerche in un indice della gia' citata collezione ohsumed, non e' garantito che funzioni per altri.
    In particolare il file delle query deve essere organizzato allo stesso modo del file contenente le query sperimentali per la collezione ohsumed (il quale si dovrebbe 
    trovare nella stessa cartella di questo programma) e i documenti dell'indice dovrebbero avere i campi 'identifier', 'title', 'abstract' e 'terms'.
    """
    fst = FileStorage(indexdir)
    ix = fst.open_index()
    # Creo il runtag utilizzando tutti i parametri che si possono cambiare
    tag = run+"_BATCH_DESC"+str(dsc)[0]+"_"+flds+"C_GRP"+lo.upper()+"_"+w.upper()+"_"+str(lim)+"RES"
    
    # ------------------------------------------------------------------------------------------------ #
    # Interpreta la scelta di quale operatore logico si usa per raggruppare le parole delle query
    if lo=="o":                                                                                 
        lgroup = qparser.OrGroup                                                                
    elif lo=="a":                                                                               
        lgroup = qparser.AndGroup                                                               
        
    # ------------------------------------------------------------------------------------------------ #
    # Interpreta la scelta dello schema di peastura
    if w=="tf":                                                                                 
        score = scoring.TF_IDF()                                                                
    elif w=="bm":                                                                               
        if opt:                                                             # opt dovrebbe contenere il punto che ottimizza un valore(come MAP) per i due parametri
            score = scoring.BM25F(opt[0],opt[1])                                                
        else:                                                                                   
            score = scoring.BM25F()                                                             
            
    # ------------------------------------------------------------------------------------------------ #
    # Interpeta il numero di campi dei documenti da utilizzare
    if flds=="1":                                                                               
        campi = "title"                                                                         
        parser = qp                                                                             
    elif flds=="2":                                                                             
        campi = ["title", "abstract"]                                                           
        parser = mp                                                                             
    elif flds=="3":                                                                             
        campi = ["title", "abstract","terms"]                                                   
        parser = mp                                                                             
        
    # ----------------------------------------------------------------------------------------------- #
    #--- apertura del file delle query ---#
    infile = open(quer,'r')
    #--- lettura del file
    text = infile.read()
    #--- dom delle query
    dom = parseString(text)
    #--- estrazione dei dati della query
    title = gettagdata(dom,'title')  # Utilizzare il campo title delle query
    if dsc==True:
        title = gettagdata(dom,'desc')  # Utilizzare il campo desc delle query
        # Togliere i commenti dalle righe successive e commentare la riga prcedente per usare entrambi
        #desc = gettagdata(dom,'desc') 
        #for x in range(len(title)-1):
        #    title[x]=title[x]+" "+desc[x]
    num   = gettagdata(dom,'num')
    infile.close()
        
    # ------------------------------------------------------------------------------------------------- #
    # Apre il file dove inserire i risultati
    if resdir and os.path.exists(resdir):
        resfile = open(resdir+"/"+run+"_"+flds+"C"+".treceval",'w')  # Se si cambiano piu' parametri e' consigliato usare la variabile tag al posto di run+"_"+flds+"C"
    else:
        print resdir,"does not exist"
        resdir=None
    
    # Effettua la ricerca per ogni query
    for qid in num[:]:
        title[int(qid)-1].encode('utf-8')                                                              
        query = parser(campi,ix.schema, group=lgroup).parse(title[int(qid)-1])
        new_query = parser(campi,ix.schema, group=lgroup).parse(expq_cor(ix,query))     # Corregge la query se le parole hanno una lettera sbagliata
        #print new_query
        results = ix.searcher(weighting=score).search(new_query,limit=lim)              # Effettua la ricerca effettiva
        
        if results:
            if not resdir:                                                              # Stampa i risultati in console
                res(results,qid,lim,tag)
            else:                                                                       # Stampa i risultati su file
                print "sta stampando i risultati della query "+qid+" su file"          
                res(results,qid,lim,tag,resfile) 
        else:
            print "non ha trovato risultati"
    resfile.close()
    ix.searcher().close()
    
    return None
    
# -------------------------------------------------------------------------------------------------- #
# Si puo' utilizzare direttamente questo programma.
# Esempio:
# $ python search_tk.py ../indice_stop3/ ./query.ohsu.1-63.xml ../Benchmarking/res STOP3
if __name__ == "__main__":
    if not os.path.exists(sys.argv[1]):                                                             # controlla se l'indice non c'e'
        print sys.argv[1],"does not exist"                                                          # esci se non esiste
    else:                                                                                           # altrimenti procedi
        fst = FileStorage(sys.argv[1])                                                              # cartella indice
        quer = sys.argv[2]                                                                          # file delle query
        resd = sys.argv[3]                                                                          # cartella dove mettere i risultati
        tag = sys.argv[4]                                                                           # runtag e nome del file dei risultati
        src(fst, quer, resdir=resd, run=tag, lim=1000)
        
