#!/bin/bash
B99="$1"
#cd .. && mkdir "$B99"
#cd -
ls > dir_need_to_copy
while read line
do
	if [ "$line" == "out" ]
	then
		continue
	fi
	cp -a "$line" "../$B99"
        echo "cp -a" "$line" "../${B99}"
done < dir_need_to_copy
rm dir_need_to_copy
cd  ../$B99
	mkdir .repo
cd -

echo "test git pull --unshallow 之后的提交"
