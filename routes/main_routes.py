from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from auth.decorators import login_required
from models.user import User
from models.driver import Driver
from models.ride import Ride

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Application landing page with hero, how-it-works, features, role showcases, and demo access."""
    # Get available rides for the homepage preview
    featured_rides = Ride.search(min_seats=1)[:4]
    return render_template('index.html', featured_rides=featured_rides)

@main_bp.route('/about')
def about():
    """About RideShare & Software Engineering Architecture overview."""
    return render_template('about.html')

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management for Rider, Driver, and Admin."""
    user_id = session['user_id']
    user = User.find_by_id(user_id)
    
    driver_info = None
    if user['role'] == 'driver':
        driver_info = Driver.find_by_user_id(user_id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()

        if not name or len(name) < 2:
            flash("Full name must be at least 2 characters.", "danger")
            return render_template('profile.html', user=user, driver_info=driver_info)

        # Update basic profile
        success, msg = User.update_profile(user_id, name, email, phone)
        if not success:
            flash(msg, "danger")
            return render_template('profile.html', user=user, driver_info=driver_info)

        # Update session name
        session['name'] = name
        session['email'] = email

        # If driver, update vehicle & license details
        if user['role'] == 'driver' and driver_info:
            license_number = request.form.get('license_number', '').strip()
            vehicle_type = request.form.get('vehicle_type', '').strip()
            vehicle_model = request.form.get('vehicle_model', '').strip()
            vehicle_number = request.form.get('vehicle_number', '').strip()
            total_seats = request.form.get('total_seats', '').strip()

            d_errors = Driver.validate_driver_info(license_number, vehicle_type, vehicle_model, vehicle_number, total_seats)
            if d_errors:
                for err in d_errors:
                    flash(err, "danger")
                return render_template('profile.html', user=user, driver_info=driver_info)

            d_success, d_msg = Driver.update_driver_info(
                driver_info['id'], license_number, vehicle_type, vehicle_model, vehicle_number, total_seats
            )
            if not d_success:
                flash(d_msg, "danger")
                return render_template('profile.html', user=user, driver_info=driver_info)

        flash("Profile updated successfully!", "success")
        return redirect(url_for('main.profile'))

    return render_template('profile.html', user=user, driver_info=driver_info)
