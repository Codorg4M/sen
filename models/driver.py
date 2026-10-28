from database.db import get_db

class Driver:
    """Driver model handling vehicle specifications, license and driver profile operations."""

    @staticmethod
    def validate_driver_info(license_number, vehicle_type, vehicle_model, vehicle_number, total_seats):
        """Validate driver and vehicle specific fields."""
        errors = []
        if not license_number or len(license_number.strip()) < 5:
            errors.append("Driving license number cannot be empty and must be at least 5 characters.")
            
        if not vehicle_type or vehicle_type.strip() not in ('Sedan', 'Hatchback', 'SUV', 'Auto/Bike', 'Van'):
            errors.append("Please select a valid vehicle type (Sedan, Hatchback, SUV, Auto/Bike, Van).")
            
        if not vehicle_model or len(vehicle_model.strip()) < 2:
            errors.append("Vehicle model cannot be empty.")
            
        if not vehicle_number or len(vehicle_number.strip()) < 4:
            errors.append("Vehicle registration number cannot be empty.")
            
        try:
            seats = int(total_seats)
            if seats <= 0 or seats > 15:
                errors.append("Total seats must be between 1 and 15.")
        except (ValueError, TypeError):
            errors.append("Total seats must be a valid positive number.")
            
        return errors

    @staticmethod
    def create(user_id, license_number, vehicle_type, vehicle_model, vehicle_number, total_seats):
        """Create a driver record linked to a user."""
        db = get_db()
        cursor = db.cursor()
        
        # Check uniqueness of license and vehicle number
        cursor.execute("SELECT id FROM drivers WHERE license_number = ? OR vehicle_number = ?", 
                       (license_number.strip().upper(), vehicle_number.strip().upper()))
        if cursor.fetchone():
            return None, "A driver with this license number or vehicle registration number already exists."
            
        cursor.execute("""
            INSERT INTO drivers (user_id, license_number, vehicle_type, vehicle_model, vehicle_number, total_seats)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            license_number.strip().upper(),
            vehicle_type.strip(),
            vehicle_model.strip(),
            vehicle_number.strip().upper(),
            int(total_seats)
        ))
        db.commit()
        return cursor.lastrowid, None

    @staticmethod
    def find_by_user_id(user_id):
        """Fetch driver profile by associated user_id."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT d.*, u.name, u.email, u.phone, u.status as user_status
            FROM drivers d
            JOIN users u ON d.user_id = u.id
            WHERE d.user_id = ?
        """, (user_id,))
        return cursor.fetchone()

    @staticmethod
    def find_by_id(driver_id):
        """Fetch driver profile by driver_id."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT d.*, u.name, u.email, u.phone
            FROM drivers d
            JOIN users u ON d.user_id = u.id
            WHERE d.id = ?
        """, (driver_id,))
        return cursor.fetchone()

    @staticmethod
    def update_driver_info(driver_id, license_number, vehicle_type, vehicle_model, vehicle_number, total_seats):
        """Update driver vehicle and license information."""
        db = get_db()
        cursor = db.cursor()
        
        # Check uniqueness collision
        cursor.execute("""
            SELECT id FROM drivers 
            WHERE (license_number = ? OR vehicle_number = ?) AND id != ?
        """, (license_number.strip().upper(), vehicle_number.strip().upper(), driver_id))
        if cursor.fetchone():
            return False, "License number or Vehicle number is already registered with another driver."
            
        cursor.execute("""
            UPDATE drivers 
            SET license_number = ?, vehicle_type = ?, vehicle_model = ?, vehicle_number = ?, total_seats = ?
            WHERE id = ?
        """, (
            license_number.strip().upper(),
            vehicle_type.strip(),
            vehicle_model.strip(),
            vehicle_number.strip().upper(),
            int(total_seats),
            driver_id
        ))
        db.commit()
        return True, "Driver details updated successfully."

    @staticmethod
    def get_all():
        """Fetch all drivers with user details."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT d.*, u.name, u.email, u.phone, u.status as account_status,
                   (SELECT COUNT(*) FROM rides r WHERE r.driver_id = d.id) as total_rides
            FROM drivers d
            JOIN users u ON d.user_id = u.id
            ORDER BY d.created_at DESC
        """)
        return cursor.fetchall()
