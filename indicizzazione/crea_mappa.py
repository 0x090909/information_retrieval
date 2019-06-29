from xml.dom.minidom import parse, parseString
import pickle
#questo crea una mappa tra riga e docid
#cosi quando voglio ottenere un documento
#apro il file xml e faccio fseek
#fo.seek(0, 0)
def gettagdata(dom,tag):
	nodes = dom.getElementsByTagName(tag)
	if nodes is None or len(nodes)==0:
		return None
	node = nodes[0]
	if node is None:
		return None
	return node.firstChild.data.strip()

docs = open("ohsumed.87.xml","r") #abbiamo un documento per linea
mappa = {}
i = 0
for doc in docs:
    #--- document object model ---#
    dom = parseString(doc)
    this_I = gettagdata(dom,'I')

    this_U = gettagdata(dom,'U')
    mappa[int(this_I)] = this_U

file_mappa = open('mappa.pkl', 'wb')
pickle.dump(mappa, file_mappa)
file_mappa.close()
