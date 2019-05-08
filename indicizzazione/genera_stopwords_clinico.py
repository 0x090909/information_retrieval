import json

#apri file di stopWords_clinico.json
stopWords_clinico = open("stopWords_clinico.json","r+w")
stoplist = json.load(stopWords_clinico)

stoplist_to_add = open("clinical-stopwords.txt")
stop_to_add = []
for word in stoplist_to_add:
    stop_to_add.append(word.replace("\r\n",""))

outList = stoplist + stop_to_add

stopWords_clinico.write(json.dumps(outList))
stopWords_clinico.close()
stoplist_to_add.close()
