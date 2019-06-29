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
import pprint, pickle


def getDoc(docid):
    docs = open("../indicizzazione/ohsumed.87.xml","r")
    docs.seek(int(docid))
    doc = docs.readline()
    print(doc)

    dom = parseString(doc)
    #--- estrazione dei dati dal documento ---#
    this_I = gettagdata(dom,'I')
    this_U = gettagdata(dom,'U')
    this_S = gettagdata(dom,'S')
    this_M = gettagdata(dom,'M')
    this_T = gettagdata(dom,'T')
    this_P = gettagdata(dom,'P')
    this_W = gettagdata(dom,'W')
    this_A = gettagdata(dom,'A')
    return (this_I,
    this_U,
    this_S,
    this_M,
    this_T,
    this_P,
    this_W,
    this_A)

# -------------------------------------------------------------------------------------------------- #
def expq_cor(ix,query):
    check = []
    no_check = []
    for x  in query.all_terms(phrases=True):
        if x[0]=="title":
            if len(x[1])>5 and ix.searcher().idf("abstract",x[1])>11.9:
                check.append(x[1])
            else:
                no_check.append(x[1])
    if "hiv" in no_check:
        no_check+=["aids"]
    corrector = ix.searcher().corrector("title")
    expq=[]
    for x in check:
        corr = []
        for y in corrector.suggest(x, prefix=4, maxdist=1,limit=1000):
            if y[:-1]!=x and (y[:-1]!=x[:-1] or y==x):
                corr.append(y)
        expq += corr
    return " ".join(expq+no_check)

# -------------------------------------------------------------------------------------------------- #


def src(fst,ud,stype="b",flds="2",lim=100,w="bm",lo="o",opt=[]):
    ix = fst.open_index()

    # ------------------------------------------------------------------------------------------------ #
    if lo=="o":
        lgroup = qparser.OrGroup
    elif lo=="a":
        lgroup = qparser.AndGroup

    # ------------------------------------------------------------------------------------------------ #
    if w=="tf":
        score = scoring.TF_IDF()
    elif w=="bm":
        if opt:                                     # opt, se c'e', contiene il punto di massimo per i due parametri
            score = scoring.BM25F(opt[0],opt[1])
        else:
            score = scoring.BM25F()

    # ------------------------------------------------------------------------------------------------ #
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
    new_query = parser(campi,ix.schema, group=lgroup).parse(expq_cor(ix,query))             #query corretta se una lettera sbagliata
    results = ix.searcher(weighting=score).search(query,limit=None)[:1000]                      # risultati
    respage = 20
    reslen = len(results)
    page = WhooshPage(results, page=ud.page, items_per_page=respage)
    pages = range(1,max(2,reslen/respage+bool(reslen%respage)+1))
    pg = page.link_map("~3~","search?query="+str(ud.query)+"&page=$page")
    for p in pg:
        print pg[p]
    ix.searcher().close()
    return page, reslen, pg

def adv_src(fst,ud,stype="b",flds="2",lim=100,w="bm",lo="o",opt=[]):
    ix = fst.open_index()

    # ------------------------------------------------------------------------------------------------ #
    if lo=="o":
        lgroup = qparser.OrGroup
    elif lo=="a":
        lgroup = qparser.AndGroup

    # ------------------------------------------------------------------------------------------------ #
    if w=="tf":
        score = scoring.TF_IDF()
    elif w=="bm":
        if opt:                                     # opt, se c'e', contiene il punto di massimo per i due parametri
            score = scoring.BM25F(opt[0],opt[1])
        else:
            score = scoring.BM25F()

    # ------------------------------------------------------------------------------------------------ #
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
    new_query = parser(campi,ix.schema, group=lgroup).parse(expq_cor(ix,query))             #query corretta se una lettera sbagliata
    results = ix.searcher(weighting=score).search(query,limit=None)[:1000]                      # risultati
    respage = 20
    reslen = len(results)
    page = WhooshPage(results, page=ud.page, items_per_page=respage)
    pages = range(1,max(2,reslen/respage+bool(reslen%respage)+1))
    pg = page.link_map("~2~","search?query="+str(ud.query)+"&page=$page")
    print pg
    ix.searcher().close()
    return page, reslen, pages




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
