from django.shortcuts import render

def generate_gradient(base_color):
    """ Génère 50 nuances d'une couleur en augmentant progressivement la luminosité """
    gradient = []
    for i in range(50):
        factor = int((i / 49) * 255)
        r, g, b = base_color
        gradient.append(f"rgb({min(r+factor,255)}, {min(g+factor,255)}, {min(b+factor,255)})")
    return gradient


def index(request):
    # Couleurs de base (sombres)
    colors = {
        "noir": (0, 0, 0),
        "rouge": (100, 0, 0),
        "vert": (0, 100, 0),
        "bleu": (0, 0, 100),
    }

    # Générer les 50 nuances pour chaque couleur
    table = []
    for i in range(50):
        row = []
        for base in colors.values():
            factor = int((i / 49) * 155)  # on va jusqu'à +155 pour éclaircir
            r, g, b = base
            color = f"rgb({r+factor}, {g+factor}, {b+factor})"
            row.append(color)
        table.append(row)

    return render(request, 'ex03/index.html', {"table": table})