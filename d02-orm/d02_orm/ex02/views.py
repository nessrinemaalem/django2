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
            CREATE TABLE IF NOT EXISTS ex02_movies (
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

def populate(request):
    movies = [
        (1, "The Phantom Menace", "Turmoil has engulfed the Galactic Republic. The taxation of trade routes to outlying star systems is in dispute.", "George Lucas", "Rick McCallum", "1999-05-19"),
        (2, "Attack of the Clones", "There is unrest in the Galactic Senate. Several thousand solar systems have declared their intentions to leave the Republic.", "George Lucas", "Rick McCallum", "2002-05-16"),
        (3, "Revenge of the Sith", "War! The Republic is crumbling under attacks by the ruthless Sith Lord, Count Dooku.", "George Lucas", "Rick McCallum", "2005-05-19"),
        (4, "A New Hope", "It is a period of civil war. Rebel spaceships, striking from a hidden base, have won their first victory against the evil Galactic Empire.", "George Lucas", "Gary Kurtz, Rick McCallum", "1977-05-25"),
        (5, "The Empire Strikes Back", "It is a dark time for the Rebellion. Although the Death Star has been destroyed, Imperial troops have driven the Rebel forces from their hidden base and pursued them across the galaxy.", "Irvin Kershner", "Gary Kurtz, Rick McCallum", "1980-05-17"),
        (6, "Return of the Jedi", "Luke Skywalker has returned to his home planet of Tatooine in an attempt to rescue his friend Han Solo from the clutches of the vile gangster Jabba the Hutt.", "Richard Marquand", "Howard G. Kazanjian, George Lucas, Rick McCallum", "1983-05-25")
    ]

    try:
        conn = psycopg2.connect(
            dbname="formationdjango",
            user="djangouser",
            password="secret",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        for movie in movies:
            try:
                cursor.execute("""
                    INSERT INTO ex02_movies (episode_nb, title, opening_crawl, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, movie)
                conn.commit()
            except psycopg2.IntegrityError as e:
                conn.rollback()
                return HttpResponse(f"Erreur d'intégrité pour {movie[1]} : {e}", status=400)
        cursor.close()
        conn.close()
        response = "<br>".join([f"OK - {movie[1]}" for movie in movies])
        return HttpResponse(response)
    except psycopg2.OperationalError as e:
        return HttpResponse(f"Erreur de connexion : {e}", status=500)

    except psycopg2.Error as e:
        return HttpResponse(f"Erreur SQL : {e}", status=500)

    except Exception as e:
        return HttpResponse(f"Erreur inattendue : {e}", status=500)

def display(request):
    try:
        conn = psycopg2.connect(
            dbname="formationdjango",
            user="djangouser",
            password="secret",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT episode_nb, title, opening_crawl, director, producer, release_date FROM ex02_movies;")
        movies = cursor.fetchall()
        cursor.close()
        conn.close()

        if not movies:
            return HttpResponse("No data available")

        response = """
            <table border='1'>
                <tr>
                    <th>Episode</th>
                    <th>Title</th>
                    <th>Opening Crawl</th>
                    <th>Director</th>
                    <th>Producer</th>
                    <th>Release Date</th>
                </tr>
        """
        for movie in movies:
            response += "<tr>"
            for field in movie:
                response += f"<td>{field if field is not None else ''}</td>"
            response += "</tr>"

        response += "</table>"
        return HttpResponse(response)

    except psycopg2.OperationalError as e:
        return HttpResponse(f"Erreur de connexion : {e}", status=500)
    except psycopg2.Error as e:
        return HttpResponse(f"Erreur SQL : {e}", status=500)
    except Exception as e:
        return HttpResponse(f"Erreur inattendue : {e}", status=500)