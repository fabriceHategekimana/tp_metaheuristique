all:hello

hello: clear
	echo "Hello world!"

test: clear
	python3 src/tests.py

zip: clear
	zip -r TP4_AS_Fabrice_Hategekimana Makefile src 

deploy: zip
	cp -f TP4_AS_Fabrice_Hategekimana.zip /home/fabrice/rendu 

clear: FORCE
	clear

FORCE:
