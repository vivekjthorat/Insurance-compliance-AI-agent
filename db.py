import sqlite3
import os
from datetime import datetime

DB_PATH = 'insurance_agent.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Documents table
    c.execute('''CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        upload_time TEXT NOT NULL
    )''')
    # Metadata table
    c.execute('''CREATE TABLE IF NOT EXISTS metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_id INTEGER,
        field_name TEXT,
        field_value TEXT,
        FOREIGN KEY(doc_id) REFERENCES documents(id)
    )''')
    # Validations table
    c.execute('''CREATE TABLE IF NOT EXISTS validations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_id INTEGER,
        status TEXT,
        errors TEXT,
        validation_time TEXT NOT NULL,
        FOREIGN KEY(doc_id) REFERENCES documents(id)
    )''')
    conn.commit()
    conn.close()

def save_upload(filename):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO documents (filename, upload_time) VALUES (?, ?)', (filename, upload_time))
    doc_id = c.lastrowid
    conn.commit()
    conn.close()
    return doc_id

def save_metadata(doc_id, fields_dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for field, value in fields_dict.items():
        c.execute('INSERT INTO metadata (doc_id, field_name, field_value) VALUES (?, ?, ?)', (doc_id, field, str(value)))
    conn.commit()
    conn.close()

def save_validation(doc_id, status, errors_list):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    validation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    errors = '\n'.join(errors_list) if errors_list else ''
    c.execute('INSERT INTO validations (doc_id, status, errors, validation_time) VALUES (?, ?, ?, ?)',
              (doc_id, status, errors, validation_time))
    conn.commit()
    conn.close() 