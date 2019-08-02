#!/bin/bash

gatk CollectReadCounts -I $2 -L chrY -O output.tsv -imr OVERLAPPING_ONLY -format TSV

COUNT=$(
python3 << END

with open("output.tsv", "r") as count_file:
    count = 0
    for line in count_file:
        if line.startswith("chrY"):
            line_array = line.split("\t")
            count = int(line_array[3])
            print(count)
END
)
echo $COUNT
echo $COUNT > "output.txt"

if [ $COUNT -lt 40000 ]; then
    GENDER="Female"
elif [ $COUNT -gt 80000 ]; then
    GENDER="Male"
else
    GENDER="Unknown"
fi
echo $GENDER
echo $GENDER >> "output.txt"

if [ $GENDER = $1 ]; then
    echo "Gender matches Sample sheet"
else
    echo "Gender does not match Samplesheet"
    exit 1
fi