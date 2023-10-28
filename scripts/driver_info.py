import os
from urllib.parse import urlsplit

import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv()

HOST_POSTGRESS = os.getenv('HOST_POSTGRESS')
PORT_POSTGRESS = os.getenv('PORT_POSTGRESS')
DB_POSTGRESS = os.getenv('DBNAME_POSTGRESS')
USER_POSTGRESS = os.getenv('USER_POSTGRESS')
PASSWORD_POSTGRESS = os.getenv('PASSWORD_POSTGRESS')

def get_driver_info():
    # Connessione al database
    count = 0
    conn = psycopg2.connect(
        host=HOST_POSTGRESS,
        port=PORT_POSTGRESS,
        database=DB_POSTGRESS,
        user=USER_POSTGRESS,
        password=PASSWORD_POSTGRESS,
        sslmode='require'
    )
    cur = conn.cursor()

    # Prendi tutti i nomi dei piloti F1 di tutti i tempi
    url = 'https://ergast.com/api/f1/drivers.json?limit=10000'
    response = requests.get(url)
    data = response.json()
    drivers = data['MRData']['DriverTable']['Drivers']

    # Prendi tutte le informazioni dei piloti
    for driver in drivers:
        count += 1
        print(count)
        driver_id = driver['driverId']
        given_name = driver['givenName']
        family_name = driver['familyName']
        driver_complete_name = driver['givenName'] + ' ' + driver['familyName']
        driver_nationality = driver['nationality']
        driver_url = driver['url']
        driver_date_of_birth = driver['dateOfBirth']

        # Prendi la biografia da driver_url (Wikipedia)
        try:
            base_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
            parsed_link = urlsplit(driver_url)
            path = parsed_link.path
            filename = os.path.basename(path)
            page_title = os.path.splitext(filename)[0]
            url_wikipedia = base_url + page_title
            response_wikipedia = requests.get(url_wikipedia)
            data_wikipedia = response_wikipedia.json()
            driver_biography = data_wikipedia['extract']
        except:
            driver_biography = ""

        # Prendi le informazioni da url_driver_info
        url_driver_info = 'https://ergast.com/api/f1/drivers/' + driver_id + '/driverStandings.json'
        response_driver_info = requests.get(url_driver_info)
        data_driver_info = response_driver_info.json()

        # Prendi tutte le informazioni da url_driver_info
            
        # Inserisci i dati nel database
        cur.execute("""
            INSERT INTO drivers (id, driver_id, given_name, family_name, complete_name, nationality, url, 
            date_of_birth, biography)
            VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (driver_id) DO UPDATE
            SET given_name = excluded.given_name,
                family_name = excluded.family_name,
                complete_name = excluded.complete_name,
                nationality = excluded.nationality,
                url = excluded.url,
                date_of_birth = excluded.date_of_birth,
                biography = excluded.biography
            RETURNING id;
        """, (driver_id, given_name, family_name, driver_complete_name, driver_nationality, driver_url,
              driver_date_of_birth, driver_biography))
        
        conn.commit()
        new_id = cur.fetchone()[0]
        # Stampa tutte le informazioni sulla console
        print(new_id)
    # Chiudi la connessione al database
    cur.close()
    conn.close()

def check_if_the_table_exist():
    # Controlla se la tabella drivers esiste
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
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'drivers'
        );
    """)
    result = cur.fetchone()
    print(result[0])
    # Se la tabella non esiste, creala
    if result[0] == False:
        cur.execute("""
            CREATE TABLE drivers (
                id SERIAL PRIMARY KEY,
                driver_id VARCHAR(255) UNIQUE,
                given_name VARCHAR(255),
                family_name VARCHAR(255),
                complete_name VARCHAR(255),
                nationality VARCHAR(255),
                url VARCHAR(255),
                date_of_birth DATE,
                biography TEXT
            );

        """)
        conn.commit()
        print("Table 'drivers' created successfully.")

    cur.close()
    conn.close()
    get_driver_info()

def print_driver_ids():
    conn = psycopg2.connect(
        host=HOST_POSTGRESS,
        port=PORT_POSTGRESS,
        database=DB_POSTGRESS,
        user=USER_POSTGRESS,
        password=PASSWORD_POSTGRESS,
        sslmode='require'
    )
    cur = conn.cursor()

    # Esegui una query per ottenere tutti gli ID dei piloti
    cur.execute("SELECT driver_id FROM drivers;")
    rows = cur.fetchall()

    # Stampa gli ID dei piloti
    for row in rows:
        print(row[0])

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
    cur.execute("DROP TABLE drivers;")
    conn.commit()
    print("Table 'drivers' deleted successfully.")
    cur.close()
    conn.close()

check_if_the_table_exist()
#delete_table_drivers()
