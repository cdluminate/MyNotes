# Detect the operating system
UNAME_S := $(shell uname -s)

# Set the viewer command based on the OS
ifeq ($(UNAME_S),Darwin)
	# macOS
	VIEWER := open -a preview
	LYX := /Applications/LyX.app/Contents/MacOS/lyx
else
	# Linux
	VIEWER := papers
	LYX := lyx
endif

.PHONY: main ci
main: jungian.tex
	xelatex jungian.tex
	xelatex jungian.tex
	xelatex jungian.tex
	-$(RM) *.aux *.log *.out *.toc *.lot src/*.aux
	-$(RM) src/beebe-energies-and-patterns/main.aux
	-$(VIEWER) jungian.pdf &

tobook: main
	pdfbook2 jungian.pdf

sutra:
	# pdf4 is xelatex
	$(LYX) -E pdf4 sutra.pdf lyx/Sutra.lyx
	-$(VIEWER) sutra.pdf &

# CI target: build all PDFs without opening viewers
# Future newly added build targets can be appended here
ci:
	xelatex jungian.tex
	xelatex jungian.tex
	xelatex jungian.tex
	-$(RM) *.aux *.log *.out *.toc *.lot src/*.aux
	$(LYX) -E pdf4 sutra.pdf lyx/Sutra.lyx

PHONY: fix-symbol
fix-symbol:
	find . -type f -name '*.tex' -exec sed -i -e "s/‘/'/g" '{}' +
	find . -type f -name '*.tex' -exec sed -i -e "s/’/'/g" '{}' +
	find . -type f -name '*.tex' -exec sed -i -e 's/“/``/g' '{}' +
	find . -type f -name '*.tex' -exec sed -i -e "s/”/''/g" '{}' +

beebe-energies-and-patterns:
	pdflatex src/beebe-energies-and-patterns.tex
	-$(VIEWER) beebe-energies-and-patterns.pdf

