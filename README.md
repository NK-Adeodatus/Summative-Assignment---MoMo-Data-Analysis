# 📱 MoMo SMS Analyzer

A fullstack web application for parsing, categorizing, and analyzing MTN Mobile Money (MoMo) SMS messages. The app extracts, classifies, and stores structured information from an XML file to the database. The frontend provides a simple and interactive interface for searching, filtering, and exploring messagess, and is connected to the backend via a RESTful API.

---

## 🔍 Features

- Extracts and parses SMS messages from an XML file (`modified_sms_v2.xml`)
- Classifies messages into transaction categories (e.g., Incoming Money, Transfers, Airtime)
- Saves both categorized and uncategorized messages into SQLite databases
- Provides a RESTful API to serve SMS data in JSON format
- Includes a dynamic frontend UI to:
  - Display SMS summaries
  - Filter by type, amount, and date
  - Search message content
  - Expand and collapse full SMS text

---

## 🗂️ Project Structure

```text
MoMo-SMS-Analyzer/
│
├── backend/
│   ├── app.py                  # Entry point – runs SMS extraction and launches Flask Server.
│   ├── api.py                  # Serves the data from database as JSON and frontend.
│   ├── extract.py              # Parses XML and stores categorized SMS in database.
│   ├── MoMo_SMS.db             # Stores structured data extracted from the XML file.
│   └── modified_sms_v2.xml     # XML file containing the SMS messages.
│
├── front_end/
│   ├── index.html              # Frontend UI.
│   ├── style.css               # Styling for the app.
│   └── index.js                # Fetches, displays, and filters SMS messages.
│
├── Unprocessed_SMS.db          # Stores uncategorized messages from the XML file.
└── README.md                   # Project documentation
```


---

## ⚙️ Technologies Used

- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: Python, Flask, SQLite3

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/NK-Adeodatus/Summative-Assignment---MoMo-Data-Analysis
cd MoMo-SMS-Analyzer/backend
```
### 2. Install Dependencies
Make sure Python is installed then install Flask.
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

- Parses modified_sms_v2.xml to extract message details
- Classifies each SMS based on patterns (e.g., "You have received")
- Saves recognized(categorized) messages in MoMo_SMS.db
- Unrecognized(uncategorized) messages go to Unprocessed_SMS.db in the root directory(Summative_MoMo_data_analysis/)

### Flask API (api.py)

- Serves static frontend files (index.html).
- API Endpoint /api/sms returns all processed SMS as JSON.

### Entry point (app.py)

When the app starts, it checks if a database exists and if it has content.
- If the database is missing or has no content:
    - It calls extract.py to:
        - Parse the XML file.
        - Extract and classify the SMS messages.
        - Create the database if it has not been created and store the structured data.
- Once the database is ready, app.py then runs the app.py which serves the extracted data from the database and the index.html in the frontend.

### 💻 Frontend (index.html, index.js, style.css)

- Fetches messages from the API.
- Displays all SMS messages in styled cards
- Allows filtering by:
    - Type (Incoming Money, Airtime, etc.)
    - Amount range
    - Date
- Supports search by message's text content
- SMS cards are expandable to view the full original message

## 📂 Databases

- MoMo_SMS.db: Stores Categorized SMS with extracted fields like type_of_sms, amount, sender, receiver, etc.
- Unprocessed_SMS.db: Stores messages that couldn’t be categorized.
