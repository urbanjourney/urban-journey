.PHONY: help clean dist tests docs-html docs-pdf install-dev uninstall-dev

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean          Removes temporarily files"
	@echo "  dist           Build Urban Journey Distribution package"
	@echo "  tests			Run unit-tests"
	@echo "  docs-html      Build HTML Sphinx documentation"
	@echo "  doct-pdf       Build PDF Sphinx documentation"
	@echo "  install-dev    Installs Urban Journey as develop package"
	@echo "  uninstall-dev  Uninstall Urban Journey as develop package"

clean:
	rm -rf dist/*
	rm -rf docs/_build/*
	rm -rf docs/_static/*
	rm -rf *egg-info
	python3 setup.py clean

dist:
	python3 setup.py -q sdist --formats=zip

tests:
	python3 setup.py test

docs-html:
	$(MAKE) -C docs/ html

docs-pdf:
	$(MAKE) -C docs/ latexpdf

install-dev:
	sudo python3 setup.py develop

uninstall-dev:
	sudo python3 setup.py develop --uninstall
