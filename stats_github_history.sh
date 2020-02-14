#!/bin/sh

cd /Users/saito/data/

THISMONTH="`date -v-0d +%Y-%m`"
LASTMONTH="`date -v-31d +%Y-%m`"
THIS="`date -v-0d +%Y%m`"
LAST="`date -v-31d +%Y%m`"

git ls-files |
while read file ; do
  commits=`git log --oneline -- $file |
  grep -e "$THISMONTH" | wc -l`;
  echo "$commits - $file";
done | sort -r -n |
awk '!/README/ {print}' |
awk '!/.gitignore/ {print}' |
awk '!/ 0 - / {print}' |
awk '!/ 1 - / {print}' |
awk '!/.log/ {print}' |
awk '!(/stats_commit/ && /.png/) {print}' |
awk '!(/stats/ && /.sh/) {print}' > mygithub_stats/stats_commit_"$THIS".log

git ls-files |
while read file ; do
  commits=`git log --oneline -- $file |
  grep -e "$LASTMONTH" | wc -l`;
  echo "$commits - $file";
done | sort -r -n |
awk '!/README/ {print}' |
awk '!/.gitignore/ {print}' |
awk '!/ 0 - / {print}' |
awk '!/ 1 - / {print}' |
awk '!/.log/ {print}' |
awk '!(/stats_commit/ && /.png/) {print}' |
awk '!(/stats/ && /.sh/) {print}' > mygithub_stats/stats_commit_"$LAST".log

