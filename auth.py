import bcrypt
import database as db

def hash_password(password):
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(stored_hash, provided_password):
    """Verify a stored password against one provided by user."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))

def register_user(username, email, password):
    """Register a new user."""
    hashed_pw = hash_password(password)
    return db.create_user(username, email, hashed_pw)

def authenticate_user(username, password):
    """Authenticate a user."""
    user = db.get_user_by_username(username)
    if user and verify_password(user['password_hash'], password):
        return user
    return None
