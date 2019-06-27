## Analisi della frequenza delle parole nei documenti rilevanti
In questa sottocartella sono presenti i programmi utilizzati allo scopo di ricavare delle possibili stopword dalle query sperimentali. Per far funzionare i comandi presentati di seguito è necessario posizionarsi in questa cartella:
```bash
	cd Analisi_frequenze
```


```bash
	python frq_terms_rel_docs.py ../indice_stop2/ query.ohsu.1-63.xml qrels.ohsu.batch.87.txt iq
	python frq_terms_rel_docs.py ../indice_stop2/ query.ohsu.1-63.xml qrels.ohsu.batch.87.txt tnn
	python frq_terms_rel_docs.py ../indice_stop2/ query.ohsu.1-63.xml qrels.ohsu.batch.87.txt fqt
	python frq_terms_rel_docs.py ../indice_stop2/ query.ohsu.1-63.xml qrels.ohsu.batch.87.txt fqt -d

```
