#! /bin/bash
#create projects

ProjectName=codeaurora/manifest
xmlName=default
BranchName=master
Servicer=10.0.30.9

for i in $(cat project.list)
do
    echo $i
    ssh -p 29418 $Servicer gerrit create-project -n codeaurora/$i --empty-commit -b $BranchName -t FAST_FORWARD_ONLY -p All-Projects
done
