.PHONY: default test clean install mypy check

PREFIX=/usr/local

default:
	@echo "uriel is a single, executable Python script: nothing to build"

test:
	./testsuite.py

check: test mypy

mypy:
	mypy uriel

clean:
	rm -rf __pycache__
	rm -rf tests/__pycache__
	rm -rf .mypy_cache

install:
	cp uriel ${PREFIX}/bin/uriel
	chown root:root ${PREFIX}/bin/uriel
	chmod 755 ${PREFIX}/bin/uriel
	mkdir -p ${PREFIX}/share/man/man1/
	cp uriel.1 ${PREFIX}/share/man/man1/
	chown root:root ${PREFIX}/share/man/man1/uriel.1

