#!/bin/bash
fold_file="$1"
xml_file="$2"
while read line1
do
    line1=$(echo $line1 | sed -n "s/\r//"p)
    echo "process $line1"
    grep -n "$line1" $xml_file
    grep -n "$line1" $xml_file | awk -F ':' '{print $1}' > line_file
#    sleep 2s
    if [ -s "line_file" ]
    then
        while read line2
        do
            #sed -n "${line2}s/clone-depth=\"1\"//g"p "$xml_file"
            sed -i "${line2}s/clone-depth=\"1\"//g" "$xml_file"
        done < line_file
    fi
     
done < $fold_file
rm line_file
