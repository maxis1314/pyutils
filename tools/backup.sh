#!/bin/bash


tar cvfz backup.tar.gz /a /b --exclude=/a/b/* --exclude=/b/a/*

echo "backup" | mutt -s `date '+backup%Y-%m-%d'` -a backup.tar.gz XXXX@gmail.com

today=`date +%Y%m%d`;
mysqldump  --databases $1 -uroot -pXXXX > ${today}_$1.sql

size=`stat -c %s ${today}_$1.sql | tr -d '\n'`

