GRCC = grcc

.PHONY: all
all: flowgraph

.PHONY: flowgraph
flowgraph: hier OreSat0.py OreSat0.cfg

.PHONY: hier
hier: hier/*.grc
	$(GRCC) -u $^

OreSat0.py: OreSat0.grc
	$(GRCC) $^
	@echo "### The errors about '__file__' not being defined are safe to ignore"
	patch $@ patches/OreSat0-hackrf.patch

OreSat0.cfg: OreSat0.cfg-dist
	cp -n $^ $@

.PHONY: clean
clean:
	rm OreSat0.py

.PHONY: distclean
distclean: clean
	rm OreSat0.cfg
