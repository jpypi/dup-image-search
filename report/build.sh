#!/bin/sh

mkdir -p covers

cp *.png covers

cd covers
pdflatex ../covers.tex

