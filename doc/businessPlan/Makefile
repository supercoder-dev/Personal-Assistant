.PHONY: all clean
.SECONDEXPANSION:

all: podnik_zamer.pdf

podnik_zamer.pdf: podnik_zamer.tex
	pdflatex podnik_zamer.tex
	pdflatex podnik_zamer.tex

clean:
	-rm -f podnik_zamer.aux
	-rm -f podnik_zamer.log
	-rm -f podnik_zamer.pdf
