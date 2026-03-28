# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 23:43:14 2026

@author: meena
"""

import sqlite3
import os

db_path = r"E:/2024/2025/2026/doctor/database1.db"

# Force new database creation
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("""
CREATE TABLE appointments (
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

print("New database created successfully")