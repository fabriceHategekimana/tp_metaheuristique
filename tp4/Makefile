all:start

start: clear
	echo "Hello world!"

test: clear
	python3 tests.py

command: clear
	cat Makefile | grep ": FORCE" | sed "s/: FORCE//" | grep --invert-match "FORCE" 

commands: clear
	cat Makefile | grep ": FORCE" | sed "s/: FORCE//" | grep --invert-match "FORCE" 

clear: FORCE
	clear

FORCE:
