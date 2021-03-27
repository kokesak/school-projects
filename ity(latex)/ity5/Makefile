all:run

FILENAME = proj5

run: $(FILENAME)

$(FILENAME): $(FILENAME).tex
	pdflatex  $(FILENAME).tex
	pdflatex $(FILENAME).tex

clean:
	rm -f *.dvi *.log *.aux *.out *.ps *.pdf


