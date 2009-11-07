
all: tests

install:
	cp -p pyrg.py /usr/local/bin/pyrg && chmod 755 /usr/local/bin/pyrg

tests:
	python test/testall.py

clean:
	rm *.pyc
