from database.db import get_db

class Booking:
    """Booking model handling ride requests, seat allocation, overbooking prevention and cancellations."""

    VALID_STATUSES = ('Pending', 'Accepted', 'Rejected', 'Cancelled', 'Completed')

    @staticmethod
    def create_request(ride_id, rider_id, seats_requested):
        """Create a new booking request with overbooking and duplicate prevention."""
        db = get_db()
        cursor = db.cursor()

        # 1. Validate seats requested
        try:
            seats = int(seats_requested)
            if seats <= 0:
                return None, "Please select at least 1 seat."
        except (ValueError, TypeError):
            return None, "Invalid number of seats requested."

        # 2. Fetch ride and verify it is available
        cursor.execute("SELECT * FROM rides WHERE id = ?", (ride_id,))
        ride = cursor.fetchone()
        if not ride:
            return None, "The requested ride does not exist."

        if ride['status'] not in ('Available',):
            return None, f"This ride is currently {ride['status'].lower()} and cannot accept new bookings."

        # 3. Check seat availability
        if seats > ride['available_seats']:
            return None, f"Not enough seats available. Only {ride['available_seats']} seat(s) remaining."

        # 4. Prevent duplicate active bookings by the same rider for the same ride
        cursor.execute("""
            SELECT id, status FROM bookings 
            WHERE ride_id = ? AND rider_id = ? AND status IN ('Pending', 'Accepted')
        """, (ride_id, rider_id))
        existing_booking = cursor.fetchone()
        if existing_booking:
            return None, f"You already have a {existing_booking['status'].lower()} booking for this ride."

        # 5. Prevent driver from booking their own ride
        cursor.execute("SELECT user_id FROM drivers WHERE id = ?", (ride['driver_id'],))
        driver_user = cursor.fetchone()
        if driver_user and driver_user['user_id'] == rider_id:
            return None, "Drivers cannot book seats on their own rides."

        # 6. Calculate total fare
        total_fare = round(seats * float(ride['fare_per_passenger']), 2)

        # 7. Create booking record
        cursor.execute("""
            INSERT INTO bookings (ride_id, rider_id, seats_requested, total_fare, status)
            VALUES (?, ?, ?, ?, 'Pending')
        """, (ride_id, rider_id, seats, total_fare))
        booking_id = cursor.lastrowid
        db.commit()
        return booking_id, None

    @staticmethod
    def accept_request(booking_id, driver_id):
        """
        Accept booking request by driver.
        Enforces overbooking check, reduces available seats, and transitions ride to 'Full' if seats reach 0.
        """
        db = get_db()
        cursor = db.cursor()

        # Verify booking and driver ownership
        cursor.execute("""
            SELECT b.*, r.driver_id, r.available_seats, r.status as ride_status
            FROM bookings b
            JOIN rides r ON b.ride_id = r.id
            WHERE b.id = ?
        """, (booking_id,))
        booking = cursor.fetchone()

        if not booking:
            return False, "Booking not found."

        if booking['driver_id'] != driver_id:
            return False, "Unauthorized: You are not the driver of this ride."

        if booking['status'] != 'Pending':
            return False, f"Cannot accept booking with status '{booking['status']}'."

        # Overbooking check
        if booking['available_seats'] < booking['seats_requested']:
            return False, f"Not enough seats available ({booking['available_seats']} left, but {booking['seats_requested']} requested)."

        new_available = booking['available_seats'] - booking['seats_requested']
        new_ride_status = 'Full' if new_available == 0 else booking['ride_status']

        # Update booking status to Accepted
        cursor.execute("UPDATE bookings SET status = 'Accepted' WHERE id = ?", (booking_id,))
        
        # Deduct seats and update ride status
        cursor.execute("""
            UPDATE rides 
            SET available_seats = ?, status = ?
            WHERE id = ?
        """, (new_available, new_ride_status, booking['ride_id']))

        db.commit()
        return True, "Booking request accepted successfully."

    @staticmethod
    def reject_request(booking_id, driver_id):
        """Reject booking request by driver."""
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT b.*, r.driver_id
            FROM bookings b
            JOIN rides r ON b.ride_id = r.id
            WHERE b.id = ?
        """, (booking_id,))
        booking = cursor.fetchone()

        if not booking:
            return False, "Booking not found."

        if booking['driver_id'] != driver_id:
            return False, "Unauthorized."

        if booking['status'] != 'Pending':
            return False, f"Cannot reject a booking that is currently '{booking['status']}'."

        cursor.execute("UPDATE bookings SET status = 'Rejected' WHERE id = ?", (booking_id,))
        db.commit()
        return True, "Booking request rejected."

    @staticmethod
    def cancel_by_rider(booking_id, rider_id):
        """
        Cancel booking by rider.
        If booking was Accepted, restores seats to the ride and updates ride status if it was 'Full'.
        """
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT b.*, r.available_seats, r.status as ride_status, r.id as ride_id
            FROM bookings b
            JOIN rides r ON b.ride_id = r.id
            WHERE b.id = ? AND b.rider_id = ?
        """, (booking_id, rider_id))
        booking = cursor.fetchone()

        if not booking:
            return False, "Booking not found or unauthorized."

        if booking['status'] not in ('Pending', 'Accepted'):
            return False, f"Cannot cancel a booking that is already {booking['status'].lower()}."

        # If booking was Accepted, restore seats
        if booking['status'] == 'Accepted':
            restored_seats = booking['available_seats'] + booking['seats_requested']
            new_ride_status = 'Available' if booking['ride_status'] == 'Full' else booking['ride_status']
            cursor.execute("""
                UPDATE rides 
                SET available_seats = ?, status = ?
                WHERE id = ?
            """, (restored_seats, new_ride_status, booking['ride_id']))

        cursor.execute("UPDATE bookings SET status = 'Cancelled' WHERE id = ?", (booking_id,))
        db.commit()
        return True, "Booking cancelled successfully."

    @staticmethod
    def get_by_rider(rider_id, status=None):
        """Fetch bookings for a rider."""
        db = get_db()
        cursor = db.cursor()
        query = """
            SELECT b.*, 
                   r.pickup_location, r.destination, r.ride_date, r.departure_time, 
                   r.vehicle_type, r.fare_per_passenger, r.status as ride_status,
                   u.name as driver_name, u.phone as driver_phone,
                   d.vehicle_model, d.vehicle_number
            FROM bookings b
            JOIN rides r ON b.ride_id = r.id
            JOIN drivers d ON r.driver_id = d.id
            JOIN users u ON d.user_id = u.id
            WHERE b.rider_id = ?
        """
        params = [rider_id]
        if status:
            query += " AND b.status = ?"
            params.append(status)
        query += " ORDER BY b.booking_date DESC"
        cursor.execute(query, tuple(params))
        return cursor.fetchall()

    @staticmethod
    def get_requests_for_driver(driver_id, status='Pending'):
        """Fetch booking requests for rides owned by the driver."""
        db = get_db()
        cursor = db.cursor()
        query = """
            SELECT b.*, 
                   r.pickup_location, r.destination, r.ride_date, r.departure_time, 
                   r.available_seats, r.status as ride_status,
                   u.name as rider_name, u.phone as rider_phone, u.email as rider_email
            FROM bookings b
            JOIN rides r ON b.ride_id = r.id
            JOIN users u ON b.rider_id = u.id
            WHERE r.driver_id = ?
        """
        params = [driver_id]
        if status:
            query += " AND b.status = ?"
            params.append(status)
        query += " ORDER BY b.booking_date DESC"
        cursor.execute(query, tuple(params))
        return cursor.fetchall()

    @staticmethod
    def get_all():
        """Fetch all bookings (Admin view)."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT b.*,
                   r.pickup_location, r.destination, r.ride_date, r.departure_time,
                   rider.name as rider_name, rider.email as rider_email,
                   driver_u.name as driver_name, driver_u.email as driver_email
            FROM bookings b
            JOIN rides r ON b.ride_id = r.id
            JOIN users rider ON b.rider_id = rider.id
            JOIN drivers d ON r.driver_id = d.id
            JOIN users driver_u ON d.user_id = driver_u.id
            ORDER BY b.booking_date DESC
        """)
        return cursor.fetchall()
