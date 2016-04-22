.PHONY: all clean
.SECONDEXPANSION:

all: progressionReport.pdf

progressionReport.pdf: progressionReport.tex imgs/cvut_text.jpg imgs/blockDiagram.pdf imgs/logo.pdf imgs/PTO-Gantt.png
	pdflatex progressionReport.tex
	pdflatex progressionReport.tex
	bibtex progressionReport
	pdflatex progressionReport.tex
	pdflatex progressionReport.tex

clean:
	-rm -f progressionReport.aux
	-rm -f progressionReport.bbl
	-rm -f progressionReport.bcf
	-rm -f progressionReport.bib
	-rm -f progressionReport.blg
	-rm -f progressionReport.log
	-rm -f progressionReport.pdf
	-rm -f progressionReport.run.xml
	-rm -f progressionReport.out
	-rm -f progressionReport-blx.bib
