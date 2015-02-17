#!/bin/bash
t=$(sqlite3 fb.sqlite ".tables" | tr -d "\012" | sed -r -e "s/(\\s+)(\\n*)/ /g")

echo "Exporting all sqlite tables as .csv"
for i in $t; do
	echo "Exporting $i.csv"
	sqlite3 -header -csv fb.sqlite "select * from $i;" > $i.csv
done

echo "Done"
