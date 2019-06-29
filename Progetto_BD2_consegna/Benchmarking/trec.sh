#/* Copyright (C) Alessandro Stefani, Cristi Gutu
# * Unauthorized copying of this file, via any medium is strictly prohibited
# * Proprietary and confidential
# * Written by Cristi Gutu <gheorghecristi.gutu@studenti.unipd.it>, June 2019
# * Written by Alessandro Stefani <alessandro.stefani.6@studenti.unipd.it>, June 2019
# */
 
#!/bin/bash
trec="./trec_eval.8.1/trec_eval"
qrel="./qrels.ohsu.batch.87.txt"

for file in ./res/*.treceval
do
    name=${file%.*}
    name=${name##*/}
   	eval "$trec -q $qrel $file > ./trecs/$name.txt"
done

