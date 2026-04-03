import sys

def erreur(message):
    print("Erreur :", message)
    sys.exit(1)

def parse_args():
    if len(sys.argv) != 4:
        erreur("les arguments attendus sont : <latitude> <longitude> <precision 5-9>")

    try:
        latitude = float(sys.argv[1])
    except ValueError:
        erreur("La latitude doit être un nombre décimal valide.")

    try:
        longitude = float(sys.argv[2])
    except ValueError:
        erreur("La longitude doit être un nombre décimal valide.")

    try:
        precision = int(sys.argv[3])
    except ValueError:
        erreur("La précision doit être un entier compris entre 5 et 9.")

    if not (-90 <= latitude <= 90):
        erreur("La latitude doit être comprise entre -90 et +90 degrés.")

    if not (-180 <= longitude <= 180):
        erreur("La longitude doit être comprise entre -180 et +180 degrés.")

    if not (5 <= precision <= 9):
        erreur("La précision doit être comprise entre 5 et 9 caractères.")

    return latitude, longitude, precision


def encode_geohash(latitude, longitude, precision=7):

    BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"

    lat_interval = [-90.0, 90.0]
    lon_interval = [-180.0, 180.0]

    geohash = []
    bits = []
    is_lon = True

    while len(geohash) < precision:

        if is_lon:
            mid = sum(lon_interval) / 2
            if longitude >= mid:
                bits.append(1)
                lon_interval[0] = mid
            else:
                bits.append(0)
                lon_interval[1] = mid
        else:
            mid = sum(lat_interval) / 2
            if latitude >= mid:
                bits.append(1)
                lat_interval[0] = mid
            else:
                bits.append(0)
                lat_interval[1] = mid

        is_lon = not is_lon

        if len(bits) >= 5:
            value = 0
            for b in bits[:5]:
                value = (value << 1) | b

            geohash.append(BASE32[value])
            bits = bits[5:]

    return "".join(geohash)


if __name__ == "__main__":
    latitude, longitude, precision = parse_args()
    geohash = encode_geohash(latitude, longitude, precision)
    print("Pour :", "\n\t- une latitude de", latitude, "\n\t- une longitude de", longitude, "\n\t- une précision de", precision, "\n\nle geohash est ", geohash)
    # compare result on https://www.movable-type.co.uk/scripts/geohash.html