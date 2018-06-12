#!/bin/bash
CMD='curl -k -X POST -H "X-FOTA-USERID: PMD_WD" -H "X-FOTA-TOKEN:a42110d41ae77b618b03b776f19bce25" -H "X-FOTA-VERSION:14.01.1706.06-user_CN_X00K-14.01.1706.07-user-CN_X00K-1485" --form "modeltype=phone" --form "carrier=CTCC-ASUS_X00KD-CN_X00K" --form "model=CN_X00K" --form "edition=formal" --form "extra_storage=350" --form "priority=force_P1" --form "activatetime=30" --form "desc=" --form "uploadfile=CN_X00K-14.01.1706.06-20170607_CN_X00K-14.01.1706.07-20170613.zip" https://dmcontrol.asus.com/DM-server/UploadFile'

function cp_rename_dir(){
    be_send_fota="$1"
    dirname=$(echo "$be_send_fota"  | awk -F "-|_" '{print $3"-user-"$1"_"$2"-"$7"-user-"$5"_"$6}')
    rm -rf "$dirname"
    mkdir "$dirname"
    cp "$be_send_fota" "$dirname/" && echo "cp successful"
}


function fix_cmd(){
    dir=`pwd`
    dir="$dir"/"$dirname"/"$be_send_fota"
    dir=`echo ${dir//\//\\\/}`
    count="$1"
    CMD=$(echo "$CMD" | sed -n "s/carrier=CTCC-ASUS_X00KD-CN_X00K/carrier=$carrier/p")
    CMD=$(echo "$CMD" | sed -n "s/model=CN_X00K/model=$model/g"p)
    CMD=$(echo "$CMD" | sed -n "s/X-FOTA-VERSION:14.01.1706.06-user_CN_X00K-14.01.1706.07-user-CN_X00K-1485/X-FOTA-VERSION:$dirname-$RANDOM_INT/g"p)
    CMD=$(echo "$CMD" | sed -n "s/CN_X00K-14.01.1706.06-20170607_CN_X00K-14.01.1706.07-20170613.zip/\@$dir/g"p)
    CMD=$(echo "$CMD" | sed -n "s/extra_storage=350/extra_storage=$extra_storage/g"p)
    CMD=$(echo "$CMD" | sed -n "s/priority=force_P1/priority=$priority/g"p)
    echo '#!/bin/bash' > ss.sh
    chmod u+x ss.sh
    echo "$CMD" | tee -a ss.sh
    source ss.sh
}

function main(){
    carrier="$1"
    model="$2"
    fota="$3"
    priority="$4"
    extra_storage="$5"
    RANDOM_INT="$6"
    cp_rename_dir "$fota"
    fix_cmd "$RANDOM_INT"
}

main $@
