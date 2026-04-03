VENV=django_venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
PROJECT=imaalem

.PHONY: help venv install run migrate makemigrations createsuperuser shell freeze clean

help:
	@echo "Commandes disponibles :"
	@echo "  make venv              -> Créer le virtualenv"
	@echo "  make install           -> Installer les dépendances"
	@echo "  make run               -> Lancer le serveur Django"
	@echo "  make migrate           -> Appliquer les migrations"
	@echo "  make makemigrations    -> Créer les migrations"
	@echo "  make createsuperuser   -> Créer un super utilisateur"
	@echo "  make shell             -> Lancer le shell Django"
	@echo "  make freeze            -> Générer requirements.txt"
	@echo "  make clean             -> Supprimer le venv et fichiers temporaires"

venv:
	python3 -m venv $(VENV)

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(PROJECT)/manage.py runserver 127.0.0.1:8000

migrate:
	$(PYTHON) $(PROJECT)/manage.py migrate

makemigrations:
	$(PYTHON) $(PROJECT)/manage.py makemigrations

createsuperuser:
	$(PYTHON) $(PROJECT)/manage.py createsuperuser

shell:
	$(PYTHON) $(PROJECT)/manage.py shell

freeze:
	$(PIP) freeze > requirements.txt

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
