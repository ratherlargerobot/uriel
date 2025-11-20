.PHONY: default test clean install

PREFIX=/usr/local

default:
	@echo "uriel is a single, executable Python script: nothing to build"

test:
	./testsuite.py

clean:
	rm -rf __pycache__
	rm -rf tests/__pycache__

install:
	cp uriel ${PREFIX}/bin/uriel
	chown root:root ${PREFIX}/bin/uriel
	chmod 755 ${PREFIX}/bin/uriel
	cp uriel.1 ${PREFIX}/share/man/man1/
	chown root:root ${PREFIX}/share/man/man1/uriel.1

