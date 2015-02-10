#!/bin/bash

# mongodb data
sed -i 's/dinanrm@gmail.com/email@dina-web.net/g' collection.json
tar cvfz mongodb-data.tgz *.json

# userdb data
sed -i 's/dinanrm@gmail.com/email@dina-web.net/g' userdb.sql
sed -i -r -e "s/'.{43}='/'#######'/g" userdb.sql
# TODO reference the .bitnami-pass file below to reuse the global pw
replace "#######" "$(printf "passw0rd12" | openssl dgst -sha256 -binary | openssl enc -a)" -- userdb.sql
tar cvfz userdb.sql.tgz userdb.sql