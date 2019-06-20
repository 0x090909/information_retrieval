#!/bin/bash
trec="/home/alex/uni/3a2s/DataBase_2/lab/trec_eval.8.1/trec_eval"
qrel="./qrels.ohsu.batch.87.txt"

for file in ./res/*.treceval
do
    name=${file%.*}
    name=${name##*/}
   	eval "$trec -q $qrel $file > ./trecs/$name.txt"
done

