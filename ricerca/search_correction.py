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
#from whoosh.analysis import StandardAnalyzer, RegexAnalyzer, StopFilter, RegexTokenizer

 
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
def pref_diff_suff(a,b,pre):
    i = pre-1
    while a[:i+1]==b[:i+1] and i<=len(a)-1:
        i += 1
    #j = 0
    #while a[i:i+j+1]!=b[i:i+j+1] and i+j<len(b):
    #    j += 1
    k = 0
    while a[-k-1:]==b[-k-1:] and len(b)-k>i:
        k+=1
    return i+1,k#,-j

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
def res(results, query = "1", n = 10, tag = "tag",resfile=None,v=False):#risultati in formato trec eval
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
def search(fst,quer,stype="b",dsc=False,flds="1",lim=100,fdbk="",w="bm",k=3,lo="o",maxrft=100,opt=[],resdir="",tag="",maxlsat=100,lsat=False,m="2"):
    ix = fst.open_index()
    if not tag:
        tag = stype+"_DESC"+str(dsc)[0]+"_"+str(flds)+"C_GRP"+lo.upper()+"_"+w.upper()+"_"+str(lim)+("RES_FDBK"+fdbk.upper() if fdbk else "")+("_LSAT"+str(maxlsat)+"M"+m if lsat else "")+tag

    # ----------------------------------------------------------------------------------------------- #
    if stype=="i":                                                                              # interactive search
        q = raw_input("Enter a query (hit enter to end): ")
    elif stype=="b":                                                                            # batch search
        #--- apertura del file delle query ---#
        infile = open(quer,'r')
        #--- lettura del file
        text = infile.read()
        #--- dom delle query
        dom = parseString(text)
        #--- estrazione dei dati della query
        #title = gettagdata(dom,'title')
        #if dsc==True:
        title = gettagdata(dom,'desc')
        #for x in range(len(title)-1):          #togliere i commenti e commentare la riga prcedente per usare entrambi
        #    title[x]=title[x]+" "+desc[x]
        num   = gettagdata(dom,'num')
        infile.close()

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
    if resdir and os.path.exists(resdir):
        resfile = open(resdir+"/"+tag+".treceval",'w')
    else:
        print resdir,"does not exist"
        resdir=None

    if stype=="i":                                                                              # ricerca interattiva
        while q <> "":                                                                          # finche' non mando a capo
            query = parser(campi,ix.schema, group=lgroup).parse(q)
            print query
            #f = [x[1] for x  in query.all_terms(phrases=True) if x[0]=="title" and ix.searcher().idf("title",x[1])+ix.searcher().idf("abstract",x[1])>15]
            #query = parser(campi,ix.schema, group=lgroup).parse(" ".join(f))
            results = ix.searcher(weighting=score).search(query,limit=lim)                      # risultati
            if results:
                if not resdir:
                    res(results,tag,lim,tag)                                                 # stampa i risultati
                else:
                    print "sta stampando i risultati su file"
                    #lsa(results,ix,campi,lgroup,score,m,tag,lim,maxlsat,tag,resfile,title[int(tag)-1])
                    res(results,tag,lim,tag,resfile)
            else:
                print "non ha trovato risultati"
            q = raw_input("Enter a query (hit enter to end): ")

    elif stype=="b":                                                                            # ricerca batch

        for qid in num[:]:                                                                        # per ogni query
            title[int(qid)-1].encode('utf-8')
            query = parser(campi,ix.schema, group=lgroup).parse(title[int(qid)-1])
            new_query = parser(campi,ix.schema, group=lgroup).parse(expq_cor(ix,query))
            results = ix.searcher(weighting=score).search(new_query,limit=lim)                      # risultati
            if results:
                if not resdir:
                    res(results,qid,lim,tag)                                                 # stampa i risultati
                else:
                    print "sta stampando i risultati della query "+qid+" su file"
                    res(results,qid,lim,tag,resfile)
            else:
                print "non ha trovato risultati"
        resfile.close()
    ix.searcher().close()

# -------------------------------------------------------------------------------------------------- #
if not os.path.exists(sys.argv[1]):                                                             # controlla se l'indice non c'e'
    print sys.argv[1],"does not exist"                                                          # esci se non esiste
else:                                                                                           # altrimenti procedi
    fst = FileStorage(sys.argv[1])                                                              # cartella indice
    quer = sys.argv[2]                                                                          # file delle query
    stype = sys.argv[3]                                                                         # tipo di ricerca (interattiva, batch)
    tag = sys.argv[4]
    search(fst,quer,stype=stype,dsc=True,flds="2",lim = 1000, w="bm", resdir="/home/alex/information_retrieval/auto/res",tag=tag)
