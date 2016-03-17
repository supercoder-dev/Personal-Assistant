.PHONY: all clean
.SECONDEXPANSION:

all: businessPlan.pdf

businessPlan.pdf: businessPlan.tex imgs/cvut_text.jpg imgs/blockDiagram.pdf imgs/logo.pdf imgs/PTO-Gantt.png
	pdflatex businessPlan.tex
	pdflatex businessPlan.tex
	bibtex businessPlan
	pdflatex businessPlan.tex
	pdflatex businessPlan.tex

clean:
	-rm -f businessPlan.aux
	-rm -f businessPlan.bbl
	-rm -f businessPlan.bcf
	-rm -f businessPlan.bib
	-rm -f businessPlan.blg
	-rm -f businessPlan.log
	-rm -f businessPlan.pdf
	-rm -f businessPlan.run.xml
	-rm -f businessPlan.out
	-rm -f businessPlan-blx.bib
