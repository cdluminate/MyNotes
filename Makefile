# Detect the operating system
UNAME_S := $(shell uname -s)

# Set the viewer command based on the OS
ifeq ($(UNAME_S),Darwin)
	# macOS
	VIEWER := open -a preview
	LYX := /Applications/LyX.app/Contents/MacOS/lyx
else
	# Linux
	VIEWER := evince
	LYX := lyx
endif

.PHONY: main ci
main: jungian.tex
	xelatex jungian.tex
	xelatex jungian.tex
	xelatex jungian.tex
	-$(RM) *.aux *.log *.out *.toc *.lot src/*.aux
	-$(VIEWER) jungian.pdf &

tobook: main
	pdfbook2 jungian.pdf

sutra:
	# pdf4 is xelatex
	$(LYX) -E pdf4 sutra.pdf lyx/Sutra.lyx
	-$(VIEWER) sutra.pdf &

# CI target: build all PDFs without opening viewers
ci:
	xelatex jungian.tex
	xelatex jungian.tex
	xelatex jungian.tex
	$(LYX) -E pdf4 sutra.pdf lyx/Sutra.lyx
#   Future newly added build targets can be appended here
	-$(RM) *.aux *.log *.out *.toc *.lot src/*.aux
