#!/bin/sh

DIR=$1

python files_to_prune.py "$DIR" > prunes.txt
LINES=`wc -l prunes.txt | awk '{print $1}'`
awk '{print $1}' prunes.txt | xargs -i rm {}
echo "Removed $LINES files."
