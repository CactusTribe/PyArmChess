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
	python3 src/main.py

test:
	python3 vision/test.py vision/samples/${sample}

send:
	@scp vision/ChessCamera.py joaquim@192.168.1.15:~/pyprojects/PyArmChess/vision/
	@scp vision/constants.py joaquim@192.168.1.15:~/pyprojects/PyArmChess/vision/
	@scp vision/test.py joaquim@192.168.1.15:~/pyprojects/PyArmChess/vision/
	@scp Game.py joaquim@192.168.1.15:~/pyprojects/PyArmChess/

info:
	find src/ -name '[^]*.py' | xargs wc -l
