from flask import Flask, jsonify, make_response 
import sqlite3
from extract import extract_sms
import os


app = Flask(__name__)


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, 'MoMo_SMS.db')

# Get the sms data from the database
def get_all_sms():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT type_of_sms, amount, sender, receiver, message, new_balance, time FROM sms LIMIT 5')
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

# serve the data from database in json format.
@app.route('/api/sms', methods=['GET'])
def api_sms():
    response = make_response(jsonify(get_all_sms()))
    response.headers['Access-Control-Allow-Origin'] = '*' 
    return response
    # return jsonify(get_all_sms())

def run_app():
    app.run(debug=True)

