#!/bin/bash
new_branch="new_branch_name"
base_branch="master"
repoc forall -c 'echo -n "$REPO_PROJECT ";git log --pretty=oneline | head -1|cut -d" " -f1' > git_path_and_commit_id.txt
readarray -t message_array < git_path_and_commit_id.txt
rm git_path_and_commit_id.txt
for line in "${message_array[@]}"
do
	project=$(echo $line | cut -d" " -f1)
	commit_id=$(echo $line | cut -d" " -f2)
	ssh -p 29418 10.0.30.9 gerrit create-branch "$project" "$new_branch_name" "$base_branch"
	echo $project $commit_id
	unset project commit_id
done
echo "testcde"
