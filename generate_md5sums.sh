#!/bin/sh

DIR=$1

if [ -z "$DIR" ]; then
    echo "$0: Syntax: $0 <directory>"
fi

md5sum $DIR/* | sort > md5sums.txt
