main: compile clean
compile:
	pdflatex mathmod.tex
	pdflatex mathmod.tex
clean:
	-rm *.log *.toc *.aux *.out
purge:clean
	-rm *.pdf
v:
	evince mathmod.pdf
