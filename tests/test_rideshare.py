import unittest
import os
import sys
import tempfile

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from database.db import get_db, init_db
from models.user import User
from models.driver import Driver
from models.ride import Ride
from models.booking import Booking

class TestRideShareApplication(unittest.TestCase):
    """
    Automated Test Suite for RideShare Mini Project.
    Implements Software Engineering Test Cases TC01 through TC14 (Section 20).
    """

    @classmethod
    def setUpClass(cls):
        """Set up test Flask client with an isolated temporary SQLite database."""
        cls.db_fd, cls.db_path = tempfile.mkstemp(suffix='.db')
        
        class TestConfig:
            TESTING = True
            SECRET_KEY = 'test-secret-key-12345'
            DATABASE_PATH = cls.db_path
            BASE_FARE = 30.0
            RATE_PER_KM = 12.0
            WTF_CSRF_ENABLED = False

        cls.app = create_app(TestConfig)
        cls.client = cls.app.test_client()

    def setUp(self):
        """Clear session before each test case to ensure test isolation."""
        self.client.get('/logout')

    @classmethod
    def tearDownClass(cls):
        """Clean up test database file."""
        os.close(cls.db_fd)
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)

    def test_tc01_valid_rider_registration(self):
        """TC01: Valid rider registration."""
        response = self.client.post('/register/rider', data={
            'name': 'Test New Rider',
            'email': 'newrider@test.com',
            'phone': '9876543210',
            'password': 'Password@123',
            'confirm_password': 'Password@123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            user = User.find_by_email('newrider@test.com')
            self.assertIsNotNone(user)
            self.assertEqual(user['role'], 'rider')
            self.assertEqual(user['status'], 'active')

    def test_tc02_invalid_email_registration(self):
        """TC02: Invalid email registration."""
        response = self.client.post('/register/rider', data={
            'name': 'Invalid Email User',
            'email': 'not-a-valid-email',
            'phone': '9876543210',
            'password': 'Password@123',
            'confirm_password': 'Password@123'
        }, follow_redirects=True)
        self.assertIn(b"Please enter a valid email address.", response.data)
        with self.app.app_context():
            user = User.find_by_email('not-a-valid-email')
            self.assertIsNone(user)

    def test_tc03_valid_login(self):
        """TC03: Valid login."""
        response = self.client.post('/login', data={
            'email': 'rider@demo.com',
            'password': 'Rider@123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome back", response.data)
        self.assertIn(b"Rider Dashboard", response.data)

    def test_tc04_invalid_login(self):
        """TC04: Invalid login."""
        response = self.client.post('/login', data={
            'email': 'rider@demo.com',
            'password': 'WrongPassword123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid email or password", response.data)

    def test_tc05_driver_creates_ride(self):
        """TC05: Driver creates ride."""
        # Log in as Driver
        self.client.post('/login', data={'email': 'driver@demo.com', 'password': 'Driver@123'})
        response = self.client.post('/driver/create-ride', data={
            'pickup_location': 'North Campus',
            'destination': 'South Metro',
            'ride_date': '2026-10-15',
            'departure_time': '10:00',
            'available_seats': 3,
            'vehicle_type': 'Sedan',
            'fare_per_passenger': 120.0
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Ride created successfully", response.data)
        with self.app.app_context():
            rides = Ride.search(pickup='North Campus')
            self.assertTrue(len(rides) >= 1)
            self.assertEqual(rides[0]['destination'], 'South Metro')
            self.assertEqual(rides[0]['available_seats'], 3)
            self.assertEqual(rides[0]['status'], 'Available')

    def test_tc06_rider_searches_ride(self):
        """TC06: Rider searches ride."""
        self.client.post('/login', data={'email': 'rider@demo.com', 'password': 'Rider@123'})
        response = self.client.get('/rider/search?pickup=College+Road&destination=Railway+Station')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"College Road", response.data)
        self.assertIn(b"Railway Station", response.data)

    def test_tc07_rider_requests_available_ride(self):
        """TC07: Rider requests available ride."""
        with self.app.app_context():
            db = get_db()
            # Fetch Ride 1
            cursor = db.cursor()
            cursor.execute("SELECT id FROM rides WHERE pickup_location = 'College Road' LIMIT 1")
            ride = cursor.fetchone()
            self.assertIsNotNone(ride)
            ride_id = ride['id']

            # Use rider2 to create request
            cursor.execute("SELECT id FROM users WHERE email = 'newrider@test.com'")
            user = cursor.fetchone()
            rider_id = user['id']

            booking_id, err = Booking.create_request(ride_id, rider_id, 1)
            self.assertIsNone(err)
            self.assertIsNotNone(booking_id)

            cursor.execute("SELECT status FROM bookings WHERE id = ?", (booking_id,))
            b = cursor.fetchone()
            self.assertEqual(b['status'], 'Pending')

    def test_tc08_driver_accepts_booking(self):
        """TC08: Driver accepts booking."""
        with self.app.app_context():
            db = get_db()
            cursor = db.cursor()
            # Create a dedicated ride and booking to test acceptance
            cursor.execute("SELECT id FROM drivers LIMIT 1")
            driver_id = cursor.fetchone()['id']
            cursor.execute("SELECT id FROM users WHERE role = 'rider' LIMIT 1")
            rider_id = cursor.fetchone()['id']

            ride_id = Ride.create(driver_id, "Point A", "Point B", "2026-11-01", "12:00", 2, "Sedan", 100.0)
            booking_id, _ = Booking.create_request(ride_id, rider_id, 1)

            # Driver accepts
            success, msg = Booking.accept_request(booking_id, driver_id)
            self.assertTrue(success)

            # Assert booking is Accepted
            cursor.execute("SELECT status FROM bookings WHERE id = ?", (booking_id,))
            self.assertEqual(cursor.fetchone()['status'], 'Accepted')

            # Assert available seats reduced from 2 to 1
            cursor.execute("SELECT available_seats, status FROM rides WHERE id = ?", (ride_id,))
            ride_row = cursor.fetchone()
            self.assertEqual(ride_row['available_seats'], 1)
            self.assertEqual(ride_row['status'], 'Available')

    def test_tc09_driver_rejects_booking(self):
        """TC09: Driver rejects booking."""
        with self.app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT id FROM drivers LIMIT 1")
            driver_id = cursor.fetchone()['id']
            cursor.execute("SELECT id FROM users WHERE role = 'rider' LIMIT 1")
            rider_id = cursor.fetchone()['id']

            ride_id = Ride.create(driver_id, "Point C", "Point D", "2026-11-02", "15:00", 3, "SUV", 150.0)
            booking_id, _ = Booking.create_request(ride_id, rider_id, 2)

            success, msg = Booking.reject_request(booking_id, driver_id)
            self.assertTrue(success)

            cursor.execute("SELECT status FROM bookings WHERE id = ?", (booking_id,))
            self.assertEqual(cursor.fetchone()['status'], 'Rejected')

            cursor.execute("SELECT available_seats FROM rides WHERE id = ?", (ride_id,))
            self.assertEqual(cursor.fetchone()['available_seats'], 3)

    def test_tc10_prevent_overbooking(self):
        """TC10: Prevent overbooking."""
        with self.app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT id FROM drivers LIMIT 1")
            driver_id = cursor.fetchone()['id']
            cursor.execute("SELECT id FROM users WHERE role = 'rider' LIMIT 1")
            rider_id = cursor.fetchone()['id']

            # Create ride with only 1 seat
            ride_id = Ride.create(driver_id, "Campus Gate", "Station", "2026-11-05", "08:00", 1, "Hatchback", 50.0)

            # Requesting 2 seats when only 1 is available must fail
            booking_id, err = Booking.create_request(ride_id, rider_id, 2)
            self.assertIsNone(booking_id)
            self.assertIn("Not enough seats available", err)

    def test_tc11_rider_cancels_booking(self):
        """TC11: Rider cancels booking."""
        with self.app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT id FROM drivers LIMIT 1")
            driver_id = cursor.fetchone()['id']
            cursor.execute("SELECT id FROM users WHERE role = 'rider' LIMIT 1")
            rider_id = cursor.fetchone()['id']

            ride_id = Ride.create(driver_id, "Hostel", "Library", "2026-11-06", "09:00", 4, "Sedan", 30.0)
            booking_id, _ = Booking.create_request(ride_id, rider_id, 1)

            # Rider cancels pending booking
            success, msg = Booking.cancel_by_rider(booking_id, rider_id)
            self.assertTrue(success)

            cursor.execute("SELECT status FROM bookings WHERE id = ?", (booking_id,))
            self.assertEqual(cursor.fetchone()['status'], 'Cancelled')

    def test_tc12_driver_completes_ride(self):
        """TC12: Driver completes ride."""
        with self.app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT id FROM drivers LIMIT 1")
            driver_id = cursor.fetchone()['id']
            cursor.execute("SELECT id FROM users WHERE role = 'rider' LIMIT 1")
            rider_id = cursor.fetchone()['id']

            ride_id = Ride.create(driver_id, "Start X", "End Y", "2026-11-10", "14:00", 3, "Sedan", 120.0)
            booking_id, _ = Booking.create_request(ride_id, rider_id, 1)
            Booking.accept_request(booking_id, driver_id)

            # Driver marks completed
            success, msg = Ride.mark_completed(ride_id, driver_id)
            self.assertTrue(success)

            cursor.execute("SELECT status FROM rides WHERE id = ?", (ride_id,))
            self.assertEqual(cursor.fetchone()['status'], 'Completed')

            cursor.execute("SELECT status FROM bookings WHERE id = ?", (booking_id,))
            self.assertEqual(cursor.fetchone()['status'], 'Completed')

    def test_tc13_unauthorized_user_tries_to_access_dashboard(self):
        """TC13: Unauthorized user tries to access dashboard."""
        # Clear session
        self.client.get('/logout')

        # Guest trying to access protected rider dashboard -> must be redirected to login
        response = self.client.get('/rider/dashboard', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers.get('Location', ''))

        # Rider trying to access driver dashboard -> must be redirected to rider dashboard
        self.client.post('/login', data={'email': 'rider@demo.com', 'password': 'Rider@123'})
        response = self.client.get('/driver/dashboard', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/rider/dashboard', response.headers.get('Location', ''))

    def test_tc14_logout(self):
        """TC14: Logout."""
        self.client.post('/login', data={'email': 'rider@demo.com', 'password': 'Rider@123'})
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"successfully logged out", response.data)
        # Verify access to dashboard is now blocked
        dash_response = self.client.get('/rider/dashboard', follow_redirects=False)
        self.assertEqual(dash_response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
