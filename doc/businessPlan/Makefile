.PHONY: all clean
.SECONDEXPANSION:

all: podnik_zamer.pdf

podnik_zamer.pdf: podnik_zamer.tex imgs/cvut_text.jpg imgs/blockDiagram.pdf imgs/ucho.jpg imgs/PTO-Gantt.png
	pdflatex podnik_zamer.tex
	pdflatex podnik_zamer.tex
	bibtex podnik_zamer
	pdflatex podnik_zamer.tex
	pdflatex podnik_zamer.tex

clean:
	-rm -f podnik_zamer.aux
	-rm -f podnik_zamer.bbl
	-rm -f podnik_zamer.bib
	-rm -f podnik_zamer.blg
	-rm -f podnik_zamer.log
	-rm -f podnik_zamer.pdf
	-rm -f podnik_zamer.run.xml
	-rm -f podnik_zamer-blx.bib
