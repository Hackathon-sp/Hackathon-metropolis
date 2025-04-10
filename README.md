# Hotel Reservation Email Parser 🏨📩

This project automatically reads hotel reservation emails, extracts relevant booking information using the Gemini API, and creates reservations in the system by matching addresses with a local database (SQLite or Aurora MySQL). It also sends a confirmation email to the customer.

---


## 🚀 How It Works

1. Connects to your email inbox via IMAP.
2. Detects new, unread emails.
3. Uses Google Gemini to extract structured reservation info from raw email text.
4. Matches the reservation address with known locations using:
   - SQLite (local `hotel.db`)
   - MySQL (via latitude/longitude)
5. Creates a reservation.
6. Sends a confirmation email with reservation details.

---

## 🧪 How to Run

### 1. Clone the repo
```
git clone https://github.com/Hackathon-sp/Hackathon-metropolis.git
```

### 2. Create a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Create a `.env` file
```
EMAIL_HOST=imap.gmail.com
EMAIL_USER=your-email@example.com
EMAIL_PASS=your-app-password

GENAI_API_KEY=your-gemini-api-key

DB_HOST=your-aurora-host
DB_USER=your-db-username
DB_PASSWORD=your-db-password

SMTP_PASS=your-smtp-password
```

### 5. Run the script
```
python main.py
```

It will continuously check for new emails every 10 seconds.

---


## ✨ Features

- ✅ Reads emails via IMAP  
- ✅ Parses natural language email content with Gemini  
- ✅ Matches locations intelligently via address or lat/long  
- ✅ Sends branded confirmation emails  
- ✅ SQLite +MySQL integration  


