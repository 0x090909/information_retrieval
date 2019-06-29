## Indicizzazione
In questa sottocartella sono presenti i programmi per effettuare l'indicizzazione della collezione.
Per far funzionare i comandi presentati di seguito è necessario posizionarsi in questa cartella:
```bash
	cd Indicizzazione/
```

Il programma ```indicizzatore_batch_baseline.py``` permette la crezione dell'indice utilizzato per la baseline tramite il comando:
```bash
	python indicizzatore_batch_baseline.py ../indice_baseline ./ohsumed.87.xml
```

Il programma ```indicizzatore_batch_stopwords.py``` permette invece di creare un indice che prevede l'eliminazione delle stopword.
Per fare gli esperimenti sono stati utilizzati i comandi:
```bash
	python indicizzatore_batch_stopwords.py ../indice_stop1 ./ohsumed.87.xml ./stopWords_generali.txt 
	python indicizzatore_batch_stopwords.py ../indice_stop2 ./ohsumed.87.xml ./stopWords_clinico.json
	python indicizzatore_batch_stopwords.py ../indice_stop3 ./ohsumed.87.xml ./stopWords_clinico_3.json
```
Gli ultimi argomenti dei comandi corrispondono ai file contenenti le stopword  utilizzate di volta in volta.
