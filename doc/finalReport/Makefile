.PHONY: all clean
.SECONDEXPANSION:

all: finalReport.pdf

finalReport.pdf: finalReport.tex imgs/cvut_text.jpg imgs/blockDiagram.pdf imgs/logo.pdf imgs/PTO-Gantt.png
	pdflatex finalReport.tex
	pdflatex finalReport.tex
	bibtex finalReport
	pdflatex finalReport.tex
	pdflatex finalReport.tex

clean:
	-rm -f finalReport.aux
	-rm -f finalReport.bbl
	-rm -f finalReport.bcf
	-rm -f finalReport.bib
	-rm -f finalReport.blg
	-rm -f finalReport.log
	-rm -f finalReport.pdf
	-rm -f finalReport.run.xml
	-rm -f finalReport.out
	-rm -f finalReport-blx.bib
