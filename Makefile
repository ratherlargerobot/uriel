.PHONY: default test clean install mypy check tar

PREFIX=/usr/local

VERSION=1.5.0

default:
	@echo "uriel is a single, executable Python script: nothing to build"

test:
	./testsuite.py

check: mypy test

mypy:
	mypy uriel

clean:
	rm -rf __pycache__
	rm -rf tests/__pycache__
	rm -rf .mypy_cache
	rm -rf dist

install:
	cp uriel ${PREFIX}/bin/uriel
	chown 0:0 ${PREFIX}/bin/uriel
	chmod 755 ${PREFIX}/bin/uriel
	mkdir -p ${PREFIX}/share/man/man1/
	cp uriel.1 ${PREFIX}/share/man/man1/
	chown 0:0 ${PREFIX}/share/man/man1/uriel.1

tar: dist/uriel-${VERSION}.tar.gz

dist/uriel-${VERSION}.tar.gz:
	mkdir -p dist
	rm -rf dist/uriel-${VERSION}
	mkdir dist/uriel-${VERSION}
	cp -a ChangeLog COPYING Makefile README.md uriel uriel.1 dist/uriel-${VERSION}/
	cp -a testsuite.py tests/ dist/uriel-${VERSION}/
	cp -a documentation/ dist/uriel-${VERSION}/
	cd dist/uriel-${VERSION}/ && make clean
	cd dist/uriel-${VERSION}/documentation/ && make clean
	cd dist/uriel-${VERSION}/documentation/ && make
	rm -rf dist/uriel-${VERSION}/documentation/lib/__pycache__
	fakeroot chown -R root:root dist/uriel-${VERSION}
	rm -f dist/uriel-${VERSION}.tar.gz
	(cd dist/ && fakeroot tar -cvf uriel-${VERSION}.tar uriel-${VERSION})
	gzip -9 dist/uriel-${VERSION}.tar
	rm -rf dist/uriel-${VERSION}/
