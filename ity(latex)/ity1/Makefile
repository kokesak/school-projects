all:run clean

FILENAME = proj1

run: $(FILENAME)

proj1: $(FILENAME).tex
	latex  $(FILENAME).tex 
	dvips -t a4 $(FILENAME).dvi
	ps2pdf  $(FILENAME).ps $(FILENAME).pdf

clean:
	rm -f *.dvi *.log *.aux *.out *.ps


