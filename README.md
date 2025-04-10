# Hackathon-metropolis

# Hotel Reservation Email Parser 🏨📩

This project automatically reads hotel reservation emails, extracts relevant booking information using the Gemini API, and creates reservations in the system by matching addresses with a local database (SQLite or Aurora MySQL). It also sends a confirmation email to the customer.

---

## 🚀 How It Works

1. Connects to your email inbox via IMAP.
2. Detects new, unread emails.
3. Uses Google Gemini to extract structured reservation info from raw email text.
4. Matches the reservation address with known locations using:
   - SQLite (local `hotel.db`)
   - Aurora MySQL (via latitude/longitude)
5. Creates a reservation.
6. Sends a confirmation email with reservation details.
