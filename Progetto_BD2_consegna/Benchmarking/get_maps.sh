#!/bin/bash
# Legge i file in trecs contenenti i risultati di trec_eval
# Crea un nuovo file "maps.txt" che conterra' tutti i map
#
for file in ./trecs/*.txt
do
    name=${file%.*}
    name=${name##*/}
    echo $name >> ./maps.txt
   	eval "cat $file | grep ^map | cut -f3 >> ./maps.txt"
   	echo $name
   	map=$(cat  $file | grep ^map | cut -f3 | tail -1)
   	echo "MAP complessivo: $map"
done
