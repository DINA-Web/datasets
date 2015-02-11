#!/bin/bash
wget https://gist.githubusercontent.com/esperlu/943776/raw/dd87f4088f6d5ec7563478f7a28a37ba02cf26e2/mysql2sqlite.sh -O mysql2sqlite.sh
chmod +x mysql2sqlite.sh
pass=$(cat .mysql-pass)
./mysql2sqlite.sh -u root -p$pass fb > fb-sampledata.sqlite