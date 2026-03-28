from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"   # 🔐 Needed for session

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database1.db")

# -----------------------------
# Initialize Database
# -----------------------------
def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            doctor TEXT,
            date TEXT,
            time TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# -----------------------------
# Dummy Login Credentials
# -----------------------------
USERNAME = "admin"
PASSWORD = "1234"

# -----------------------------
# Doctor List
# -----------------------------
doctors = ["Dr. Smith", "Dr. John", "Dr. Meena", "Dr. Kumar"]

# -----------------------------
# Home Page
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html', doctors=doctors)

# -----------------------------
# LOGIN
# -----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')

        if user == USERNAME and pwd == PASSWORD:
            session['logged_in'] = True
            return redirect('/appointments')
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

# -----------------------------
# LOGOUT
# -----------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# -----------------------------
# Book Appointment
# -----------------------------
@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    phone = request.form['phone']
    doctor = request.form['doctor']
    date = request.form['date']
    time = request.form['time']

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Prevent double booking
    c.execute("SELECT * FROM appointments WHERE doctor=? AND date=? AND time=?",
              (doctor, date, time))

    if c.fetchone():
        conn.close()
        return "<h3 style='color:red;text-align:center;'>❌ Slot already booked!</h3>"

    c.execute("INSERT INTO appointments (name, phone, doctor, date, time) VALUES (?,?,?,?,?)",
              (name, phone, doctor, date, time))

    conn.commit()
    conn.close()

    return render_template('success.html', name=name, doctor=doctor, date=date, time=time)

# -----------------------------
# Protected Appointments Page
# -----------------------------
@app.route('/appointments')
def appointments():
    # 🔐 Check login
    if not session.get('logged_in'):
        return redirect('/login')

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT * FROM appointments")
    data = c.fetchall()

    conn.close()

    return render_template('appointments.html', appointments=data)

# -----------------------------
# Run App
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)