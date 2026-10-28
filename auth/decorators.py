from functools import wraps
from flask import session, redirect, url_for, flash, abort, request

def login_required(f):
    """Decorator ensuring that a user is logged into the session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    """Decorator ensuring user belongs to one of the authorized roles."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash("Please log in to access this page.", "warning")
                return redirect(url_for('auth.login', next=request.path))

            user_role = session.get('role')
            if user_role not in allowed_roles:
                flash(f"Access Denied: You must be an authorized {', '.join(allowed_roles)} to view this page.", "danger")
                # Redirect to appropriate user dashboard
                if user_role == 'rider':
                    return redirect(url_for('rider.dashboard'))
                elif user_role == 'driver':
                    return redirect(url_for('driver.dashboard'))
                elif user_role == 'admin':
                    return redirect(url_for('admin.dashboard'))
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
