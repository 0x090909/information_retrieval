#!/bin/bash
for file in ./trecs/*.txt
do
    echo "file: $file"
   	#eval "$trec -q $qrel $file | grep ^map | cut -f3"
done

