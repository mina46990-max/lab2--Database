# DB Lab 2 - Login & To-Do Application

## Team
| Name | ID | Contribution |
|------|----|--------------|
| (your name) | (your ID) | (what you did) |

## Technology
- Back end: Python 3 + Flask, PyMySQL (plain SQL, no ORM), bcrypt
- Front end: HTML, CSS (flexbox, media query), vanilla JavaScript
- Database: MySQL

## How to run
1. Install Python 3.10+ and MySQL Server.
2. Create the database: `mysql -u root -p < database/schema.sql`
3. Create a virtual environment and install packages:
   ```
   python -m venv venv
   venv\Scripts\activate        # Windows  (Linux/Mac: source venv/bin/activate)
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your MySQL password and a random `SECRET_KEY`.
5. Start the server: `python app.py`
6. Open http://127.0.0.1:5000

## Features
R1 register (duplicate email message, auto login) - R2 login/logout with one generic error - R3 private list - R4 add - R5 edit - R6 mark done/open - R7 delete with confirmation - R8 validation in browser and on server with the exact messages - R9 bcrypt hashes, parameterized queries, user_id from the session - R10 responsive consistent UI with empty state and feedback.

## Screenshots
See the `screenshots/` folder: register with errors, login, list with a done item, phone-sized window.

## Answers
**(a)** `AND user_id = ?` makes the statement affect only rows owned by the logged-in user. The to-do id comes from the browser, so without it any user could edit or delete another user's to-dos by sending their id.

**(b)** MySQL rejects the insert with a foreign key error (1452). This is referential integrity: a foreign key value must match an existing primary key in the referenced table.

**(c)** If the database leaks, plain passwords would be exposed. A bcrypt hash is one-way, salted and slow, so passwords cannot be read back and are very hard to brute-force.

**(d)** `NOT NULL` only rejects NULL. An empty string `''` is a value, so MySQL accepts it. Only our own check (trim and test for empty) can refuse an empty name.
