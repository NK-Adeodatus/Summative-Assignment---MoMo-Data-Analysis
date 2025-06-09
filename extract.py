import xml.etree.ElementTree as ET
import sqlite3
import re

# Parse the XML file
tree = ET.parse('modified_sms_v2.xml')
root = tree.getroot()

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('MoMo_SMS.db')
cursor = conn.cursor()

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

def determine_type_of_sms(message):
    print('message:\n',message)
    if re.search(r'You have received', message):
        # print('*1*')
        return 'Incoming Money'
    elif re.search(r'Your payment of', message):
        print('type: Your payment of')
        # print('*2*')
        return 'Payments to Code Holders'
    elif re.search(r'A bank deposit of', message):
        # print('*3*')
        return 'Bank Deposits'
    elif re.search(r'transferred to', message):
        # print('*4*')
        return 'Bank Transfers'
    elif re.search(r'to Airtime', message):
        # print('*5*')
        return 'Airtime Bill Payments'
    elif re.search(r'^<#>', message):
        # print('*6*')
        return 'MoMo Advice'
    elif re.search(r'Cash Power', message):
        # print('*7*')
        return 'Cash Power Bill Payments'
    elif re.search(r'withdrawn', message):
        # print('*8*')
        return 'Withdrawals from Agents'
    elif re.search('Bundles', message):
        # print('*9*')
        return 'Internet and Voice Bundle Purchases'
    else:
        # print('*0*')
        return 'Uncategorized'
    

# Insert data into the database
test = 1
for sms in root.findall('sms'):
    test += 1
    message = sms.get('body')
    id = re.search(r'\s\d{11}\s', message)
    amount = re.search(r'\d{1,3}(?:,\d{3})*|\d+\s*RWF\s', message)
    type_of_sms = determine_type_of_sms(message)
    sender = re.search(r'RWF\sfrom\s[a-zA-Z]*\s[a-zA-Z]*', message)
    receiver = re.search(r'(RWF|transferred)\sto\s([a-zA-Z ]+\s[a-zA-Z ]+)\s\d+', message)
    new_balance = re.search(r'(?i)new\sbalance\s?:(\s?\d{1,3}(?:,\d{3})*|\d+)', message)
    time = re.search(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', message)

    if message:
        amount_match = re.search(r'(\d[\d,]*)\s*RWF', message)
        amount = int(amount_match.group(1).replace(',', '')) if amount_match else None

        new_balance_match = re.search(r'(?i)new\s+balance\s*:\s*(\d[\d,]*)', message)
        new_balance = int(new_balance_match.group(1).replace(',', '')) if new_balance_match else None
        if id:
            id = int(id.group().strip())
        sender = sender.group().replace('RWF from ', '').strip() if sender else None
        receiver = receiver.group(2).strip() if receiver else None
        time = time.group().strip() if time else None
    if test <= 10:
        print('type_of_sms:\n', type_of_sms)

    # Insert the data into the database
    cursor.execute('''
        INSERT INTO sms (type_of_sms, amount, sender, receiver, message, new_balance, time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (type_of_sms, amount, sender, receiver, message, new_balance, time))

conn.commit()