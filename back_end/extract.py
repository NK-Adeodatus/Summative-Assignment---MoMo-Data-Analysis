import xml.etree.ElementTree as ET
import sqlite3
import re
import os

def determine_type_of_sms(message):
    if re.search(r'You have received', message):
        return 'Incoming Money'
    elif re.search(r'A bank deposit of', message):
        return 'Bank Deposits'
    elif re.search(r'transferred to', message):
        return 'Transfers to Mobile Numbers'
    elif re.search(r'to Airtime', message):
        return 'Airtime Bill Payments'
    elif re.search(r'Your payment of', message):
        return 'Payments to Code Holders'
    elif re.search(r'DEPOSIT RWF|You have transferred', message):
        return 'Bank Transfers'
    elif re.search(r'transaction of', message):
        return 'Transactions Initiated by Third Parties'
    elif re.search(r'Cash Power', message):
        return 'Cash Power Bill Payments'
    elif re.search(r'withdrawn', message):
        return 'Withdrawals from Agents'
    elif re.search('Bundles', message):
        return 'Internet and Voice Bundle Purchases'
    else:
        return 'Uncategorized'

def extract_sms():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    xml_file = os.path.join(script_dir, 'modified_sms_v2.xml')
    db_file = os.path.join(script_dir, 'MoMo_SMS.db')
    unprocessed_db = os.path.join(script_dir, '../Unprocessed_SMS.db')

    # Parse the XML file
    tree = ET.parse(xml_file)
    if tree:
        print('tree is available')
    root = tree.getroot()

    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_file)
    conn_unprocessed = sqlite3.connect(unprocessed_db)
    cursor = conn.cursor()
    cursor_unprocessed = conn_unprocessed.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_of_sms TEXT,
            amount INTEGER,
            sender TEXT,
            receiver TEXT,
            message TEXT,
            new_balance INTEGER,
            time TEXT
            )
            ''')
    
    cursor_unprocessed.execute('''
        CREATE TABLE IF NOT EXISTS unprocessed_sms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            date TEXT
        )
    ''')

    # Insert data into the database
    for sms in root.findall('sms'):
        message = sms.get('body')
        if message == None:
            return
        time = re.search(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', message)
        time = time.group().strip() if time else None
        type_of_sms = determine_type_of_sms(message)
        if type_of_sms == 'Uncategorized':
            cursor_unprocessed.execute('''
                INSERT INTO unprocessed_sms (message, date)
                VALUES (?, ?)
            ''', (message, time))
        else:
            amount = re.search(r'\d{1,3}(?:,\d{3})*|\d+\s*RWF\s', message)
            sender = re.search(r'RWF\sfrom\s[a-zA-Z]*\s[a-zA-Z]*', message)
            new_balance = re.search(r'(?i)new\sbalance\s?:(\s?\d{1,3}(?:,\d{3})*|\d+)', message)

            amount_match = re.search(r'(\d[\d,]*)\s*RWF', message)
            amount = int(amount_match.group(1).replace(',', '')) if amount_match else None

            new_balance_match = re.search(r'(?i)new\s+balance\s*:\s*(\d[\d,]*)', message)
            new_balance = int(new_balance_match.group(1).replace(',', '')) if new_balance_match else None
            sender = sender.group().replace('RWF from ', '').strip() if sender else None

            receiver = None
            receiver_match = re.search(r'Your payment of.*RWF to ([A-Z][a-z]+ [A-Z][a-z]+)', message)
            if not receiver_match:
                receiver_match = re.search(r'transferred to ([A-Z][a-z]+ [A-Z][a-z]+)', message)
            receiver = receiver_match.group(1).strip() if receiver_match else None
            cursor.execute('''
                INSERT INTO sms (type_of_sms, amount, sender, receiver, message, new_balance, time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (type_of_sms, amount, sender, receiver, message, new_balance, time))
    conn.commit()
    conn_unprocessed.commit()
    conn.close()
    conn_unprocessed.close()
