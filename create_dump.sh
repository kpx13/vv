#! /bin/bash

DATE=`date +%Y-%m-%d`
python manage.py dumpdata articles blog edu feedback pages review subscribe auth users --natural > dump_"$DATE".json
git add -A
git commit -a -m "dump ""$DATE"
git push
