#!/bin/sh

cd /Users/saito/data/

DAY1="`date -v-1d +%Y-%m-%d`"
DAY2="`date -v-2d +%Y-%m-%d`"
DAY3="`date -v-3d +%Y-%m-%d`"
DAY4="`date -v-4d +%Y-%m-%d`"
DAY5="`date -v-5d +%Y-%m-%d`"
DAY6="`date -v-6d +%Y-%m-%d`"
DAY7="`date -v-7d +%Y-%m-%d`"

git ls-files |
while read file ; do
  commits=`git log --oneline -- $file |
  grep -e "$DAY1" | wc -l`;
  echo "$commits - $file";
done |
sort -r -n |
awk '!/README/ {print}' |
awk '!/.gitignore/ {print}' |
awk '!/ 0 - / {print}' |
awk '!/ 1 - / {print}' |
awk '!/.log/ {print}' |
awk '!(/stats_commit/ && /.png/) {print}' |
awk '!(/stats/ && /.sh/) {print}' > mygithub_stats/stats_commit_yesterday.log

git ls-files |
while read file ; do
  commits=`git log --oneline -- $file |
  grep -e "$DAY1" -e "$DAY2" -e "$DAY3" -e "$DAY4" -e "$DAY5" -e "$DAY6" -e "$DAY7" | wc -l`;
  echo "$commits - $file";
done | sort -r -n |
awk '!/README/ {print}' |
awk '!/.gitignore/ {print}' |
awk '!/ 0 - / {print}' |
awk '!/ 1 - / {print}' |
awk '!/.log/ {print}' |
awk '!(/stats_commit/ && /.png/) {print}' |
awk '!(/stats/ && /.sh/) {print}' > mygithub_stats/stats_commit_lastweek.log
