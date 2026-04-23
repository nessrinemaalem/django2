import psycopg2
from django.http import HttpResponse

def init(request):
    try:
        conn = psycopg2.connect(
            dbname="formationdjango",
            user="djangouser",
            password="secret",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ex00_movies (
                episode_nb      INTEGER PRIMARY KEY,
                title           VARCHAR(64) UNIQUE NOT NULL,
                opening_crawl   TEXT,
                director        VARCHAR(32) NOT NULL,
                producer        VARCHAR(128) NOT NULL,
                release_date    DATE NOT NULL
            );
        """)

        conn.commit()
        cursor.close()
        conn.close()

        return HttpResponse("OK")

    except psycopg2.OperationalError as e:
        return HttpResponse(f"Erreur de connexion : {e}", status=500)

    except psycopg2.Error as e:
        return HttpResponse(f"Erreur SQL : {e}", status=500)

    except Exception as e:
        return HttpResponse(f"Erreur inattendue : {e}", status=500)
