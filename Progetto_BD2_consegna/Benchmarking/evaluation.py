#serve python almeno versione 3.5 per il test di wilcoxon con possibilita' di scegliere l'ipotesi alternativa

from scipy.stats import wilcoxon

res = open("./maps.txt",'r')
maps = dict()
for row in res:
    try:    
        val = float(row)
        maps[current].append(val)
    except ValueError:    
        current = row.rstrip()
        maps[current] = []
c2 = sorted([x for x in maps.keys() if x[-2:]=="2C"])
#test = wilcoxon(maps["BASELINE_2C"][:-1],maps["STOP3_2C"][:-1],alternative = "less")# alternativa, secondo "modello" meglio del primo
for i in range(len(c2)):
    for j in range(i+1, len(c2)):
        print(c2[i]+" contro "+c2[j])
        test = wilcoxon(maps[c2[i]][:-1],maps[c2[j]][:-1])#,alternative = "less")
        print(test)
