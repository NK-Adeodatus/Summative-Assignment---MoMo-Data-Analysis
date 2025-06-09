from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_all_sms():
    conn = sqlite3.connect('MoMo_SMS.db')
    cursor = conn.cursor()

    cursor.execute('SELECT type_of_sms, amount, sender, receiver, message, new_balance, time FROM sms LIMIT 5')
    rows = cursor.fetchall()
    conn.close()

    sms_list = [{'type': row[0], 'amount': row[1], 'sender': row[2], 'receiver': row[3], 'message': row[4], 'new_balance': row[5], 'time': row[6]} for row in rows]
    return sms_list

@app.route('/api/sms', methods=['GET'])
def api_sms():
    return jsonify(get_all_sms)

if __name__ == '__main__':
    app.run(debug=True)

