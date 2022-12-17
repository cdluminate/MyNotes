main:clean
	make Mmod.1988
	make clean
clean:
	-rm *.log *.toc *.aux *.out
purge:clean
	-rm *.pdf
b:
	c99 -Wall -O2 -fopenmp b.c -o b
bint:
	c99 -Wall -O2 -fopenmp bint.c -o bint
Mmod.1988:
	pdflatex Mmod.1988.tex
