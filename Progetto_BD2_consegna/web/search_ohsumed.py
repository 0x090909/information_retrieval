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
from whoosh import scoring,qparser,highlight as hl
from whoosh.fields import *
from whoosh.qparser import QueryParser as qp
from whoosh.qparser import MultifieldParser as mp
from whoosh.searching import Searcher
from paginate_whoosh import WhooshPage

# -------------------------------------------------------------------------------------------------- #
# Funzione per ottenere suggerimenti tra le parole della conllezione
def suggerimenti(ix,query):                                                
    qt_correction = dict([(x[1],[]) for x  in query.all_terms(phrases=True) if len(x[1]) > 3])
    corrector = ix.searcher().corrector("abstract")
    for x in qt_correction:
        scores = []
        for y in corrector.suggest(x, prefix=1, maxdist=4, limit=10):
            qt_correction[x].append(y)
    return qt_correction

# -------------------------------------------------------------------------------------------------- #
def src(indexdir,ud,stype="b",flds="2",lim=100,w="bm",lo="o",opt=[]):
    """
    Questa funzione permette di effettuare il reperimento di risultati per query interattive dall'indice indicato in indexdir, 
    utilizzando oggetti e funzioni del modulo whoosh.
    
    Parameters
    ----------
    indexdir : string
    Una stringa che indica il percorso della cartella contenente l'indice su cui effettuare la ricerca.
    
    ud : string
    Una stringa contenente la query del'utente.
    
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
        if opt:                                     # opt dovrebbe contenere il punto che ottimizza un valore(come MAP) per i due parametri
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

    # ------------------------------------------------------------------------------------------------- #
    q = ud.query
    query = parser(campi,ix.schema, group=lgroup).parse(q)
    results = ix.searcher(weighting=score).search(query,limit=None)[:1000]          # Effettua la ricerca effettiva
    
    # Per ottenere la paginazione
    respage = 15
    reslen = len(results)
    page = WhooshPage(results, page=ud.page, items_per_page=respage)
    pages = range(1,max(2,reslen/respage+bool(reslen%respage)+1))
    pg = page.link_map("~2~","search?query="+str(ud.query)+"&page=$page")
    #for p in pg:
    #    print pg[p]
    
    if reslen:                                                                      # Se si hanno dei risultati li restituisce 
        ix.searcher().close()
        return page, reslen, pg
    else:                                                                           # Altrimenti si cerca di suggerire parole simili a quelle cercate 
        qtc = suggerimenti(ix,query)
        ix.searcher().close()
        return qtc, 0, None

def adv_src(fst,ud,stype="b",flds="2",lim=100,w="bm",lo="o",opt=[]):
    """
        Possibilita' di creare una ricerca avanzata permettendo di cambiare altri parametri.
    """
    pass


# -------------------------------------------------------------------------------------------------- #
if __name__ == "__main__":
    if not os.path.exists(sys.argv[1]):                                                             # controlla se l'indice non c'e'
        print sys.argv[1],"does not exist"                                                          # esci se non esiste
    else:                                                                                           # altrimenti procedi
        fst = FileStorage(sys.argv[1])                                                              # cartella indice
        quer = sys.argv[2]                                                                          # file delle query
        stype = sys.argv[3]                                                                         # tipo di ricerca (interattiva, batch)
        tag = sys.argv[4]
        src(fst,quer,stype=stype,dsc=True,flds="2",lim = 1000, w="bm", resdir="/home/alex/information_retrieval/auto/res",tag=tag)
