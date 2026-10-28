from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from auth.decorators import role_required
from models.driver import Driver
from models.ride import Ride
from models.booking import Booking
from services.fare_service import FareService

driver_bp = Blueprint('driver', __name__, url_prefix='/driver')

def get_current_driver():
    """Helper to fetch driver profile for current logged in user."""
    user_id = session.get('user_id')
    return Driver.find_by_user_id(user_id)

@driver_bp.route('/dashboard')
@role_required('driver')
def dashboard():
    """Driver dashboard displaying key performance metrics and quick ride overview."""
    driver = get_current_driver()
    if not driver:
        flash("Driver profile not found. Please register or contact support.", "danger")
        return redirect(url_for('main.index'))

    rides = Ride.get_by_driver(driver['id'])
    pending_requests = Booking.get_requests_for_driver(driver['id'], status='Pending')

    active_rides_count = sum(1 for r in rides if r['status'] in ('Available', 'Ongoing'))
    pending_requests_count = len(pending_requests)
    available_seats_count = sum(r['available_seats'] for r in rides if r['status'] == 'Available')
    completed_rides_count = sum(1 for r in rides if r['status'] == 'Completed')

    return render_template(
        'driver/dashboard.html',
        driver=driver,
        active_rides_count=active_rides_count,
        pending_requests_count=pending_requests_count,
        available_seats_count=available_seats_count,
        completed_rides_count=completed_rides_count,
        recent_rides=rides[:5],
        pending_requests=pending_requests[:5]
    )

@driver_bp.route('/create-ride', methods=['GET', 'POST'])
@role_required('driver')
def create_ride():
    """Create a new ride post with automated validation and fare estimation."""
    driver = get_current_driver()
    if not driver:
        flash("Driver profile not found.", "danger")
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        pickup = request.form.get('pickup_location', '').strip()
        destination = request.form.get('destination', '').strip()
        ride_date = request.form.get('ride_date', '').strip()
        departure_time = request.form.get('departure_time', '').strip()
        available_seats = request.form.get('available_seats', '').strip()
        vehicle_type = request.form.get('vehicle_type', driver['vehicle_type']).strip()
        fare = request.form.get('fare_per_passenger', '').strip()

        # Backend Validation
        errors = Ride.validate_ride(
            pickup, destination, ride_date, departure_time,
            available_seats, vehicle_type, fare
        )

        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template(
                'driver/create_ride.html',
                driver=driver,
                pickup_location=pickup,
                destination=destination,
                ride_date=ride_date,
                departure_time=departure_time,
                available_seats=available_seats,
                vehicle_type=vehicle_type,
                fare_per_passenger=fare
            )

        try:
            ride_id = Ride.create(
                driver['id'], pickup, destination, ride_date,
                departure_time, available_seats, vehicle_type, fare
            )
            flash("Ride created successfully! It is now available for riders to book.", "success")
            return redirect(url_for('driver.my_rides'))
        except Exception as e:
            flash("Error creating ride. Please ensure all values are valid.", "danger")
            return render_template('driver/create_ride.html', driver=driver)

    return render_template('driver/create_ride.html', driver=driver)

@driver_bp.route('/my-rides')
@role_required('driver')
def my_rides():
    """View all rides created by the driver."""
    driver = get_current_driver()
    rides = Ride.get_by_driver(driver['id'])
    return render_template('driver/my_rides.html', rides=rides)

@driver_bp.route('/requests')
@role_required('driver')
def ride_requests():
    """View incoming booking requests for the driver's rides."""
    driver = get_current_driver()
    requests_list = Booking.get_requests_for_driver(driver['id'], status='Pending')
    return render_template('driver/ride_requests.html', requests=requests_list)

@driver_bp.route('/requests/accept/<int:booking_id>', methods=['POST'])
@role_required('driver')
def accept_request(booking_id):
    """Driver accepts a rider's booking request."""
    driver = get_current_driver()
    success, msg = Booking.accept_request(booking_id, driver['id'])
    if success:
        flash("Ride request accepted! Seats have been reserved.", "success")
    else:
        flash(f"Could not accept request: {msg}", "danger")
    return redirect(url_for('driver.ride_requests'))

@driver_bp.route('/requests/reject/<int:booking_id>', methods=['POST'])
@role_required('driver')
def reject_request(booking_id):
    """Driver rejects a rider's booking request."""
    driver = get_current_driver()
    success, msg = Booking.reject_request(booking_id, driver['id'])
    if success:
        flash("Ride request rejected.", "info")
    else:
        flash(f"Could not reject request: {msg}", "danger")
    return redirect(url_for('driver.ride_requests'))

@driver_bp.route('/rides/complete/<int:ride_id>', methods=['POST'])
@role_required('driver')
def complete_ride(ride_id):
    """Mark an active ride and its accepted bookings as Completed."""
    driver = get_current_driver()
    success, msg = Ride.mark_completed(ride_id, driver['id'])
    if success:
        flash("Ride marked as Completed! Bookings have moved to completed status.", "success")
    else:
        flash(f"Error: {msg}", "danger")
    return redirect(url_for('driver.my_rides'))

@driver_bp.route('/rides/cancel/<int:ride_id>', methods=['POST'])
@role_required('driver')
def cancel_ride(ride_id):
    """Cancel a ride."""
    driver = get_current_driver()
    success, msg = Ride.cancel_ride(ride_id, driver['id'])
    if success:
        flash("Ride has been cancelled and riders will be notified.", "warning")
    else:
        flash(f"Error: {msg}", "danger")
    return redirect(url_for('driver.my_rides'))

@driver_bp.route('/completed-rides')
@role_required('driver')
def completed_rides():
    """Archive of rides successfully completed by driver."""
    driver = get_current_driver()
    completed = Ride.get_by_driver(driver['id'], status='Completed')
    return render_template('driver/completed_rides.html', rides=completed)
