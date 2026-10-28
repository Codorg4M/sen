import re
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db

class User:
    """User model handling authentication and user CRUD operations."""

    @staticmethod
    def validate_registration(name, email, phone, password, confirm_password, role='rider'):
        """Validate user registration inputs."""
        errors = []
        if not name or len(name.strip()) < 2:
            errors.append("Full name must be at least 2 characters.")
        
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not email or not re.match(email_regex, email.strip()):
            errors.append("Please enter a valid email address.")
            
        phone_clean = re.sub(r'[\s\-\+]', '', phone or '')
        if not phone_clean.isdigit() or len(phone_clean) < 10 or len(phone_clean) > 15:
            errors.append("Please enter a valid phone number (10 to 15 digits).")
            
        if not password or len(password) < 6:
            errors.append("Password must be at least 6 characters long.")
            
        if password != confirm_password:
            errors.append("Passwords do not match.")
            
        if role not in ('rider', 'driver', 'admin'):
            errors.append("Invalid user role specified.")
            
        return errors

    @staticmethod
    def find_by_email(email):
        """Fetch user by email (case-insensitive)."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email.strip(),))
        return cursor.fetchone()

    @staticmethod
    def find_by_id(user_id):
        """Fetch user by ID."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

    @staticmethod
    def create(name, email, phone, password, role='rider'):
        """Create a new user with securely hashed password."""
        db = get_db()
        cursor = db.cursor()
        password_hash = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO users (name, email, phone, password_hash, role, status)
            VALUES (?, ?, ?, ?, ?, 'active')
        """, (name.strip(), email.strip().lower(), phone.strip(), password_hash, role))
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def authenticate(email, password):
        """Verify user credentials."""
        user = User.find_by_email(email)
        if not user:
            return None, "Invalid email or password."
        if user['status'] != 'active':
            return None, "Your account is deactivated. Please contact administrator."
        if not check_password_hash(user['password_hash'], password):
            return None, "Invalid email or password."
        return user, None

    @staticmethod
    def update_profile(user_id, name, email, phone):
        """Update basic user profile details."""
        db = get_db()
        cursor = db.cursor()
        
        # Check if email is already taken by another user
        cursor.execute("SELECT id FROM users WHERE LOWER(email) = LOWER(?) AND id != ?", (email.strip(), user_id))
        if cursor.fetchone():
            return False, "This email is already in use by another account."
            
        cursor.execute("""
            UPDATE users SET name = ?, email = ?, phone = ?
            WHERE id = ?
        """, (name.strip(), email.strip().lower(), phone.strip(), user_id))
        db.commit()
        return True, "Profile updated successfully."

    @staticmethod
    def get_all(role=None):
        """Fetch all users, optionally filtered by role."""
        db = get_db()
        cursor = db.cursor()
        if role:
            cursor.execute("SELECT * FROM users WHERE role = ? ORDER BY created_at DESC", (role,))
        else:
            cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        return cursor.fetchall()

    @staticmethod
    def toggle_status(user_id):
        """Toggle user status between active and inactive (Admin operation)."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT status FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            return False, "User not found."
        new_status = 'inactive' if user['status'] == 'active' else 'active'
        cursor.execute("UPDATE users SET status = ? WHERE id = ?", (new_status, user_id))
        db.commit()
        return True, f"User status changed to {new_status}."
