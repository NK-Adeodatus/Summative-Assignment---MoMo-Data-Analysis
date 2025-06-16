import sqlite3
from extract import extract_sms
from api import run_app
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, 'MoMo_SMS.db')

# Check if the data has already been extracted from the XML file to the dadabase
def check_extraction():
    print('check run')
    if not os.path.exists(DB_PATH):
        extract_sms()
        return
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM sms')
        count = cursor.fetchone()[0]
        conn.close()
        if count == 0:
            extract_sms()
    except sqlite3.Error as e:
        print("SQLite error:", e)
        extract_sms()

if __name__ == '__main__':
    check_extraction()
    run_app()
