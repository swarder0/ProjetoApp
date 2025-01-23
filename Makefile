# Variáveis
PYTHON := python
TEST_DIR := src
COV_REPORT := --cov-report term-missing --cov=.

# Rodar os testes
test:
	$(PYTHON) -m pytest $(TEST_DIR) $(COV_REPORT)

.PHONY: test

# Verificar lint
lint:
	flake8 .

# Formatar código
format:
	black .

# Checar tipos
type-check:
	mypy .

# Executar tudo
all: format lint type-check test
