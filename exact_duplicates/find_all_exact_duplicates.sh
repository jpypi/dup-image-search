#!/bin/sh

BASE_DIR=$1

if [ -z "$BASE_DIR" ]; then
    echo "$0: Syntax: $0 <album covers base directory>"
    exit 0
fi

for i in "a" "b" "c" "d" "e" "f" "g" "h" "i" "j" "k" "l" "m" "n" "o" "p" "q" "r" "s" "t" "the" "u" "v" "w" "x" "y"
do
    echo "Calculating hashes for the '${i}' directory."
    SUB_DIR="${BASE_DIR}/${i}"

    # 17 min 41 sec on "a"
    ls -1 -Q $SUB_DIR | xargs -i{} md5sum $SUB_DIR/{} >> md5sums.txt

    # 18 min 23 sec on "a"
    #find $SUB_DIR -type f -exec md5sum {} \; >> md5sums.txt
done

sort md5sums.txt > md5sums_sorted.txt
echo "Completed hashing."

#python detect_exact_image_duplicates.py md5sums_sorted.txt
