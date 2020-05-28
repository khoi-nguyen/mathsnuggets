ENV := . env/bin/activate;
PYTHON := $(ENV) python3

.PHONY: all backend clean docker docs env frontend hooks lint precommit tests

all: docs lint tests

backend: env
	@$(PYTHON) -m app

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
	@$(PYTHON) -m pytest -v --cov=. --cov-report=xml tests/
	@$(PYTHON) -m coverage html
