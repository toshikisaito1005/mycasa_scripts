# README for mycasa_scripts

![stats_commit_today](https://github.com/toshikisaito1005/mycasa_scripts/blob/master/mygithub_stats/stats_commit_today.png)
![stats_commit_yesterday](https://github.com/toshikisaito1005/mycasa_scripts/blob/master/mygithub_stats/stats_commit_yesterday.png)
![stats_commit_lastweek](https://github.com/toshikisaito1005/mycasa_scripts/blob/master/mygithub_stats/stats_commit_lastweek.png)
![stats_commit_202005](https://github.com/toshikisaito1005/mycasa_scripts/blob/master/mygithub_stats/stats_commit_202005.png)
![stats_commit_202004](https://github.com/toshikisaito1005/mycasa_scripts/blob/master/mygithub_stats/stats_commit_202004.png)

sync_github.sh
```
#!/bin/bash
set -e
content_dir=/<path_to_sync_github.sh>/

set -x
cd "$content_dir"
git rm -rf --cached .
git init

git add "mycasa_scripts_active"
git add "mycasa_scripts_done"
git add "myradex_scripts"
git add .gitignore
git add README.md
git add stats_github*.sh
git add mygithub_stats

git commit -m "Commit at $(date "+%Y-%m-%d %T")" || true
git push -f origin master:master
```

crontab -e
```
*/5 * * * * /bin/sh /<path_to_sync_github.sh>/sync_github.sh >> /<path_to_sync_github.sh>/sync_github.log 2>&1
59 */2 * * * /bin/rm -rf /<path_to_sync_github.sh>/sync_github.log
* */6 * * * /bin/sh /<path_to_sync_github.sh>/stats_github.sh
*/30 * * * * /bin/sh /<path_to_sync_github.sh>/stats_github_today.sh
```

backup
1. institute cloud
2. WD My Pssport 2TB HDD (Time Machine)
3. TOSHIBA 1TB HDD (some important data)
4. I-O DATA 500 GB HDD (some important data mirror)
