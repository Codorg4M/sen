from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import User
from models.driver import Driver

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login supporting Rider, Driver, and Admin credentials."""
    if 'user_id' in session:
        role = session.get('role')
        if role == 'rider':
            return redirect(url_for('rider.dashboard'))
        elif role == 'driver':
            return redirect(url_for('driver.dashboard'))
        elif role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return render_template('login.html', email=email)

        user, err = User.authenticate(email, password)
        if err:
            flash(err, "danger")
            return render_template('login.html', email=email)

        # Set session variables
        session.clear()
        session['user_id'] = user['id']
        session['name'] = user['name']
        session['email'] = user['email']
        session['role'] = user['role']

        flash(f"Welcome back, {user['name']}!", "success")

        # Redirect based on role
        if user['role'] == 'rider':
            return redirect(url_for('rider.dashboard'))
        elif user['role'] == 'driver':
            return redirect(url_for('driver.dashboard'))
        elif user['role'] == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.index'))

    return render_template('login.html')

@auth_bp.route('/register/rider', methods=['GET', 'POST'])
def register_rider():
    """Register a new Rider."""
    if 'user_id' in session:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        errors = User.validate_registration(name, email, phone, password, confirm_password, role='rider')
        if User.find_by_email(email):
            errors.append("An account with this email address already exists.")

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template('register_rider.html', name=name, email=email, phone=phone)

        # Create user
        try:
            user_id = User.create(name, email, phone, password, role='rider')
            flash("Registration successful! You can now log in as a Rider.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash("An error occurred during registration. Please try again.", "danger")
            return render_template('register_rider.html', name=name, email=email, phone=phone)

    return render_template('register_rider.html')

@auth_bp.route('/register/driver', methods=['GET', 'POST'])
def register_driver():
    """Register a new Driver with vehicle specifications."""
    if 'user_id' in session:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Driver specific fields
        license_number = request.form.get('license_number', '').strip()
        vehicle_type = request.form.get('vehicle_type', '').strip()
        vehicle_model = request.form.get('vehicle_model', '').strip()
        vehicle_number = request.form.get('vehicle_number', '').strip()
        total_seats = request.form.get('total_seats', '').strip()

        # Validation
        errors = User.validate_registration(name, email, phone, password, confirm_password, role='driver')
        driver_errors = Driver.validate_driver_info(license_number, vehicle_type, vehicle_model, vehicle_number, total_seats)
        errors.extend(driver_errors)

        if User.find_by_email(email):
            errors.append("An account with this email address already exists.")

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                'register_driver.html',
                name=name, email=email, phone=phone,
                license_number=license_number, vehicle_type=vehicle_type,
                vehicle_model=vehicle_model, vehicle_number=vehicle_number,
                total_seats=total_seats
            )

        try:
            # Create user first
            user_id = User.create(name, email, phone, password, role='driver')
            driver_id, driver_err = Driver.create(user_id, license_number, vehicle_type, vehicle_model, vehicle_number, total_seats)
            if driver_err:
                flash(driver_err, "danger")
                return render_template('register_driver.html', name=name, email=email, phone=phone)

            flash("Registration successful! You can now log in as a Driver.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash("An error occurred during driver registration. Please try again.", "danger")
            return render_template('register_driver.html', name=name, email=email, phone=phone)

    return render_template('register_driver.html')

@auth_bp.route('/logout')
def logout():
    """Clear session and log out user."""
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for('auth.login'))
