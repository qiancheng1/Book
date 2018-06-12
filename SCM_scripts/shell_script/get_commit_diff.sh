#!/bin/bash
ROOT=$(pwd)
grep -aoe path.* "$1" | sort > file1
grep -aoe path.* "$2" | sort > file2
line1=$(wc -l file1 | awk '{print $1}')
line2=$(wc -l file2 | awk '{print $1}')
if [ "$line1"  -ne "$line2" ]
then
    echo "error,文件行数不相等"
fi
readarray -t file1_array < file1
readarray -t file2_array < file2
rm file1 file2 log_update
for i in `seq 0 ${#file1_array[@]}`
do
    if [[ "${file1_array[$i]}" != "" && "${file2_array[$i]}" != "" ]]
    then
        path1=$(echo "${file1_array[$i]}" | grep -aoe "path=[.A-Z_a-z0-9\"/-]*" | awk -F '"|"' '{print $2}')
        path2=$(echo "${file2_array[$i]}" | grep -aoe "path=[.A-Z_a-z0-9\"/-]*" | awk -F '"|"' '{print $2}')
        revision1=$(echo "${file1_array[$i]}" | grep -aoe "revision=[.A-Z_a-z0-9\"/-]*" | awk -F '"|"' '{print $2}')
        revision2=$(echo "${file2_array[$i]}" | grep -aoe "revision=[.A-Z_a-z0-9\"/-]*" | awk -F '"|"' '{print $2}')
        if [ "$path1" != "$path2" ]
        then
            echo "path error"
        fi
        pushd "$path1"
            log_line=$(git log --pretty=oneline "$revision1".."$revision2" | wc -l )
            if [ "$log_line" -ne 0 ]
            then
                echo "######## PATH: $path1" >> "$ROOT"/log_update
                #git log --pretty=oneline "$revision1".."$revision2" >> "$ROOT"/log_update
                git log "$revision1".."$revision2" >> "$ROOT"/log_update
                echo >> "$ROOT"/"log_update"
                echo >> "$ROOT"/"log_update"
                echo >> "$ROOT"/"log_update"
                echo >> "$ROOT"/"log_update"
            fi
        popd
        
    fi
done
