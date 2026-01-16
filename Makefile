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

.PHONY: main
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
