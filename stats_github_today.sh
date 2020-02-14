#!/bin/sh

cd /Users/saito/data/

TODAY="`date -v-0d +%Y-%m-%d`"

git ls-files |
while read file ; do
  commits=`git log --oneline -- $file |
  grep -e "$TODAY" | wc -l`;
  echo "$commits - $file";
done |
sort -r -n |
awk '!/README/ {print}' |
awk '!/.gitignore/ {print}' |
awk '!/ 0 - / {print}' |
awk '!/ 1 - / {print}' |
awk '!/.log/ {print}' |
awk '!(/stats_commit/ && /.png/) {print}' |
awk '!(/stats/ && /.sh/) {print}' > mygithub_stats/stats_commit_today.log
