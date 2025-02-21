PYTHON = python3
VENV_DIR = .venv
ACTIVATE = source $(VENV_DIR)/bin/activate

install:
	@echo "Criando ambiente virtual..."
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(ACTIVATE) && pip install -r alert_colletor/requirements/requirements.txt

clean:
	@echo "Removendo o ambiente virtual..."
	@rm -rf $(VENV_DIR)
	@echo "Ambiente virtual removido!"

run:
	@$(ACTIVATE) && python main.py
