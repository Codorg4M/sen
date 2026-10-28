from datetime import datetime
from database.db import get_db

class Ride:
    """Ride model handling ride creation, search filters, state transitions and driver rides."""

    VALID_STATUSES = ('Available', 'Full', 'Ongoing', 'Completed', 'Cancelled')

    @staticmethod
    def validate_ride(pickup_location, destination, ride_date, departure_time, available_seats, vehicle_type, fare_per_passenger):
        """Validate ride creation input."""
        errors = []
        if not pickup_location or len(pickup_location.strip()) < 2:
            errors.append("Pickup location cannot be empty.")
            
        if not destination or len(destination.strip()) < 2:
            errors.append("Destination cannot be empty.")
            
        if pickup_location and destination and pickup_location.strip().lower() == destination.strip().lower():
            errors.append("Pickup location and destination cannot be identical.")
            
        if not ride_date:
            errors.append("Ride date is required.")
        else:
            try:
                r_date = datetime.strptime(ride_date.strip(), "%Y-%m-%d").date()
                # College project allows today or future dates
                if r_date < datetime.today().date():
                    errors.append("Ride date cannot be in the past.")
            except ValueError:
                errors.append("Invalid ride date format. Please use YYYY-MM-DD.")
                
        if not departure_time:
            errors.append("Departure time is required.")
            
        try:
            seats = int(available_seats)
            if seats <= 0:
                errors.append("Available seats must be greater than 0.")
        except (ValueError, TypeError):
            errors.append("Available seats must be a valid number.")
            
        try:
            fare = float(fare_per_passenger)
            if fare < 0:
                errors.append("Fare per passenger cannot be negative.")
        except (ValueError, TypeError):
            errors.append("Fare must be a valid number.")
            
        if not vehicle_type:
            errors.append("Please specify a vehicle type.")
            
        return errors

    @staticmethod
    def create(driver_id, pickup_location, destination, ride_date, departure_time, available_seats, vehicle_type, fare_per_passenger):
        """Save new ride to database with status 'Available'."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO rides (
                driver_id, pickup_location, destination, ride_date, departure_time,
                available_seats, vehicle_type, fare_per_passenger, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Available')
        """, (
            driver_id,
            pickup_location.strip(),
            destination.strip(),
            ride_date.strip(),
            departure_time.strip(),
            int(available_seats),
            vehicle_type.strip(),
            float(fare_per_passenger)
        ))
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def find_by_id(ride_id):
        """Fetch ride by ID including driver and vehicle details."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT r.*, 
                   u.name as driver_name, u.phone as driver_phone, u.email as driver_email,
                   d.vehicle_type as registered_vehicle_type, d.vehicle_model, d.vehicle_number, d.license_number
            FROM rides r
            JOIN drivers d ON r.driver_id = d.id
            JOIN users u ON d.user_id = u.id
            WHERE r.id = ?
        """, (ride_id,))
        return cursor.fetchone()

    @staticmethod
    def search(pickup=None, destination=None, ride_date=None, vehicle_type=None, min_seats=1):
        """Search available rides matching criteria (case-insensitive substring search)."""
        db = get_db()
        cursor = db.cursor()
        
        query = """
            SELECT r.*, 
                   u.name as driver_name, u.phone as driver_phone,
                   d.vehicle_model, d.vehicle_number
            FROM rides r
            JOIN drivers d ON r.driver_id = d.id
            JOIN users u ON d.user_id = u.id
            WHERE r.status = 'Available'
              AND r.available_seats >= ?
              AND u.status = 'active'
        """
        params = [int(min_seats) if min_seats else 1]

        if pickup and pickup.strip():
            query += " AND LOWER(r.pickup_location) LIKE LOWER(?)"
            params.append(f"%{pickup.strip()}%")

        if destination and destination.strip():
            query += " AND LOWER(r.destination) LIKE LOWER(?)"
            params.append(f"%{destination.strip()}%")

        if ride_date and ride_date.strip():
            query += " AND r.ride_date = ?"
            params.append(ride_date.strip())

        if vehicle_type and vehicle_type.strip() and vehicle_type.strip().lower() != 'all':
            query += " AND LOWER(r.vehicle_type) = LOWER(?)"
            params.append(vehicle_type.strip())

        query += " ORDER BY r.ride_date ASC, r.departure_time ASC"
        cursor.execute(query, tuple(params))
        return cursor.fetchall()

    @staticmethod
    def get_by_driver(driver_id, status=None):
        """Fetch all rides created by a specific driver."""
        db = get_db()
        cursor = db.cursor()
        if status:
            cursor.execute("""
                SELECT r.*,
                       (SELECT COUNT(*) FROM bookings b WHERE b.ride_id = r.id AND b.status = 'Pending') as pending_requests,
                       (SELECT COUNT(*) FROM bookings b WHERE b.ride_id = r.id AND b.status = 'Accepted') as accepted_bookings
                FROM rides r
                WHERE r.driver_id = ? AND r.status = ?
                ORDER BY r.ride_date DESC, r.departure_time DESC
            """, (driver_id, status))
        else:
            cursor.execute("""
                SELECT r.*,
                       (SELECT COUNT(*) FROM bookings b WHERE b.ride_id = r.id AND b.status = 'Pending') as pending_requests,
                       (SELECT COUNT(*) FROM bookings b WHERE b.ride_id = r.id AND b.status = 'Accepted') as accepted_bookings
                FROM rides r
                WHERE r.driver_id = ?
                ORDER BY r.ride_date DESC, r.departure_time DESC
            """, (driver_id,))
        return cursor.fetchall()

    @staticmethod
    def cancel_ride(ride_id, driver_id=None):
        """Cancel a ride and mark its bookings cancelled."""
        db = get_db()
        cursor = db.cursor()
        
        # Verify ownership if driver_id provided
        if driver_id:
            cursor.execute("SELECT id FROM rides WHERE id = ? AND driver_id = ?", (ride_id, driver_id))
            if not cursor.fetchone():
                return False, "Unauthorized or ride not found."
                
        cursor.execute("UPDATE rides SET status = 'Cancelled' WHERE id = ?", (ride_id,))
        # Cancel all pending/accepted bookings for this ride
        cursor.execute("UPDATE bookings SET status = 'Cancelled' WHERE ride_id = ? AND status IN ('Pending', 'Accepted')", (ride_id,))
        db.commit()
        return True, "Ride has been cancelled."

    @staticmethod
    def mark_completed(ride_id, driver_id):
        """Mark a ride as completed and update its accepted bookings to completed."""
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("SELECT id, status FROM rides WHERE id = ? AND driver_id = ?", (ride_id, driver_id))
        ride = cursor.fetchone()
        if not ride:
            return False, "Ride not found or unauthorized."
            
        if ride['status'] == 'Completed':
            return False, "Ride is already marked as completed."
            
        cursor.execute("UPDATE rides SET status = 'Completed' WHERE id = ?", (ride_id,))
        # All accepted bookings become completed
        cursor.execute("UPDATE bookings SET status = 'Completed' WHERE ride_id = ? AND status = 'Accepted'", (ride_id,))
        db.commit()
        return True, "Ride and bookings marked as Completed."

    @staticmethod
    def delete(ride_id):
        """Delete ride (Admin function)."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM rides WHERE id = ?", (ride_id,))
        db.commit()
        return True, "Ride deleted successfully."

    @staticmethod
    def get_all():
        """Fetch all rides across all drivers (Admin overview)."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT r.*, u.name as driver_name, u.email as driver_email, d.vehicle_model, d.vehicle_number,
                   (SELECT COUNT(*) FROM bookings b WHERE b.ride_id = r.id) as total_bookings
            FROM rides r
            JOIN drivers d ON r.driver_id = d.id
            JOIN users u ON d.user_id = u.id
            ORDER BY r.created_at DESC
        """)
        return cursor.fetchall()
