#!/bin/bash
# This script converts a fishbase mdb data file into 
# a mysql database and exports this database for
# further processing and cleaning elsewhere if needed

# Dependencies:
# note that this bash script relies on a .mysql-pass file (chmod 400) w the db password
# sudo apt-get install mdbtools pv
# you also need a mysql server for the import 
# src: http://nialldonegan.me/2007/03/10/converting-microsoft-access-mdb-into-csv-or-mysql-in-linux/

t=$(mdb-tables FishBaseLit.mdb)
echo "Exporting mdb tables $t"
for i in $t; do
  mdb-export -I mysql FishBaseLit.mdb $i \
  > $i.sql
done
mdb-schema FishBaseLit.mdb mysql \
| sed "s/Int8/int/" \
| sed "s/Char /varchar/" \
| sed "s/text /varchar/" \
| grep -v "^COMMENT ON" \
| sed "s/^-/#/" > schema.sql

echo "Creating mysql db and importing schema and data"
pass=$(cat .mysql-pass)
mysql -u root -p$pass -e "drop database if exists fb; create database fb;"
mysql -u root -p$pass -D fb < schema.sql
rm schema.sql

t=$(ls *.sql)
for i in $t; do
  echo "Importing $i"
  pv -petli 1 $i | mysql -u root -p$pass -D fb
done

echo "Exporting mysql db into dumpfile"
mysqldump -u root -p$pass fb > fb-sampledata.sql