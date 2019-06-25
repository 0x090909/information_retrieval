#--- importazione di interi moduli
import string as st
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
        no_check += ["aids"]
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
def src(fst,quer,dsc=True,flds="2",lim=100,w="bm",lo="o",opt=[],resdir="",run=""):
    ix = fst.open_index()
    tag = run+"_BATCH_DESC"+str(dsc)[0]+"_"+flds+"C_GRP"+lo.upper()+"_"+w.upper()+"_"+str(lim)+"RES"
    
    # ------------------------------------------------------------------------------------------------ #    
    if lo=="o":                                                                                 
        lgroup = qparser.OrGroup                                                                
    elif lo=="a":                                                                               
        lgroup = qparser.AndGroup                                                               
        
    # ------------------------------------------------------------------------------------------------ #
    if w=="tf":                                                                                 
        score = scoring.TF_IDF()                                                                
    elif w=="bm":                                                                               
        if opt:                                     # opt, se c'e', dovrebbe contenere il punto con MAP massimo per i due parametri
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
        
    # ----------------------------------------------------------------------------------------------- #
    #--- apertura del file delle query ---#
    infile = open(quer,'r')
    #--- lettura del file
    text = infile.read()
    #--- dom delle query
    dom = parseString(text)
    #--- estrazione dei dati della query
    title = gettagdata(dom,'title')
    if dsc==True:
        title = gettagdata(dom,'desc')
        #desc = gettagdata(dom,'desc') #togliere i commenti e commentare la riga prcedente per usare entrambi
        #for x in range(len(title)-1):
        #    title[x]=title[x]+" "+desc[x]
    num   = gettagdata(dom,'num')
    infile.close()
        
    # ------------------------------------------------------------------------------------------------- #
    if resdir and os.path.exists(resdir):
        resfile = open(resdir+"/"+run+"_"+flds+"C"+".treceval",'w')
    else:
        print resdir,"does not exist"
        resdir=None
        
    for qid in num[:]:                                                                          # per ogni query
        title[int(qid)-1].encode('utf-8')                                                              
        query = parser(campi,ix.schema, group=lgroup).parse(title[int(qid)-1])
        new_query = parser(campi,ix.schema, group=lgroup).parse(expq_cor(ix,query))             #query corretta se una lettera sbagliata
        #print new_query
        results = ix.searcher(weighting=score).search(new_query,limit=lim)                      # risultati   
        
        if results:
            if not resdir:
                res(results,qid,lim,tag)                                                        # stampa i risultati
            else:
                print "sta stampando i risultati della query "+qid+" su file"
                res(results,qid,lim,tag,resfile) 
        else:
            print "non ha trovato risultati"
    resfile.close()
    ix.searcher().close()
    
# -------------------------------------------------------------------------------------------------- #
if __name__ == "__main__":
    if not os.path.exists(sys.argv[1]):                                                             # controlla se l'indice non c'e'
        print sys.argv[1],"does not exist"                                                          # esci se non esiste
    else:                                                                                           # altrimenti procedi
        fst = FileStorage(sys.argv[1])                                                              # cartella indice
        quer = sys.argv[2]                                                                          # file delle query
        resd = sys.argv[3]
        tag = sys.argv[4]
        src(fst, quer, resdir=resd, run=tag, lim=1000)
        
