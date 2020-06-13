ENV := . env/bin/activate;
PYTHON := $(ENV) python3

.PHONY: all backend build clean docker docs env e2e frontend hooks lint precommit tests

all: docs lint tests

backend: env
	@$(PYTHON) -m app

build: node_modules
	@npx parcel build src/index.html

clean:
	@rm -fR docs/build docs/source/apidoc

docker:
	docker build -t mathsnuggets .
	docker tag mathsnuggets bknguyen/mathsnuggets
	docker push bknguyen/mathsnuggets

docs: env
	@$(ENV) sphinx-apidoc -fME --implicit-namespaces -o docs/source/apidoc mathsnuggets
	@$(ENV) sphinx-build -M html docs/source docs/build

env: env/bin/activate

env/bin/activate: requirements.txt
	@test -d env || python3 -m venv env
	@$(PYTHON) -m pip install -Ur requirements.txt
	@touch env/bin/activate

e2e: build env
	@$(PYTHON) -m app &
	sleep 1
	npx mocha --timeout 10000 src/tests
	sleep 1
	ps -ef | grep "env/bin/python3 -m app" | awk '{print $$2}' | head -1 | xargs kill

frontend: node_modules
	@npx parcel watch src/index.html

hooks:
	@echo "make precommit" > .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit

lint: env node_modules
	@$(ENV) isort --apply --skip env
	@$(PYTHON) -m black .
	@$(PYTHON) -m flake8
	@npx eslint --fix --ignore-path .gitignore src/*

node_modules: package.json
	@npm install

precommit:
	@$(ENV) isort -c --skip env
	@$(PYTHON) -m black .
	@$(PYTHON) -m flake8
	@npx eslint --ignore-path .gitignore src/*

tests: env
	@$(PYTHON) -m pytest -v --cov=. --cov-report=xml -n 4 tests/
	@$(PYTHON) -m coverage html
