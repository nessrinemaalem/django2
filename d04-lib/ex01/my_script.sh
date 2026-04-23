#!/bin/bash

pip --version
mkdir -p local_lib
pip install --upgrade --target=./local_lib git+https://github.com/jaraco/path.py.git > installation.log 2>&1
if [ $? -ne 0 ]; then
    echo "Erreur lors de l'installation de la bibliothèque path.py. Voir installation.log pour plus de détails."
    exit 1
fi
export PYTHONPATH=$(pwd)/local_lib:$PYTHONPATH
python3 my_program.py
