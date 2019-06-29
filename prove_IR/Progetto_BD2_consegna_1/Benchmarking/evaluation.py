#serve python almeno versione 3.5 e scipy versione almeno 1.3 per il test di wilcoxon con possibilita' di scegliere l'ipotesi alternativa
from scipy.stats import wilcoxon

res = open("./maps.txt",'r')  # Apro il file maps.txt che contiene una lista di map corrispondenti ai risultati ottenuti
# Creo un dizionario contenente come chiavi i nomi dei file dei risultati e come valori i map corrispondenti 
maps = dict()
for row in res:
    try:    
        val = float(row)
        maps[current].append(val)
    except ValueError:    
        current = row.rstrip()
        maps[current] = []
        
c2 = sorted([x for x in maps.keys() if x[-2:]=="2C"])  # In questo (mini) progetto siamo solo interessati a confrontare risultati da ricerche con 2 campi
# Confronta i map delle varie ricerche con 2 campi 
for i in range(len(c2)):
    for j in range(i+1, len(c2)):
        print(c2[i]+" contro "+c2[j])
        test = wilcoxon(maps[c2[i]][:-1],maps[c2[j]][:-1])#,alternative = "less")  # Non si considera nel test l'ultimo map che e' quello complessivo
        print(test)
