
# DB Lab 2 - Login & To-Do Application

## Team

| Name | ID | Contribution |
|------|----|--------------|
| Mina Hany | 2304072 | Database connection, registration and login |
| Yassin Mohamed | 2304064 | To-Do list operations and SQL queries |
| Abdrahman Mohamed Etman | 2304104 | Front-end design, validation and testing |

## Technology

- Back end: Python 3 + Flask, PyMySQL (plain SQL, no ORM), bcrypt
- Front end: HTML, CSS (flexbox, media query), vanilla JavaScript
- Database: MySQL

## How to run

1. Install Python 3.10+ and MySQL Server.
2. Create the database:

   ```bash
   mysql -u root -p < database/schema.sql
   ```

3. Create a virtual environment and install packages:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

   Linux/Mac activation:

   ```bash
   source venv/bin/activate
   ```

4. Copy `.env.example` to `.env` and fill in your MySQL password and a random `SECRET_KEY`.

5. Start the server:

   ```bash
   python app.py
   ```

6. Open http://127.0.0.1:5000

## Features

- R1: Register with duplicate email message and automatic login.
- R2: Login/logout with one generic error message.
- R3: Private to-do list for each user.
- R4: Add a to-do.
- R5: Edit a to-do.
- R6: Mark a to-do as done or open.
- R7: Delete a to-do with confirmation.
- R8: Browser-side and server-side validation with the exact required messages.
- R9: bcrypt password hashes, parameterized SQL queries, and `user_id` taken from the session.
- R10: Responsive and consistent UI with an empty state and feedback messages.

## Screenshots

See the `screenshots/` folder:

- Registration with errors
- Login page
- To-do list with a completed item
- Phone-sized window

## Answers

**(a) Why do we use `AND user_id = ?`?**

It makes the SQL statement affect only rows owned by the logged-in user. The to-do ID comes from the browser, so without this condition, another user could edit or delete someone else's to-do by sending its ID.

**(b) What happens if we insert a non-existent `user_id`?**

MySQL rejects the insert with foreign key error 1452. This enforces referential integrity: a foreign key value must match an existing primary key in the referenced table.

**(c) Why use bcrypt instead of storing plain passwords?**

If the database leaks, plain passwords would be exposed. A bcrypt hash is one-way, salted, and slow, so passwords cannot be read back directly and are much harder to brute-force.

**(d) Why doesn't `NOT NULL` reject an empty string?**

`NOT NULL` rejects only `NULL`. An empty string (`''`) is still a value, so MySQL accepts it. Application-side validation must trim the input and check whether it is empty.
