from django.shortcuts import render
from django.conf import settings
from .forms import TextForm
from datetime import datetime
import os

def index(request):

    form = TextForm()
    log_path = settings.LOG_FILE_PATH

    # ---- 1) Charger l'historique existant au démarrage ----
    historique = []
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                historique.append(line.strip())

    # ---- 2) Si le formulaire est soumis ----
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            texte = form.cleaned_data["text"]
            horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entree = f"{horodatage} - {texte}"

            # ---- 3) Écrire dans le fichier de logs ----
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(entree + "\n")

            # ---- 4) Ajouter à l'historique affiché à l'écran ----
            historique.append(entree)

    return render(request, "ex02/index.html", {
        "form": form,
        "historique": historique
    })

