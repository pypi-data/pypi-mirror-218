#!make
# -*- coding:utf-8 -*-
#
.PHONY: update_hgstamp
.phony:distclean checkin release build  all clean readme install

all:build install

CC  ?=/usr/bin/clang
CXX ?=/usr/bin/clang++
PYTHON3 ?=$(shell which python3)
PYTHON2 ?=$(shell which python2)

# from https://www.mercurial-scm.org/wiki/VersioningWithMake
#HGVERSION:= $(shell hg parents --template 'hgid: {node|short}')
HGVERSION:= $(shell hg parents --template 'HGTagShort = \\\"{latesttag}.{latesttagdistance}\\\"')
VERSION:= $(shell hg parents --template '{latesttag}.{latesttagdistance}')

update_hgstamp:
	[ -f hgstamp.py ] && rm hgstamp.py
	make hgstamp.py

hgstamp.py: 
	[ -f $@ ] || touch $@
	echo $(HGVERSION) | cmp -s $@ - || echo $(HGVERSION) > $@
#


distclean:
	-rm ./build/bdist.*


checkin :
	-hg ci -m "before release $(VERSION)"
	-hg kwexpand
	make update_hgstamp


release: distclean
	make readme
	make checkin
	-hg bookmark -i "release $(VERSION)"
	$(PYTHON3) setup.py sdist


upload: release
	$(PYTHON3) -m twine upload  dist/PythonCA-$(VERSION).tar.gz


pythonca: setup.py hgstamp.py
	$(PYTHON3) setup.py clean
	$(PYTHON3) setup.py build
	-$(PYTHON2) setup.py clean
	-$(PYTHON2) setup.py build


install:
	-rm -r ./build/bdist.*
	#$(PYTHON3) setup.py install
	$(PYTHON3) -m pip install ./
	-rm -r ./build/bdist.*
	#python2 setup.py install
	$(PYTHON2) -m pip install ./


build: pythonca


readme: README.rst
	/usr/local/bin/pandoc -t plain -o README.txt README.rst
	/usr/local/bin/pandoc -t html -o README.html README.rst
	/usr/local/bin/pandoc -t markdown -o README.md README.rst


sdist:
	$(PYTHON3) setup.py sdist

