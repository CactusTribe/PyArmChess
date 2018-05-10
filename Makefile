PI=pi@joaquim-lefranc.butandsystems.com:~/PyArmChess/
VERSION=0.1

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
	UI_DIR = interface_linux/
endif
ifeq ($(UNAME_S),Darwin)
	UI_DIR = interface_osx/
endif

run:
	python3 pyarmchess_interactive.py

calib:
	python3 test.py vision/samples/empty.jpg -c

test:
	python3 test.py vision/samples/${sample}.jpg

send:
	@scp vision/ChessCamera.py joaquim@192.168.1.15:~/pyprojects/PyArmChess/vision/
	@scp vision/constants.py joaquim@192.168.1.15:~/pyprojects/PyArmChess/vision/
	@scp test.py joaquim@192.168.1.15:~/pyprojects/PyArmChess/
	@scp Game.py joaquim@192.168.1.15:~/pyprojects/PyArmChess/
	@scp Makefile joaquim@192.168.1.15:~/pyprojects/PyArmChess/

info:
	find . -name '*.py' | xargs wc -l

.PHONY: lint
lint:
	pylint controler *.py --disable=fixme

tests:
	python3 -m unittest discover

config:
	pip install -r requirements.txt
