#!/bin/sh

for item in $(ls *.rst *.tex); do
	2pdf -t -z -m $item;
done

2pdf -t -m stochproc.tex --toc-depth=4
