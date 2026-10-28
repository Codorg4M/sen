from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from auth.decorators import role_required
from models.ride import Ride
from models.booking import Booking

rider_bp = Blueprint('rider', __name__, url_prefix='/rider')

@rider_bp.route('/dashboard')
@role_required('rider')
def dashboard():
    """Rider dashboard displaying key metrics, recent bookings and quick actions."""
    rider_id = session['user_id']
    all_bookings = Booking.get_by_rider(rider_id)

    # Dashboard Metrics
    active_bookings_count = sum(1 for b in all_bookings if b['status'] == 'Accepted')
    pending_requests_count = sum(1 for b in all_bookings if b['status'] == 'Pending')
    completed_rides_count = sum(1 for b in all_bookings if b['status'] == 'Completed')
    total_rides_count = len(all_bookings)

    recent_bookings = all_bookings[:5]

    return render_template(
        'rider/dashboard.html',
        active_count=active_bookings_count,
        pending_count=pending_requests_count,
        completed_count=completed_rides_count,
        total_count=total_rides_count,
        recent_bookings=recent_bookings
    )

@rider_bp.route('/search', methods=['GET', 'POST'])
@role_required('rider')
def search():
    """Search and filter available rides."""
    pickup = request.args.get('pickup', '').strip()
    destination = request.args.get('destination', '').strip()
    ride_date = request.args.get('date', '').strip()
    vehicle_type = request.args.get('vehicle_type', '').strip()
    passengers = request.args.get('passengers', 1, type=int)

    # Fetch matching available rides
    rides = Ride.search(
        pickup=pickup,
        destination=destination,
        ride_date=ride_date,
        vehicle_type=vehicle_type,
        min_seats=passengers
    )

    return render_template(
        'rider/search_rides.html',
        rides=rides,
        pickup=pickup,
        destination=destination,
        ride_date=ride_date,
        vehicle_type=vehicle_type,
        passengers=passengers
    )

@rider_bp.route('/book/<int:ride_id>', methods=['POST'])
@role_required('rider')
def book_ride(ride_id):
    """Submit a ride booking request with validation and overbooking prevention."""
    rider_id = session['user_id']
    seats_requested = request.form.get('seats_requested', 1)

    booking_id, err = Booking.create_request(ride_id, rider_id, seats_requested)
    if err:
        flash(f"Booking Error: {err}", "danger")
        return redirect(url_for('rider.search', **request.args))

    flash("Ride requested successfully! Your booking status is currently 'Pending' waiting for driver confirmation.", "success")
    return redirect(url_for('rider.my_bookings'))

@rider_bp.route('/bookings')
@role_required('rider')
def my_bookings():
    """View active, pending, accepted, and rejected bookings."""
    rider_id = session['user_id']
    bookings = Booking.get_by_rider(rider_id)
    return render_template('rider/my_bookings.html', bookings=bookings)

@rider_bp.route('/bookings/cancel/<int:booking_id>', methods=['POST'])
@role_required('rider')
def cancel_booking(booking_id):
    """Cancel a booking by rider."""
    rider_id = session['user_id']
    success, msg = Booking.cancel_by_rider(booking_id, rider_id)
    if success:
        flash("Your booking has been cancelled.", "info")
    else:
        flash(f"Could not cancel booking: {msg}", "danger")
    return redirect(url_for('rider.my_bookings'))

@rider_bp.route('/history')
@role_required('rider')
def ride_history():
    """View completed ride history."""
    rider_id = session['user_id']
    completed_bookings = Booking.get_by_rider(rider_id, status='Completed')
    return render_template('rider/ride_history.html', bookings=completed_bookings)
