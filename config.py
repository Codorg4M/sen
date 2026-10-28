import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Application configuration settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'rideshare-college-project-secret-key-2026')
    DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'rideshare.db')
    
    # Fare calculation defaults (INR ₹)
    BASE_FARE = 30.0
    RATE_PER_KM = 12.0
    
    # Session configuration
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
