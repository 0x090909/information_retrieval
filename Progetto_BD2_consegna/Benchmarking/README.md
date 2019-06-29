## Benchmarking
In questa sottocartella sono presenti i programmi per effettuare l'indicizzazione della collezione. Per far funzionare i comandi presentati di seguito è necessario posizionarsi in questa cartella:
```bash
	cd Benchmarking/
```
Prima di poter eseguire i programmi per ottenere le misure di valutazione dei risultati è necessario decomprimere la cartella di trec_eval e compilare i file che ne hanno bisogno, per questo prima si eseguono i comandi

```bash
	gunzip trec_eval.8.1.tar.gz
	tar xf trec_eval.8.1.tar
	cd trec_eval.8.1
	make
	cd ..
```
Adesso, utilizzando il programma ```trec.sh``` si ottiene l'output di trec_eval per tutti i file dei risultati contenutti nella cartella ```/res```.
```bash
	./trec.sh
```
Da questi si ricavano quindi i map utilizzando ```get_maps.sh```  che li salva nel file ```maps.txt```
```bash
	./get_maps.sh
```
Questo programma mostra anche nell'output della console i map complessivi per ogni run.

Infine per effettuare i test di Wilcoxon sulle coppie di risultati si usa il programma ```evaluation.py``` con:
```bash
	python evaluation.py
```
Da notare che questi test hanno ipotesi alternativa bilaterale, inqueanto la funzione utilizzata, contenuta nelmodulo scipy, non supporta alternativa unilaterale.
Per avere quindi l'ipotesi alternativa unilaterale è necessario utilizzare una versione di python successiva alla 3.5 e rimuovere dei commenti dal programma.
