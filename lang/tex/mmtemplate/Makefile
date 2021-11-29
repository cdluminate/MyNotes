main:clean
	make mmtemplate
	make temp
	make clean
clean:
	-rm *.log *.toc *.aux *.out
purge:clean
	-rm *.pdf
mmtemplate:
	pdflatex mmtemplate.tex
	pdflatex mmtemplate.tex
temp:
	pdflatex temp.tex
