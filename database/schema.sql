-- ====================================================================
-- RideShare Database Schema (SQLite / Relational SQL)
-- Software Engineering Mini Project
-- ====================================================================

PRAGMA foreign_keys = ON;

-- 1. USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('rider', 'driver', 'admin')),
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'inactive')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. DRIVERS TABLE (1-to-1 with USERS for driver role)
CREATE TABLE IF NOT EXISTS drivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    license_number TEXT NOT NULL UNIQUE,
    vehicle_type TEXT NOT NULL,
    vehicle_model TEXT NOT NULL,
    vehicle_number TEXT NOT NULL UNIQUE,
    total_seats INTEGER NOT NULL CHECK(total_seats > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. RIDES TABLE (1-to-Many: Driver -> Rides)
CREATE TABLE IF NOT EXISTS rides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_id INTEGER NOT NULL,
    pickup_location TEXT NOT NULL,
    destination TEXT NOT NULL,
    ride_date TEXT NOT NULL,
    departure_time TEXT NOT NULL,
    available_seats INTEGER NOT NULL CHECK(available_seats >= 0),
    vehicle_type TEXT NOT NULL,
    fare_per_passenger REAL NOT NULL CHECK(fare_per_passenger >= 0),
    status TEXT NOT NULL DEFAULT 'Available' CHECK(status IN ('Available', 'Full', 'Ongoing', 'Completed', 'Cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE
);

-- 4. BOOKINGS TABLE (Many-to-Many link between Users/Riders and Rides)
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ride_id INTEGER NOT NULL,
    rider_id INTEGER NOT NULL,
    seats_requested INTEGER NOT NULL CHECK(seats_requested > 0),
    total_fare REAL NOT NULL CHECK(total_fare >= 0),
    status TEXT NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending', 'Accepted', 'Rejected', 'Cancelled', 'Completed')),
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ride_id) REFERENCES rides(id) ON DELETE CASCADE,
    FOREIGN KEY (rider_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indices for performance and search optimization
CREATE INDEX IF NOT EXISTS idx_rides_search ON rides(pickup_location, destination, ride_date, status);
CREATE INDEX IF NOT EXISTS idx_bookings_rider ON bookings(rider_id, status);
CREATE INDEX IF NOT EXISTS idx_bookings_ride ON bookings(ride_id, status);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
