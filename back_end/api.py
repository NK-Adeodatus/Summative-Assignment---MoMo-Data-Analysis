from flask import Flask, jsonify, make_response, send_from_directory
import sqlite3
from extract import extract_sms
import os




SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, 'MoMo_SMS.db')
FRONTEND_DIR = os.path.join(SCRIPT_DIR, '../front_end')
FRONTEND_DIR = os.path.abspath(FRONTEND_DIR)

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')

# Get the sms data from the database
def get_all_sms():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT type_of_sms, amount, sender, receiver, message, new_balance, time FROM sms')
    rows = cursor.fetchall()
    conn.close()

    sms_list = [
        {
            'type': row[0],
            'amount': row[1],
            'sender': row[2],
            'receiver': row[3],
            'message': row[4],
            'new_balance': row[5],
            'time': row[6]
        } for row in rows
    ]
    return sms_list

@app.route('/')
def serve_page():
    return send_from_directory(app.static_folder, 'index.html')

# serve the data from database in json format.
@app.route('/api/sms', methods=['GET'])
def api_sms():
    response = make_response(jsonify(get_all_sms()))
    response.headers['Access-Control-Allow-Origin'] = '*' 
    return response
    # return jsonify(get_all_sms())

def run_app():
    app.run(debug=True)

