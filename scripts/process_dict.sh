#!/bin/bash
##
# Process a dictionary file(one word per line) and filter out anything that is
# too short or too long
#
# ./scripts/process_dict.shcripts/process_dict.sh /path/to/dict.txt > icenine/contrib/words.txt
##

LOW=3; 
HIGH=7; 

OUT="";

while read line; do 
    ct=${#line}; 
    if [[ $LOW -lt $ct ]] && [[ $ct -lt $HIGH ]]; then 
        echo "$OUT$line"; 
    fi 
done <$1