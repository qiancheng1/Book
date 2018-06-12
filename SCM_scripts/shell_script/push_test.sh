#!/bin/bash
ROOT_PATH=`pwd`
repoc list > name_path.txt
while read line
do
	name=`echo $line | awk -F ' : ' '{print $2}'`
	path=`echo $line | awk -F ' : ' '{print $1}'`
	if [ -d "$path" ]
	then
		pushd $path > /dev/null
			pwd
			git ls-remote git@10.0.30.8:GR6750_66_A_O_ASUS_SW3/${name} 
			if [ "$?" != 0 ]
			then
				echo git@10.0.30.8:GR6750_66_A_O_ASUS_SW3/${name} >> ${ROOT_PATH}/no_name.txt
				echo "ls-remote failed!!!!"
			else
				git push git@10.0.30.8:GR6750_66_A_O_ASUS_SW3/${name} HEAD:PDU3_MTK_BRH
			fi
		popd > /dev/null
	fi
done < name_path.txt
