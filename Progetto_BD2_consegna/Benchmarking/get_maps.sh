#!/bin/bash
for file in ./trecs/*.txt
do
    name=${file%.*}
    name=${name##*/}
    echo $name >> ./maps.txt
   	eval "cat $file | grep ^map | cut -f3 >> ./maps.txt"
done

