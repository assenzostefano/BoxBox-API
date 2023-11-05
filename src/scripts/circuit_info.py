import datetime
import os
from urllib.parse import urlsplit

import fastf1
import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv()

HOST_POSTGRESS = os.getenv('HOST_POSTGRESS')
PORT_POSTGRESS = os.getenv('PORT_POSTGRESS')
DB_POSTGRESS = os.getenv('DBNAME_POSTGRESS')
USER_POSTGRESS = os.getenv('USER_POSTGRESS')
PASSWORD_POSTGRESS = os.getenv('PASSWORD_POSTGRESS')

# Ottieni il percorso della cartella corrente
current_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso della cartella di cache relativo al percorso corrente
cache_directory = os.path.join(current_directory, '../..', 'cache')

fastf1.Cache.enable_cache(cache_directory)  # optionally change cache location

def get_all_circuits():
    conn = psycopg2.connect(
        host=HOST_POSTGRESS,
        port=PORT_POSTGRESS,
        database=DB_POSTGRESS,
        user=USER_POSTGRESS,
        password=PASSWORD_POSTGRESS,
        sslmode='require'
    )
    cur = conn.cursor()
    # Take current year
    year = datetime.datetime.now().year
    year += 1
    years = range(1950, year)
    for year in years:
        print(year)
        url = f"http://ergast.com/api/f1/{year}/circuits.json"
        response = requests.get(url)
        data = response.json()
        circuits = data['MRData']['CircuitTable']['Circuits']
        for circuit in circuits:
            circuit_id = circuit['circuitId']
            circuit_name = circuit['circuitName']
            locality = circuit['Location']['locality']
            country = circuit['Location']['country']
            latitude = circuit['Location']['lat']
            longitude = circuit['Location']['long']
            url = circuit['url']
            
            try:
                base_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
                parsed_link = urlsplit(url)
                path = parsed_link.path
                filename = os.path.basename(path)
                page_title = os.path.splitext(filename)[0]
                url_wikipedia = base_url + page_title
                response_wikipedia = requests.get(url_wikipedia)
                data_wikipedia = response_wikipedia.json()
                driver_biography = data_wikipedia['extract']
            except:
                driver_biography = ""
            
            try:
                # Esegue l'inserimento o l'aggiornamento del circuito
                cur.execute("""
                    INSERT INTO circuits (circuit_id, circuit_name, locality, country, latitude, longitude, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (circuit_id) DO NOTHING
                """, (circuit_id, circuit_name, locality, country, latitude, longitude, url))
                
                # Controlla se l'anno non è già stato aggiunto nella colonna years_used
                cur.execute("""
                    SELECT years_used FROM circuits WHERE circuit_id = %s
                """, (circuit_id,))
                result = cur.fetchone()
                if result is not None:
                    years_used = result[0].split(',') if result[0] is not None else []  # Converte la stringa in un elenco di stringhe o assegna una lista vuota
                    if str(year) not in years_used:  # Converte l'anno in stringa per il confronto
                        years_used.append(str(year))
                else:
                    years_used = [str(year)]
                
                # Aggiorna l'elenco degli anni utilizzati
                cur.execute("""
                    UPDATE circuits
                    SET years_used = %s
                    WHERE circuit_id = %s
                """, (','.join(years_used), circuit_id))  # Converte l'elenco in una stringa separata da virgole
                
                conn.commit()
            except psycopg2.Error as e:
                print(f"Error inserting/updating circuit {circuit_id}: {e}")

        print('------------------')
    cur.close()
    conn.close()

def create_circuit_table():
    conn = psycopg2.connect(
            host=HOST_POSTGRESS,
            port=PORT_POSTGRESS,
            database=DB_POSTGRESS,
            user=USER_POSTGRESS,
            password=PASSWORD_POSTGRESS,
            sslmode='require'
        )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS circuits (
            circuit_id VARCHAR(255) PRIMARY KEY,
            circuit_name VARCHAR(255),
            locality VARCHAR(255),
            country VARCHAR(255),
            latitude FLOAT,
            longitude FLOAT,
            url VARCHAR(255),
            years_used VARCHAR(1000)
        );
    """)

    conn.commit()
    print("Table 'circuits' created successfully.")

    cur.close()
    conn.close()

def delete_table_drivers():
    conn = psycopg2.connect(
        host=HOST_POSTGRESS,
        port=PORT_POSTGRESS,
        database=DB_POSTGRESS,
        user=USER_POSTGRESS,
        password=PASSWORD_POSTGRESS,
        sslmode='require'
    )
    cur = conn.cursor()
    cur.execute("DROP TABLE circuits;")
    conn.commit()
    print("Table 'circuits' deleted successfully.")
    cur.close()
    conn.close()

get_all_circuits()
#create_circuit_table()
#delete_table_drivers()