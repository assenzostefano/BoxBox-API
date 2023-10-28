import os

import fastf1
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify

fastf1.Cache.enable_cache('cache')  # optionally change cache location

app = Flask(__name__)

load_dotenv()

HOST_POSTGRESS = os.getenv('HOST_POSTGRESS')
PORT_POSTGRESS = os.getenv('PORT_POSTGRESS')
DB_POSTGRESS = os.getenv('DBNAME_POSTGRESS')
USER_POSTGRESS = os.getenv('USER_POSTGRESS')
PASSWORD_POSTGRESS = os.getenv('PASSWORD_POSTGRESS')

conn = psycopg2.connect(
    host=HOST_POSTGRESS,
    port=PORT_POSTGRESS,
    dbname=DB_POSTGRESS,
    user=USER_POSTGRESS,
    password=PASSWORD_POSTGRESS,
    sslmode='require'
)


@app.route('/api/driver/id/<driver_id>')
def get_circuit(driver_id):
    # Connettiti al database prendi le informazioni del pilota e mostrale in JSON
    conn = psycopg2.connect(
        host=HOST_POSTGRESS,
        port=PORT_POSTGRESS,
        database=DB_POSTGRESS,
        user=USER_POSTGRESS,
        password=PASSWORD_POSTGRESS,
        sslmode='require'
    )
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM drivers WHERE driver_id = '{driver_id}'")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        ID = row[0]
        driver_id = row[1]
        driver_name = row[2]
        driver_surname = row[3]
        driver_complete_name = row[4]
        driver_nationality = row[5]
        driver_url = row[6]
        driver_date_of_birth = row[7]
        driver_description = row[8]

        return_json = {
            'ID': ID,
            'Driver ID': driver_id,
            'Name': driver_name,
            'Surname': driver_surname,
            'Complete Name': driver_complete_name,
            'Nnationality': driver_nationality,
            'Url': driver_url,
            'Date of birth': driver_date_of_birth,
            'Description': driver_description
        }
        return jsonify(return_json)
    else:
        return "Driver not found"


@app.route('/api/driver/name/<driver_name>')
def get_driver_by_name(driver_name):
    # Connettiti al database prendi le informazioni del pilota e mostrale in JSON
    conn = psycopg2.connect(
        host=HOST_POSTGRESS,
        port=PORT_POSTGRESS,
        database=DB_POSTGRESS,
        user=USER_POSTGRESS,
        password=PASSWORD_POSTGRESS,
        sslmode='require'
    )
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM drivers WHERE given_name = '{driver_name}'")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        ID = row[0]
        driver_id = row[1]
        driver_name = row[2]
        driver_surname = row[3]
        driver_complete_name = row[4]
        driver_nationality = row[5]
        driver_url = row[6]
        driver_date_of_birth = row[7]
        driver_description = row[8]

        return_json = {
            'ID': ID,
            'Driver ID': driver_id,
            'Name': driver_name,
            'Surname': driver_surname,
            'Complete Name': driver_complete_name,
            'Nnationality': driver_nationality,
            'Url': driver_url,
            'Date of birth': driver_date_of_birth,
            'Description': driver_description
        }
        return jsonify(return_json)
    else:
        return "Driver not found"


@app.route('/api/driver/surname/<driver_surname>')
def get_driver_by_surname(driver_surname):
    # Connettiti al database prendi le informazioni del pilota e mostrale in JSON
    conn = psycopg2.connect(
        host=HOST_POSTGRESS,
        port=PORT_POSTGRESS,
        database=DB_POSTGRESS,
        user=USER_POSTGRESS,
        password=PASSWORD_POSTGRESS,
        sslmode='require'
    )
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM drivers WHERE family_name = '{driver_surname}'")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        ID = row[0]
        driver_id = row[1]
        driver_name = row[2]
        driver_surname = row[3]
        driver_complete_name = row[4]
        driver_nationality = row[5]
        driver_url = row[6]
        driver_date_of_birth = row[7]
        driver_description = row[8]

        return_json = {
            'ID': ID,
            'Driver ID': driver_id,
            'Name': driver_name,
            'Surname': driver_surname,
            'Complete Name': driver_complete_name,
            'Nnationality': driver_nationality,
            'Url': driver_url,
            'Date of birth': driver_date_of_birth,
            'Description': driver_description
        }
        return jsonify(return_json)
    else:
        return "Driver not found"


@app.route('/api/driver/complete_name/<driver_complete_name>')
def get_driver_by_complete_name(driver_complete_name):
    # Connettiti al database prendi le informazioni del pilota e mostrale in JSON
    conn = psycopg2.connect(
        host=HOST_POSTGRESS,
        port=PORT_POSTGRESS,
        database=DB_POSTGRESS,
        user=USER_POSTGRESS,
        password=PASSWORD_POSTGRESS,
        sslmode='require'
    )
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM drivers WHERE complete_name = '{driver_complete_name}'")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        ID = row[0]
        driver_id = row[1]
        driver_name = row[2]
        driver_surname = row[3]
        driver_complete_name = row[4]
        driver_nationality = row[5]
        driver_url = row[6]
        driver_date_of_birth = row[7]
        driver_description = row[8]

        return_json = {
            'ID': ID,
            'Driver ID': driver_id,
            'Name': driver_name,
            'Surname': driver_surname,
            'Complete Name': driver_complete_name,
            'Nnationality': driver_nationality,
            'Url': driver_url,
            'Date of birth': driver_date_of_birth,
            'Description': driver_description
        }
        return jsonify(return_json)
    else:
        return "Driver not found"


@app.route('/api/circuit/complete_name/<circuit_name>')
def get_circuit_by_name(circuit_name):
    # Connettiti al database prendi le informazioni del pilota e mostrale in JSON
    conn = psycopg2.connect(
        host=HOST_POSTGRESS,
        port=PORT_POSTGRESS,
        database=DB_POSTGRESS,
        user=USER_POSTGRESS,
        password=PASSWORD_POSTGRESS,
        sslmode='require'
    )
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM circuits WHERE circuit_name = '{circuit_name}'")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        ID = row[0]
        circuit_id = row[1]
        circuit_locality = row[2]
        circuit_country = row[3]
        circuit_latitude = row[4]
        circuit_longitude = row[5]
        circuit_url = row[6]
        circuit_years_used = row[7]
        # Separate driver_date_of_birth
        circuit_years_used = circuit_years_used.split(',')
        return_json = {
            'ID': ID,
            'Name': circuit_id,
            'Locality': circuit_locality,
            'Country': circuit_country,
            'Latitude': circuit_latitude,
            'Longitude': circuit_longitude,
            'Url': circuit_url,
            'Years use': circuit_years_used
        }
        return jsonify(return_json)
    else:
        return "Circuit not found"


@app.route('/api/circuit/id/<circuit_id>')
def get_circuit_by_id(circuit_id):
    # Connettiti al database prendi le informazioni del pilota e mostrale in JSON
    conn = psycopg2.connect(
        host=HOST_POSTGRESS,
        port=PORT_POSTGRESS,
        database=DB_POSTGRESS,
        user=USER_POSTGRESS,
        password=PASSWORD_POSTGRESS,
        sslmode='require'
    )
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM circuits WHERE circuit_id = '{circuit_id}'")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        ID = row[0]
        circuit_id = row[1]
        circuit_locality = row[2]
        circuit_country = row[3]
        circuit_latitude = row[4]
        circuit_longitude = row[5]
        circuit_url = row[6]
        circuit_years_used = row[7]
        # Separate driver_date_of_birth
        circuit_years_used = circuit_years_used.split(',')
        return_json = {
            'ID': ID,
            'Name': circuit_id,
            'Locality': circuit_locality,
            'Country': circuit_country,
            'Latitude': circuit_latitude,
            'Longitude': circuit_longitude,
            'Url': circuit_url,
            'Years use': circuit_years_used
        }
        return jsonify(return_json)
    else:
        return "Circuit not found"


@app.route('/api/circuit/locality/<circuit_locality>')
def get_circuit_by_locality(circuit_locality):
    # Connettiti al database prendi le informazioni del pilota e mostrale in JSON
    conn = psycopg2.connect(
        host=HOST_POSTGRESS,
        port=PORT_POSTGRESS,
        database=DB_POSTGRESS,
        user=USER_POSTGRESS,
        password=PASSWORD_POSTGRESS,
        sslmode='require'
    )
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM circuits WHERE locality = '{circuit_locality}'")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        ID = row[0]
        circuit_id = row[1]
        circuit_locality = row[2]
        circuit_country = row[3]
        circuit_latitude = row[4]
        circuit_longitude = row[5]
        circuit_url = row[6]
        circuit_years_used = row[7]
        # Separate driver_date_of_birth
        circuit_years_used = circuit_years_used.split(',')
        # Show all circuits in the locality
        return_json = {
            'ID': ID,
            'Name': circuit_id,
            'Locality': circuit_locality,
            'Country': circuit_country,
            'Latitude': circuit_latitude,
            'Longitude': circuit_longitude,
            'Url': circuit_url,
            'Years use': circuit_years_used
        }
        return jsonify(return_json)
    else:
        return "Circuit not found"


@app.route('/api/circuit/country/<circuit_country>')
def get_circuit_by_country(circuit_country):
    # Connettiti al database e ottieni le informazioni dei circuiti
    conn = psycopg2.connect(
        host=HOST_POSTGRESS,
        port=PORT_POSTGRESS,
        database=DB_POSTGRESS,
        user=USER_POSTGRESS,
        password=PASSWORD_POSTGRESS,
        sslmode='require'
    )
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM circuits WHERE country = '{circuit_country}'")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if rows:
        circuits = []
        for row in rows:
            ID = row[0]
            circuit_id = row[1]
            circuit_locality = row[2]
            circuit_country = row[3]
            circuit_latitude = row[4]
            circuit_longitude = row[5]
            circuit_url = row[6]
            circuit_years_used = row[7]
            # Separate circuit_years_used
            circuit_years_used = circuit_years_used.split(',')
            circuit_data = {
                'ID': ID,
                'Name': circuit_id,
                'Locality': circuit_locality,
                'Country': circuit_country,
                'Latitude': circuit_latitude,
                'Longitude': circuit_longitude,
                'Url': circuit_url,
                'Years used': circuit_years_used
            }
            circuits.append(circuit_data)

        # Restituisci tutti i circuiti trovati
        return jsonify(circuits)
    else:
        return "Circuits not found"


if __name__ == '__main__':
    app.run(debug=True)