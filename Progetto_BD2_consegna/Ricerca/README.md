## Ricerca
In questa sottocartella sono presenti i programmi utilizzati per la ricerca di documenti rilevanti.Per far funzionare i comandi presentati di seguito è necessario posizionarsi in questa cartella:
```bash
	cd Ricerca/
```

Il programma ```batch_searches.py``` permette di effettuare automaticamente tutte le ricerche fatte negli esperimenti, cambiando quindi indici e numero di campi.
A tal fine si  utilizza il comando:
```bash
	python batch_searches.py
```

Se si vuole effettuare una ricerca singola si può invece sfruttare il programma ```search_tk.py``` che permette con alcune modifice di cambiare anche altri parametri oltre all'indice ed al numero di  campi.
Un esempio di comando per effettuare la ricerca singola è il seguente:

```bash
	python search_tk.py ../indice_stop3/ ./query.ohsu.1-63.xml ../Benchmarking/res STOP3
```
