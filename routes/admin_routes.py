from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from auth.decorators import role_required
from models.user import User
from models.driver import Driver
from models.ride import Ride
from models.booking import Booking

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@role_required('admin')
def dashboard():
    """Admin summary dashboard displaying platform-wide analytics."""
    all_users = User.get_all()
    all_rides = Ride.get_all()
    all_bookings = Booking.get_all()

    total_users = len(all_users)
    total_drivers = sum(1 for u in all_users if u['role'] == 'driver')
    total_riders = sum(1 for u in all_users if u['role'] == 'rider')
    total_rides = len(all_rides)
    total_bookings = len(all_bookings)
    active_rides = sum(1 for r in all_rides if r['status'] in ('Available', 'Ongoing'))
    completed_rides = sum(1 for r in all_rides if r['status'] == 'Completed')

    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_drivers=total_drivers,
        total_riders=total_riders,
        total_rides=total_rides,
        total_bookings=total_bookings,
        active_rides=active_rides,
        completed_rides=completed_rides,
        recent_users=all_users[:6],
        recent_rides=all_rides[:6]
    )

@admin_bp.route('/users')
@role_required('admin')
def users():
    """Manage registered users (Riders, Drivers, Admins)."""
    users_list = User.get_all()
    return render_template('admin/users.html', users=users_list)

@admin_bp.route('/users/toggle/<int:user_id>', methods=['POST'])
@role_required('admin')
def toggle_user(user_id):
    """Activate or deactivate a user account."""
    if user_id == session.get('user_id'):
        flash("You cannot deactivate your own admin account.", "warning")
        return redirect(url_for('admin.users'))

    success, msg = User.toggle_status(user_id)
    if success:
        flash(msg, "success")
    else:
        flash(msg, "danger")
    return redirect(url_for('admin.users'))

@admin_bp.route('/drivers')
@role_required('admin')
def drivers():
    """View all registered drivers with vehicle specifications."""
    drivers_list = Driver.get_all()
    return render_template('admin/drivers.html', drivers=drivers_list)

@admin_bp.route('/rides')
@role_required('admin')
def rides():
    """View all rides posted in the platform."""
    rides_list = Ride.get_all()
    return render_template('admin/rides.html', rides=rides_list)

@admin_bp.route('/rides/delete/<int:ride_id>', methods=['POST'])
@role_required('admin')
def delete_ride(ride_id):
    """Delete an invalid ride."""
    success, msg = Ride.delete(ride_id)
    if success:
        flash(msg, "info")
    else:
        flash(msg, "danger")
    return redirect(url_for('admin.rides'))

@admin_bp.route('/bookings')
@role_required('admin')
def bookings():
    """View all booking transactions."""
    bookings_list = Booking.get_all()
    return render_template('admin/bookings.html', bookings=bookings_list)
