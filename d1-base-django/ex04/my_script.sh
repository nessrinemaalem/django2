#!/bin/bash

python3 -m venv django_venv

source django_venv/bin/activate

pip install --upgrade pip

pip install -r requirement.txt

echo "Virtualenv django_venv créé, dépendances installées et environnement activé."
echo "Pour utiliser le venv, tape : source django_venv/bin/activate"

