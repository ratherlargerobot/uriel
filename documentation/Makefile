##############################################################################
# uriel project Makefile                                                     #
##############################################################################

# path to uriel
URIEL=../uriel

# uriel project subdirectories
STATIC=static
NODES=nodes
TEMPLATES=templates
PUBLIC=public
LIB=lib

##############################################################################
# targets                                                                    #
##############################################################################

.PHONY: site clean preview

site:
	${URIEL} .

clean:
	rm -rf ${PUBLIC}/
	rm -rf ${LIB}/__pycache__

preview: site
	cd ${PUBLIC}/ && python3 -m http.server

