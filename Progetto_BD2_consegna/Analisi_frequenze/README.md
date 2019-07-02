## Analisi della frequenza delle parole nei documenti rilevanti
In questa sottocartella sono presenti i programmi utilizzati allo scopo di ricavare delle possibili stopword dalle query sperimentali. 
Per far funzionare i comandi presentati di seguito è necessario posizionarsi in questa cartella:
```bash
	cd Analisi_frequenze
```
Il programma ```frq_terms_rel_docs.py``` dà varie opzioni.
Utilizzando l'opzione iq viene richiesto di inserire dei numeri interi da 1 a 63, questi corrispondono ciascuno ad una query sperimentale. 
Inserite le query che interessano il programma permette di vedere quante volte i termini delle query appaiono nei corrsipondenti documenti rilevanti, suddividendo i conteggi nei tre campi title, abstract e trems.
Per esempio:
```bash
    python frq_terms_rel_docs.py ../indice_stop2/ query.ohsu.1-63.xml qrels.ohsu.batch.87.txt iq
    Comma-separated query (tra 1 e 63 compresi, press enter to end): 1,5,12

    Query numero 1
            given        estrogen     progesterone   adverse      therapy      effects      replacement   lipids       
    87157536   0;  0;  0    0;  0;  0    0;  0;  0      0;  1;  0    0;  4;  0    0;  1;  0    0;  1;  0     0;  1;  0     tot. 8
    87157537   0;  0;  0    0;  0;  0    0;  0;  0      0;  0;  0    1;  2;  0    1;  0;  0    1;  0;  0     1;  1;  1     tot. 8
    87202778   0;  0;  0    1;  6;  0    0;  0;  0      0;  0;  0    0;  2;  1    0;  0;  0    0;  1;  0     0;  0;  0     tot. 11
    87097544   0;  1;  0    0;  4;  0    1;  3;  1      0;  0;  0    0;  2;  1    1;  0;  0    0;  0;  0     0;  2;  0     tot. 16
    87316316   0;  0;  0    0;  2;  0    0;  1;  0      0;  0;  0    0;  2;  0    0;  1;  0    0;  2;  0     0;  0;  1     tot. 9
    87316326   0;  0;  0    0;  2;  0    0;  0;  0      0;  1;  0    0;  1;  0    1;  3;  0    0;  0;  0     0;  0;  0     tot. 8

    Query numero 5
            estrogen     cancer       therapy      breast       cause        replacement   
    87086987   1;  1;  0    1;  5;  0    1;  1;  0    1;  4;  1    0;  0;  0    1;  1;  0      tot. 18
    87097092   0;  5;  0    1;  2;  0    0;  0;  0    0;  2;  1    0;  0;  0    0;  0;  0      tot. 11
    87170056   0;  *;  0    1;  *;  0    0;  *;  0    1;  *;  1    0;  *;  0    0;  *;  0      tot. 3
    87299569   0;  0;  0    1;  6;  0    1;  3;  0    0;  2;  1    0;  0;  0    1;  1;  0      tot. 16
    87114242   0;  0;  0    0;  0;  0    0;  2;  0    0;  0;  1    0;  0;  0    1;  0;  0      tot. 4
    87316321   0;  3;  0    1;  2;  0    0;  1;  0    0;  2;  1    0;  0;  0    0;  2;  0      tot. 12

    Query numero 12
            concurrently   hypokalemia   isolated     syndromes    hypoaldosteronism   occur        
    87212268   0;  0;  0      0;  0;  0     0;  1;  0    0;  0;  0    0;  2;  0           0;  0;  0     tot. 3
    87085858   0;  0;  0      1;  2;  1     0;  0;  0    0;  0;  0    0;  0;  0           0;  0;  0     tot. 4
    87169943   0;  0;  0      0;  1;  0     0;  0;  0    0;  0;  0    0;  1;  0           0;  0;  0     tot. 2
    87210263   0;  0;  0      0;  0;  0     0;  0;  0    0;  0;  0    1;  1;  0           0;  0;  0     tot. 2
    87249110   0;  0;  0      0;  0;  0     0;  0;  0    0;  0;  0    1;  1;  0           0;  0;  0     tot. 2
    87228899   0;  *;  0      0;  *;  0     0;  *;  0    0;  *;  0    1;  *;  0           0;  *;  0     tot. 1
```

L'opzione 'tnn' riassume i risultati di 'iq', per tutte le query stampa i totali di colonna delle "matrici" ottenibili con 'iq'.
Omette eventuali query per cui i documenti rilevanti non contengono nessuna parola della query.
Per esempio:
```bash
    python frq_terms_rel_docs.py ../indice_stop2/ query.ohsu.1-63.xml qrels.ohsu.batch.87.txt tnn
            given        estrogen     progesterone   adverse      therapy      effects      replacement   lipids       
    query 1    0;  1;  0    1;  14; 0    1;  4;  1      0;  2;  0    1;  13; 2    3;  5;  0    1;  4;  0     1;  4;  2       tot. 60 parole su 6 documenti rilevanti

            pathophysiology   intravascular   coagulation   disseminated   treatment    
    query 2    0;  1;  0         6;  20; 9       5;  25; 12    6;  18; 9      0;  7;  0       tot. 118 parole su 11 documenti rilevanti

            lupus        anticoagulants   anticardiolipin   pathophysiology   epidemiology   complications   
    query 3    17; 56; 12   4;  5;  1        7;  26; 0         0;  0;  0         0;  0;  0      0;  1;  3          tot. 132 parole su 23 documenti rilevanti

            treating     etidronate   effectiveness   hypercalcemia   malignancy   
    query 4    0;  1;  0    7;  27; 8    0;  0;  0       10; 36; 13      8;  12; 0       tot. 122 parole su 13 documenti rilevanti

            estrogen     cancer       therapy      breast       cause        replacement   
    query 5    1;  9;  0    5;  15; 0    2;  7;  0    2;  10; 6    0;  0;  0    3;  4;  0        tot. 64 parole su 6 documenti rilevanti

            cell         autoimmune   lymphoma     associated   symptoms     
    query 6    7;  20; 1    0;  1;  0    6;  19; 5    3;  6;  0    0;  0;  0       tot. 68 parole su 6 documenti rilevanti

            deficiency   lactase      therapy      options      
    query 7    0;  1;  0    3;  11; 0    1;  1;  0    0;  0;  0       tot. 17 parole su 7 documenti rilevanti

            etiology     pancytopenia   workup       aids         
    query 8    1;  0;  0    2;  1;  3      0;  0;  0    2;  7;  2       tot. 18 parole su 8 documenti rilevanti

            isoimmunization   rh           review       topics       
    query 9    1;  5;  10        5;  5;  13   0;  0;  0    0;  0;  0       tot. 39 parole su 10 documenti rilevanti

            duration     antimicrobial   therapy      endocarditis   
    query 10   0;  0;  0    0;  4;  0       1;  8;  2    5;  9;  7         tot. 36 parole su 7 documenti rilevanti

            chemotherapy   cancer       metastatic   breast       advanced     
    query 11   9;  44; 0      14; 29; 0    7;  14; 0    16; 34; 19   5;  4;  0       tot. 195 parole su 18 documenti rilevanti

            concurrently   hypokalemia   isolated     syndromes    hypoaldosteronism   occur        
    query 12   0;  0;  0      1;  3;  1     0;  1;  0    0;  0;  0    3;  5;  0           0;  0;  0       tot. 14 parole su 6 documenti rilevanti

        .                                                       .                                                   .
        .                                                       .                                                   .
        .                                                       .                                                   .
    ```

Infine, l'opzione 'fqt' permette di sapere in quali query sono presenti le parole inserite.
Utilizzando l'ulteriore opzione -d(dettagli) esegue le funzioni di iq e tnn sulle query trovate
Per esempio:
```bash
    python frq_terms_rel_docs.py ../indice_stop2/ query.ohsu.1-63.xml qrels.ohsu.batch.87.txt fqt
    
    python frq_terms_rel_docs.py /home/alex/prove_IR/indice_stop3_rev2 query.ohsu.1-63.xml qrels.ohsu.batch.87.txt fqt
    Comma-separated terms (press enter to end): estrogen,therapy

    La parola 'estrogen' si trova nelle query:  1, 5, 61

    La parola 'therapy' si trova nelle query:  1, 5, 7, 10, 22, 51, 61
```

```bash
	python frq_terms_rel_docs.py ../indice_stop2/ query.ohsu.1-63.xml qrels.ohsu.batch.87.txt fqt -d
    Comma-separated terms (press enter to end): estrogen

    La parola 'estrogen' si trova nelle query:  1, 5, 61

    Query numero 1
            given        estrogen     progesterone   adverse      therapy      effects      replacement   lipids       
    87157536   0;  0;  0    0;  0;  0    0;  0;  0      0;  1;  0    0;  4;  0    0;  1;  0    0;  1;  0     0;  1;  0     tot. 8
    87157537   0;  0;  0    0;  0;  0    0;  0;  0      0;  0;  0    1;  2;  0    1;  0;  0    1;  0;  0     1;  1;  1     tot. 8
    87202778   0;  0;  0    1;  6;  0    0;  0;  0      0;  0;  0    0;  2;  1    0;  0;  0    0;  1;  0     0;  0;  0     tot. 11
    87097544   0;  1;  0    0;  4;  0    1;  3;  1      0;  0;  0    0;  2;  1    1;  0;  0    0;  0;  0     0;  2;  0     tot. 16
    87316316   0;  0;  0    0;  2;  0    0;  1;  0      0;  0;  0    0;  2;  0    0;  1;  0    0;  2;  0     0;  0;  1     tot. 9
    87316326   0;  0;  0    0;  2;  0    0;  0;  0      0;  1;  0    0;  1;  0    1;  3;  0    0;  0;  0     0;  0;  0     tot. 8

            given        estrogen     progesterone   adverse      therapy      effects      replacement   lipids       
    query 1    0;  1;  0    1;  14; 0    1;  4;  1      0;  2;  0    1;  13; 2    3;  5;  0    1;  4;  0     1;  4;  2       tot. 60 parole su 6 documenti rilevanti



    Query numero 5
            estrogen     cancer       therapy      breast       cause        replacement   
    87086987   1;  1;  0    1;  5;  0    1;  1;  0    1;  4;  1    0;  0;  0    1;  1;  0      tot. 18
    87097092   0;  5;  0    1;  2;  0    0;  0;  0    0;  2;  1    0;  0;  0    0;  0;  0      tot. 11
    87170056   0;  *;  0    1;  *;  0    0;  *;  0    1;  *;  1    0;  *;  0    0;  *;  0      tot. 3
    87299569   0;  0;  0    1;  6;  0    1;  3;  0    0;  2;  1    0;  0;  0    1;  1;  0      tot. 16
    87114242   0;  0;  0    0;  0;  0    0;  2;  0    0;  0;  1    0;  0;  0    1;  0;  0      tot. 4
    87316321   0;  3;  0    1;  2;  0    0;  1;  0    0;  2;  1    0;  0;  0    0;  2;  0      tot. 12

            estrogen     cancer       therapy      breast       cause        replacement   
    query 5    1;  9;  0    5;  15; 0    2;  7;  0    2;  10; 6    0;  0;  0    3;  4;  0        tot. 64 parole su 6 documenti rilevanti



    Query numero 61
            estrogen     bleeding     differential   progesterone   breakthrough   therapy      diagnosis    vaginal      
    87097517   1;  3;  0    0;  0;  0    0;  0;  0      0;  0;  0      0;  0;  0      1;  0;  0    0;  0;  0    0;  0;  0     tot. 5
    87181409   0;  0;  0    0;  0;  0    0;  0;  0      0;  0;  0      0;  0;  0      0;  0;  0    0;  0;  0    0;  0;  0    
    87322900   0;  0;  0    1;  2;  0    0;  0;  0      0;  0;  0      0;  0;  0      0;  0;  0    0;  1;  0    0;  0;  0     tot. 4
    87114244   0;  0;  0    0;  1;  0    0;  1;  0      0;  0;  0      0;  0;  0      0;  0;  0    0;  1;  1    0;  0;  0     tot. 4
    87316320   0;  0;  0    1;  1;  0    0;  0;  0      0;  1;  0      0;  0;  0      0;  2;  0    1;  0;  0    0;  0;  0     tot. 6
    87316326   0;  2;  0    0;  2;  0    0;  0;  0      0;  0;  0      0;  0;  0      0;  1;  0    0;  0;  0    0;  0;  0     tot. 5

            estrogen     bleeding     differential   progesterone   breakthrough   therapy      diagnosis    vaginal      
    query 61   1;  5;  0    2;  6;  0    0;  1;  0      0;  1;  0      0;  0;  0      1;  3;  0    1;  2;  1    0;  0;  0       tot. 24 parole su 6 documenti rilevanti

```

### Nota:
I comandi visti sopra prevedono che esista una cartella ```indice_stop2``` contenente un indice della collezione.
