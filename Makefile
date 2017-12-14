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

send:
	scp -P 2238 -r src/ $(PI)

info:
	find src/ -name '[^]*.py' | xargs wc -l