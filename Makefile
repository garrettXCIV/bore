.PHONY:
	build
	build-src
	build-wheel
	ci
	clean
	clean-build
	clean-docs
	clean-tmp
	dry-pypi
	git-undo
	git-update
	isort
	lint
	lint-docs
	pip-update
	precommit
	pypi-upload
	readme-check
	readme-desc
	test
	test-local
	testpypi-upload

build:
	python setup.py sdist bdist_wheel

build-src:
	python setup.py sdist

build-wheel:
	python setup.py bdist_wheel

ci:
	$(MAKE) isort
	$(MAKE) lint
	$(MAKE) lint-docs
	$(MAKE) test

clean:
	$(MAKE) clean-build
	$(MAKE) clean-docs
	$(MAKE) clean-tmp

clean-build:
	rm -rf *.egg-info build dist

clean-docs:
	rm -rf docs/_build

clean-tmp:
	rm -rf tmp

dry-pypi:
	python setup.py --dry-run sdist bdist_wheel upload -s -r https://test.pypi.org/legacy/

git-undo:
	git reset --soft

git-update:
	git update-index --again

isort:
	isort -rc bore.py tests --atomic --check-only --diff

lint:
	flake8 bore.py setup.py tests
	pylint bore.py setup.py tests

lint-docs:
	doc8 README.rst CHANGELOG --ignore D005

pip-update:
	$(eval UPDATED := $(shell pip list --outdated --pre --format=freeze | grep -v '^\-e' | cut -d = -f 1))
	@pip list --outdated --pre --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U --pre
	@printf "\n%s\n" "******************************************"
	@printf "%s\n" "PYTHON PACKAGES UPDATED"
	@printf "%s\n" "------------------------------------------"
	@$(foreach UPDATE,$(UPDATED),pip list --format=freeze | grep $(UPDATE) | xargs -I {} printf "{}\n";)
	@printf "%s\n\n" "******************************************"

precommit:
	$(MAKE) pip-update
	$(MAKE) clean
	$(MAKE) isort
	$(MAKE) lint
	$(MAKE) lint-docs
	$(MAKE) test-local
	$(MAKE) readme-check

pypi-upload:
	python setup.py sdist bdist_wheel upload -s

readme-check:
	python setup.py check -r -s

readme-desc:
	python setup.py check -r -s
	python setup.py --long-description | rst2html.py > tmp/long_desc/output.html

# FIXME: Fix tox!!
test:
	tox -e

test-local:
	tox -e

testpypi-upload:
	python setup.py sdist bdist_wheel upload -s -r https://test.pypi.org/legacy/
