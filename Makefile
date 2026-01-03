# Detect the operating system
UNAME_S := $(shell uname -s)

# Set the viewer command based on the OS
ifeq ($(UNAME_S),Darwin)
	# macOS
	VIEWER := open -a preview
else
	# Linux
	VIEWER := evince
endif

main: jungian.tex
	xelatex jungian.tex
	xelatex jungian.tex
	xelatex jungian.tex
	-$(RM) *.aux *.log *.out *.toc *.lot src/*.aux
	-$(VIEWER) jungian.pdf &
