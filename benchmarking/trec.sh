#!/bin/bash
trec="trec_eval"
qrel="../ricerca/qrels.ohsu.batch.87.txt"
for file in *.treceval
do
   	eval "$trec -q $qrel $file | grep ^map | cut -f3"
	echo "aleste"
done

