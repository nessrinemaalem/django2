import os
import psycopg2
from django.http import HttpResponse

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data_d02sql')

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
            CREATE TABLE IF NOT EXISTS ex08_planets (
                id              SERIAL PRIMARY KEY,
                name            VARCHAR(64) UNIQUE NOT NULL,
                climate         VARCHAR,
                diameter        INTEGER,
                orbital_period  INTEGER,
                population      BIGINT,
                rotation_period INTEGER,
                surface_water   REAL,
                terrain         VARCHAR(128)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ex08_people (
                id              SERIAL PRIMARY KEY,
                name            VARCHAR(64) UNIQUE NOT NULL,
                birth_year      VARCHAR(32),
                gender          VARCHAR(32),
                eye_color       VARCHAR(32),
                hair_color      VARCHAR(32),
                height          INTEGER,
                mass            REAL,
                homeworld       VARCHAR(64),
                FOREIGN KEY (homeworld) REFERENCES ex08_planets(name)
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
            CREATE TEMP TABLE tmp_planets (
                name            VARCHAR(64),
                climate         VARCHAR,
                diameter        INTEGER,
                orbital_period  INTEGER,
                population      BIGINT,
                rotation_period INTEGER,
                surface_water   REAL,
                terrain         VARCHAR(128)
            );
        """)
        with open(os.path.join(DATA_DIR, 'planets.csv'), 'r') as f:
            cursor.copy_from(f, 'tmp_planets', sep='\t', null='NULL')
        cursor.execute("""
            INSERT INTO ex08_planets (name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain)
            SELECT name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain
            FROM tmp_planets
            ON CONFLICT (name) DO NOTHING;
        """)

        cursor.execute("""
            CREATE TEMP TABLE tmp_people (
                name            VARCHAR(64),
                birth_year      VARCHAR(32),
                gender          VARCHAR(32),
                eye_color       VARCHAR(32),
                hair_color      VARCHAR(32),
                height          INTEGER,
                mass            REAL,
                homeworld       VARCHAR(64)
            );
        """)
        with open(os.path.join(DATA_DIR, 'people.csv'), 'r') as f:
            cursor.copy_from(f, 'tmp_people', sep='\t', null='NULL')
        cursor.execute("""
            INSERT INTO ex08_people (name, birth_year, gender, eye_color, hair_color, height, mass, homeworld)
            SELECT name, birth_year, gender, eye_color, hair_color, height, mass, homeworld
            FROM tmp_people
            ON CONFLICT (name) DO NOTHING;
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

        cursor.execute("SELECT name, birth_year, gender, eye_color, hair_color, height, mass, homeworld FROM ex08_people ORDER BY name ASC;")
        people = cursor.fetchall()

        cursor.close()
        conn.close()

        if not people:
            return HttpResponse("No data available")

        response = """
            <table border='1'>
                <tr>
                    <th>Name</th>
                    <th>Birth Year</th>
                    <th>Gender</th>
                    <th>Eye Color</th>
                    <th>Hair Color</th>
                    <th>Height</th>
                    <th>Mass</th>
                    <th>Homeworld</th>
                </tr>
        """
        for person in people:
            response += "<tr>"
            for field in person:
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