```bash
	cd Indicizzazione/
	python indicizzatore_batch_baseline.py ../indice_baseline ./ohsumed.87.xml
	python indicizzatore_batch_stopwords.py ../indice_stop1 ./ohsumed.87.xml ./stopWords_generali.txt 
	python indicizzatore_batch_stopwords.py ../indice_stop2 ./ohsumed.87.xml ./stopWords_clinico.json
	python indicizzatore_batch_stopwords.py ../indice_stop3 ./ohsumed.87.xml ./stopWords_generali.txt 

```
