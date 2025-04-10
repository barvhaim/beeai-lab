.PHONY: install-deps
install-deps:
	@echo "Installing general dependencies"
	pip install -r requirements.txt

.PHONY: install-llms-deps
install-llms-deps: install-deps
	@echo "Installing llms dependencies"
	pip install -r llms/requirements.txt

.PHONY: install-agents-deps
install-agents-deps: install-deps
	@echo "Installing agents dependencies"
	pip install -r agents/requirements.txt