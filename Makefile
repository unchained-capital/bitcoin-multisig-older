#
# == Paths & Directories ==
#

ROOT_DIR  := $(shell pwd)
NODE_DIR  := $(ROOT_DIR)/node_modules
VENV_DIR  := $(ROOT_DIR)/.venv

#
# == Configuration ==
#

#
# == Commands ==
#

MKDIR      := mkdir -p
LN         := ln
FIND       := find
PIPENV     := pipenv
PYTHON     := python
NPM        := npm

#
# == Top-Level Targets ==
#

default: dependencies

dependencies: python-dependencies nodejs-dependencies

dev-dependencies: python-dependencies-dev nodejs-dependencies-dev

freeze:
	$(PIPENV) lock
	$(NPM) shrinkwrap

purge:
	rm -r $(NODE_DIR)
	rm -r $(VENV_DIR)

server:
	$(NPM) start

test: python-test

test-integration: python-test-integration 

test-full: python-test-full


#
# == Dependencies ==
#

python-dependencies:
	PIPENV_VENV_IN_PROJECT=true $(PIPENV) install --ignore-pipfile

nodejs-dependencies:
	$(NPM) install --production

python-dependencies-dev:
	PIPENV_VENV_IN_PROJECT=true $(PIPENV) install --ignore-pipfile --dev

nodejs-dependencies-dev:
	$(NPM) install

# 
# == Testing ==
#

python-test:
	$(PIPENV) run pytest -m "not integration" --cov=pymultisig --cov-config pymultisig/tests/.coveragerc


# Ideally, instead of 'plug in trezor', we just started a trezor emulator...
python-test-integration:
	@printf '%s\n' '-----------------'
	@printf '%s\n' "| Plug in Trezor |"
	@printf '%s\n' '-----------------'
	@read -n1 -r -p "Then press space to continue..." key
	@printf '\n'
	$(PIPENV) run pytest -m "integration" --cov=pymultisig --cov-config pymultisig/tests/.coveragerc -vv

python-test-full:
	- $(PIPENV) run pytest -m "not integration" --cov=pymultisig --cov-config pymultisig/tests/.coveragerc
	@printf '%s\n' '-----------------'
	@printf '%s\n' "| Plug in Trezor |"
	@printf '%s\n' '-----------------'
	@read -n1 -r -p "Then press space to continue..." key
	@printf '\n'
	$(PIPENV) run pytest -m "integration" --cov-append --cov=pymultisig --cov-config pymultisig/tests/.coveragerc


js-test:
	NODE_ENV="test" $(MOCHA) --recursive --grep @integration --invert --require babel-register --require babel-polyfill --require ./test/testHelper.js


js-test-integration:
	@printf '%s\n' '-----------------'
	@printf '%s\n' "| Plug in Ledger |"
	@printf '%s\n' '-----------------'
	@read -n1 -r -p "Then press space to continue..." key
	@printf '\n'
	NODE_ENV="test" $(MOCHA) --recursive --grep @integration-ledger --require babel-register --require babel-polyfill --require ./test/testHelper.js


.PHONY: test
