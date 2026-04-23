# ============================================================
#  Makefile – Projet Django d07-sessions
#  Utilisation : make <commande>
# ============================================================

# --- Configuration -------------------------------------------
PYTHON     = python3
MANAGE     = $(PYTHON) manage.py
DB_SQLITE  = db.sqlite3

# --- Aide ----------------------------------------------------

help:  ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# --- Serveur Django ------------------------------------------

runserver:  ## Lance le serveur de développement Django
	$(MANAGE) runserver

runserver-plus:  ## Lance le serveur sur un port personnalisé (ex: make runserver-plus PORT=8080)
	$(MANAGE) runserver $(PORT)

# --- Migrations ----------------------------------------------

migrate:  ## Applique les migrations
	$(MANAGE) migrate

makemigrations:  ## Crée les fichiers de migration
	$(MANAGE) makemigrations

# --- Suppression de la base ----------------------------------

drop-sqlite:  ## Supprime le fichier SQLite (irréversible !)
	@rm -f $(DB_SQLITE)
	@echo "✅  Base SQLite supprimée."

reset-db:  ## Supprime la DB SQLite ET réapplique toutes les migrations
	$(MAKE) drop-sqlite
	$(MAKE) migrate
	@echo "✅  Base de données réinitialisée."

# --- Nettoyage -----------------------------------------------

clean-migrations:  ## Supprime tous les fichiers de migration (sauf __init__.py)
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -delete
	@echo "✅  Fichiers de migration supprimés."

full-reset:  ## Supprime migrations + DB SQLite + recrée tout from scratch
	$(MAKE) clean-migrations
	$(MAKE) drop-sqlite
	$(MAKE) makemigrations
	$(MAKE) migrate

# --- Utilitaires ---------------------------------------------

shell:  ## Ouvre le shell Django
	$(MANAGE) shell

superuser:  ## Crée un superutilisateur Django
	$(MANAGE) createsuperuser

collectstatic:  ## Collecte les fichiers statiques
	$(MANAGE) collectstatic --noinput

install:  ## Installe les dépendances Python
	pip install -r requirements.txt

.PHONY: help runserver runserver-plus migrate makemigrations drop-sqlite \
        reset-db clean-migrations full-reset shell superuser collectstatic install
