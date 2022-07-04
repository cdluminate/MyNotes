main: demo.pdf
	pdflatex cvpr
	bibtex cvpr
	pdflatex cvpr
	pdflatex cvpr
	-evince cvpr.pdf

demo.pdf:
	inkscape -o demo.pdf demo.svg
