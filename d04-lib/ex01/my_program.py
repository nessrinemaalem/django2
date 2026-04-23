from path import Path


def creer_et_lire_fichier():
    dossier = Path("un_dossier")
    fichier = "un_fichier.txt"
    chemin_fichier = dossier / fichier

    dossier.makedirs_p()

    texte_a_ecrire = """Le programme Python à créer est une composition de votre choix, qui doit néanmoins respecter ces contraintes :
• Son extension doit être .py car c’est un programme Python.
• Il doit importer le module path.py depuis l’endroit où cette bibliothèque a été
installée, grâce au script précédent.
• Il doit créer un dossier puis un fichier à l’interieur de ce dossier, écrire quelque
chose dans ce fichier et enfin lire puis afficher son contenu.
• Il doit respecter les règles spécifiques de la journée.
"""

    chemin_fichier.write_text(texte_a_ecrire, encoding="utf-8")

    contenu = chemin_fichier.read_text(encoding="utf-8")

    print("Contenu du fichier :")
    print(contenu)


if __name__ == "__main__":
    creer_et_lire_fichier()
