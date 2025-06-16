# 📱 MoMo SMS Analyzer

A fullstack web application for parsing, categorizing, and analyzing Mobile Money (MoMo) SMS messages. Users can search and filter transaction messages such as incoming money, withdrawals, bank deposits, and more.

---

## 🔍 Features

- Extracts and parses SMS messages from an XML file.
- Classifies SMS messages into categories (e.g., Incoming Money, Transfers, Airtime).
- Stores processed and unprocessed messages into SQLite databases.
- Provides a RESTful API to serve the SMS data.
- Offers a user-friendly frontend to visualize, search, and filter messages.

---

## 🗂️ Project Structure
```text
MoMo-SMS-Analyzer/
│
├── backend/
│ ├── app.py # ✅ Entry point – runs extraction & launches Flask API
│ ├── api.py # Flask app serving JSON API and static HTML
│ ├── extract.py # Parses XML and stores categorized SMS in database
│ ├── MoMo_SMS.db # Processed SMS database (auto-generated)
│ └── modified_sms_v2.xml # Input file containing SMS messages
│
├── front_end/
│ ├── index.html # Frontend UI with filters and display
│ ├── style.css # App styling
│ └── script.js # Fetches, displays, and filters messages
│
├── Unprocessed_SMS.db # Unrecognized messages database (auto-generated)
└── README.md
```


---

## ⚙️ Technologies Used

- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: Python, Flask, SQLite3, ElementTree (for XML)
- **Architecture**: REST API

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/NK-Adeodatus/Summative-Assignment---MoMo-Data-Analysis
cd MoMo-SMS-Analyzer/backend
```
### 2. Install Dependencies
Make sure Flask is installed.
```bash
pip install flask
```
### 3. Run the Backend
Make sure modified_sms_v2.xml is in the backend directory.
```bash
python app.py
```

- This will:
    - Parse and categorize the SMS XML file
    - Store the data in MoMo_SMS.db
    - Launch the Flask development server

### 4. View the Frontend
Once the backend is running, open your browser and navigate to:
```cpp
http://127.0.0.1:5000/
```

## 🔧 How It Works
### SMS Extraction (extract.py)

- Parses modified_sms_v2.xml and categorizes messages.
- Stores structured data in MoMo_SMS.db.
- Uncategorized messages are saved to Unprocessed_SMS.db at the root directory(Summative_MoMo_data_analysis/).

### Flask API (api.py)

- Serves static frontend files (index.html).
- API Endpoint /api/sms returns all processed SMS as JSON.

### Frontend (front_end/)

- Fetches messages from the API.
- Allows search and filter by:
    - Type of SMS
    - Amount range
    - Date
- Messages are displayed with collapsible full content.

## 📂 Databases

- MoMo_SMS.db: Stores SMS with extracted fields like amount, sender, receiver, etc.
- Unprocessed_SMS.db: Stores messages that couldn’t be categorized.
