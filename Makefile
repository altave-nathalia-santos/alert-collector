PYENV_ROOT = $(HOME)/.pyenv
PYTHON_VERSION ?= 3.12.2
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3

install:
	@echo "Criando ambiente virtual..."
	@python3 -m venv $(VENV)
	@echo "Instalando dependências..."
	@$(PIP) install -r alert_colletor/requirements/requirements.txt

clean:
	@echo "Removendo o ambiente virtual..."
	@rm -rf $(VENV)
	@echo "Ambiente virtual removido!"

run:
	@source $(VENV)/bin/activate && python main.py
