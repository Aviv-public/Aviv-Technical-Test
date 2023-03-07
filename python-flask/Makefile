#!/usr/bin/env make

.DEFAULT_GOAL: help

MAKEFLAGS=--no-print-directory

DOCKER_COMPOSE?=docker-compose -p aviv-technical-test

SHELL_COMMAND_WITHOUT_DEPS?=$(DOCKER_COMPOSE) run --user listingapi:listingapi --rm -T --no-deps python-flask bash -c

.PHONY: help
help: ## List all Python Makefile targets
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'


##
## Python Containers 📦
## -----------------
##
.PHONY: run
run:  ## Run a python-flask container
	$(DOCKER_COMPOSE) run -p 8080:8080 --rm python-flask python app.py

.PHONY: stop
stop:  ## Stop the running containers
	$(DOCKER_COMPOSE) down --rm

.PHONY: build
build: ## Build the python docker image
	docker build --label python-flask --label aviv-technical-test -t ghcr.io/meilleursagents/aviv-technical-test/python-flask:latest .

.PHONY: clear
clear:  ## Clear volumes and stop containers
	$(DOCKER_COMPOSE) down --volumes --remove-orphans
	docker image prune -af --filter label=aviv-technical-test

.PHONY: shell
shell: ## Open a bash shell on a python-flask container
	$(DOCKER_COMPOSE) run --rm python-flask bash


##
## Python Tests 🧪
## ------------
##
.PHONY: test
test: ## Shortcut to launch all the test tasks (unit, functional and integration).
	$(SHELL_COMMAND_WITHOUT_DEPS) "pytest -Werror tests"


##
## Python Code Analysis 🔎
## --------------------
##
.PHONY: format
format: ## Format code
	$(SHELL_COMMAND_WITHOUT_DEPS) "isort tests listingapi && black ."

.PHONY: style
style: ## Check lint, code styling rules
	$(SHELL_COMMAND_WITHOUT_DEPS) "mypy tests listingapi && flake8 tests listingapi && isort tests listingapi -c && black --check ."

.PHONY: complexity
complexity: ## Compute cyclomatic complexity and maintainability check
	$(SHELL_COMMAND_WITHOUT_DEPS) \
		"radon cc -s -n B listingapi | tee /tmp/cc.txt && if [ -s /tmp/cc.txt ]; then exit 1; fi; \
		radon mi -n B listingapi | tee /tmp/mi.txt && if [ -s /tmp/mi.txt ]; then exit 1; fi;"


##
## Python tools 🧰
## ------------
##
.PHONY: lock-dependencies
lock-dependencies: ## Lock dependencies to update Pipfile.lock file
	$(SHELL_COMMAND_WITHOUT_DEPS) "pipenv lock"

.PHONY: generate-random-listings
generate-random-listings: ## Generates and displays 10 random listings payloads
	$(SHELL_COMMAND_WITHOUT_DEPS) "python generate_random_listings.py"
