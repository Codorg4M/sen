import sqlite3
import os
from flask import g, current_app
from werkzeug.security import generate_password_hash
from datetime import date, timedelta

def get_db():
    """Get database connection for current request context."""
    if 'db' not in g:
        db_path = current_app.config.get('DATABASE_PATH')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        # Enable SQLite Foreign Keys
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db

def close_db(e=None):
    """Close database connection at request teardown."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    """Initialize database tables using schema.sql and seed demo data."""
    with app.app_context():
        db = get_db()
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            db.cursor().executescript(f.read())
        db.commit()
        seed_demo_data(db)

def seed_demo_data(db):
    """Seed sample/demo accounts and rides if the database is newly initialized."""
    cursor = db.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        return

    # 1. Seed Demo Admin
    admin_hash = generate_password_hash("Admin@123")
    cursor.execute("""
        INSERT INTO users (name, email, phone, password_hash, role, status)
        VALUES (?, ?, ?, ?, 'admin', 'active')
    """, ("System Admin", "admin@demo.com", "9876543210", admin_hash))

    # 2. Seed Demo Driver
    driver_hash = generate_password_hash("Driver@123")
    cursor.execute("""
        INSERT INTO users (name, email, phone, password_hash, role, status)
        VALUES (?, ?, ?, ?, 'driver', 'active')
    """, ("Demo Driver (Rahul Sharma)", "driver@demo.com", "9812345678", driver_hash))
    driver1_user_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO drivers (user_id, license_number, vehicle_type, vehicle_model, vehicle_number, total_seats)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (driver1_user_id, "DL-0420180012345", "Sedan", "Honda City", "DL-03-AB-1020", 4))
    driver1_id = cursor.lastrowid

    # 3. Seed Second Driver
    driver2_hash = generate_password_hash("Driver@123")
    cursor.execute("""
        INSERT INTO users (name, email, phone, password_hash, role, status)
        VALUES (?, ?, ?, ?, 'driver', 'active')
    """, ("Priya Patel (Driver)", "driver2@demo.com", "9823456789", driver2_hash))
    driver2_user_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO drivers (user_id, license_number, vehicle_type, vehicle_model, vehicle_number, total_seats)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (driver2_user_id, "MH-0120190098765", "Hatchback", "Hyundai i20", "MH-02-XY-9080", 4))
    driver2_id = cursor.lastrowid

    # 4. Seed Demo Rider
    rider_hash = generate_password_hash("Rider@123")
    cursor.execute("""
        INSERT INTO users (name, email, phone, password_hash, role, status)
        VALUES (?, ?, ?, ?, 'rider', 'active')
    """, ("Demo Rider (Aman Verma)", "rider@demo.com", "9898765432", rider_hash))
    rider_id = cursor.lastrowid

    # 5. Seed Second Rider
    cursor.execute("""
        INSERT INTO users (name, email, phone, password_hash, role, status)
        VALUES (?, ?, ?, ?, 'rider', 'active')
    """, ("Sneha Rao (Rider)", "rider2@demo.com", "9871234567", rider_hash))
    rider2_id = cursor.lastrowid

    # Dates for realistic scheduling
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    # 6. Seed Demo Rides (Section 22 Requirements)
    # Ride 1: College Road -> Railway Station
    cursor.execute("""
        INSERT INTO rides (driver_id, pickup_location, destination, ride_date, departure_time, available_seats, vehicle_type, fare_per_passenger, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (driver1_id, "College Road", "Railway Station", tomorrow, "09:30", 3, "Sedan", 100.0, "Available"))
    ride1_id = cursor.lastrowid

    # Ride 2: Bus Stand -> City Center
    cursor.execute("""
        INSERT INTO rides (driver_id, pickup_location, destination, ride_date, departure_time, available_seats, vehicle_type, fare_per_passenger, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (driver2_id, "Bus Stand", "City Center", tomorrow, "14:00", 2, "Hatchback", 80.0, "Available"))
    ride2_id = cursor.lastrowid

    # Ride 3: Tech Park -> Airport
    cursor.execute("""
        INSERT INTO rides (driver_id, pickup_location, destination, ride_date, departure_time, available_seats, vehicle_type, fare_per_passenger, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (driver1_id, "Tech Park", "Airport", today, "18:00", 4, "Sedan", 350.0, "Available"))
    ride3_id = cursor.lastrowid

    # Ride 4: Completed Ride (for ride history demonstration)
    cursor.execute("""
        INSERT INTO rides (driver_id, pickup_location, destination, ride_date, departure_time, available_seats, vehicle_type, fare_per_passenger, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (driver1_id, "University Campus", "Central Mall", yesterday, "11:00", 2, "Sedan", 90.0, "Completed"))
    ride4_id = cursor.lastrowid

    # 7. Seed Demo Bookings
    # A Completed booking for Rider 1 on Ride 4
    cursor.execute("""
        INSERT INTO bookings (ride_id, rider_id, seats_requested, total_fare, status)
        VALUES (?, ?, ?, ?, ?)
    """, (ride4_id, rider_id, 1, 90.0, "Completed"))

    # A Pending booking on Ride 1 (so driver sees a pending request right away on first login!)
    cursor.execute("""
        INSERT INTO bookings (ride_id, rider_id, seats_requested, total_fare, status)
        VALUES (?, ?, ?, ?, ?)
    """, (ride1_id, rider2_id, 1, 100.0, "Pending"))

    db.commit()
