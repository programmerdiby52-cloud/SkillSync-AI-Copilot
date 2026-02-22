import sqlite3
import os
from contextlib import contextmanager

DB_PATH = 'skillsync.db'

@contextmanager
def get_db_connection():
    """Context manager for SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()

def init_db():
    """Initialize the SQLite database with required tables."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                xp INTEGER DEFAULT 0,
                streak INTEGER DEFAULT 0,
                last_login DATE,
                level TEXT DEFAULT 'Novice',
                soft_skills_score INTEGER DEFAULT 0
            )
        ''')
        
        # User Modules (for RAG / Custom Modules)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                module_name TEXT NOT NULL,
                content TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Diagnostic Scores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diagnostic_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                score INTEGER NOT NULL,
                max_score INTEGER NOT NULL,
                taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Study Analytics (Burnout & Focus)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_date DATE NOT NULL,
                duration_minutes INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

def get_user_by_username(username):
    """Fetch user details by username."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return cursor.fetchone()

def create_user(username, email, password_hash):
    """Create a new user."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username, email, password_hash))
            return True
    except sqlite3.IntegrityError:
        return False # Username or email already exists

def update_user_xp(user_id, xp_to_add):
    """Add XP to a user and calculate level."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT xp, level FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        if not row: return
        
        new_xp = row['xp'] + xp_to_add
        new_level = 'Novice'
        if new_xp >= 1000:
            new_level = 'Architect'
        elif new_xp >= 500:
            new_level = 'Developer'
            
        cursor.execute('''
            UPDATE users SET xp = ?, level = ? WHERE id = ?
        ''', (new_xp, new_level, user_id))

def update_streak(user_id, last_login_date):
    """Update logic for streak (simplified for now)."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # In a real app, calculate days difference from last_login
        # For simplicity, increment streak here. 
        cursor.execute('UPDATE users SET streak = streak + 1, last_login = ? WHERE id = ?', (last_login_date, user_id))

def update_password(user_id, new_password_hash):
    """Update user password."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_password_hash, user_id))
