all:run

FILENAME = proj4

run: $(FILENAME)

$(FILENAME): $(FILENAME).tex
	latex  $(FILENAME).tex
	bibtex $(FILENAME)
	latex  $(FILENAME).tex
	latex  $(FILENAME).tex  
	dvips -t a4 $(FILENAME).dvi
	ps2pdf  $(FILENAME).ps $(FILENAME).pdf

clean:
	rm -f *.dvi *.log *.aux *.out *.ps *.pdf


