/**
 * RideShare - Client-side Interactivity & Validation
 * Software Engineering Mini Project
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Mobile Menu Toggle
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.getElementById('navLinks');
    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', function () {
            navLinks.classList.toggle('show');
        });
    }

    // 2. Alert Dismissal
    const alertCloses = document.querySelectorAll('.alert-close');
    alertCloses.forEach(btn => {
        btn.addEventListener('click', function () {
            const alert = this.closest('.alert');
            if (alert) {
                alert.style.transition = 'opacity 0.3s ease';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 300);
            }
        });
    });

    // 3. Password Confirmation Validation
    const regForms = document.querySelectorAll('form[action*="register"]');
    regForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const password = form.querySelector('input[name="password"]');
            const confirmPassword = form.querySelector('input[name="confirm_password"]');
            if (password && confirmPassword && password.value !== confirmPassword.value) {
                e.preventDefault();
                alert("Passwords do not match. Please re-enter.");
                confirmPassword.focus();
            }
        });
    });

    // 4. Live Fare Calculator in Driver Create Ride Form
    const pickupInput = document.getElementById('pickup_location');
    const destInput = document.getElementById('destination');
    const fareInput = document.getElementById('fare_per_passenger');
    const farePreviewBox = document.getElementById('liveFarePreview');

    function updateEstimatedFare() {
        if (!pickupInput || !destInput || !fareInput) return;
        const p = pickupInput.value.trim();
        const d = destInput.value.trim();
        if (p && d) {
            fetch(`/api/fare/calculate?pickup=${encodeURIComponent(p)}&destination=${encodeURIComponent(d)}`)
                .then(res => res.json())
                .then(data => {
                    if (data && data.estimated_fare) {
                        // Auto populate recommended fare if empty or previous estimate
                        if (!fareInput.value || fareInput.dataset.autoFilled === "true") {
                            fareInput.value = data.estimated_fare;
                            fareInput.dataset.autoFilled = "true";
                        }
                        if (farePreviewBox) {
                            farePreviewBox.innerHTML = `
                                <strong>Estimated Distance:</strong> ${data.distance_km} km |
                                <strong>Recommended Fare:</strong> ₹${data.estimated_fare}
                                <span class="form-text" style="display:block;">${data.disclaimer}</span>
                            `;
                            farePreviewBox.style.display = 'block';
                        }
                    }
                })
                .catch(err => console.log('Fare estimation note:', err));
        }
    }

    if (pickupInput && destInput) {
        pickupInput.addEventListener('blur', updateEstimatedFare);
        destInput.addEventListener('blur', updateEstimatedFare);
    }

    // 5. Booking Modal / Seat Confirmation
    const bookForms = document.querySelectorAll('.book-ride-form');
    bookForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const seats = form.querySelector('select[name="seats_requested"], input[name="seats_requested"]');
            const available = parseInt(form.dataset.availableSeats || "999", 10);
            if (seats && parseInt(seats.value, 10) > available) {
                e.preventDefault();
                alert(`Cannot book more seats than available (${available} available).`);
            }
        });
    });
});

/**
 * Quick-fill demo account credentials for immediate testing
 */
function fillDemoLogin(role) {
    const emailField = document.getElementById('loginEmail');
    const passwordField = document.getElementById('loginPassword');
    if (!emailField || !passwordField) return;

    if (role === 'rider') {
        emailField.value = 'rider@demo.com';
        passwordField.value = 'Rider@123';
    } else if (role === 'driver') {
        emailField.value = 'driver@demo.com';
        passwordField.value = 'Driver@123';
    } else if (role === 'admin') {
        emailField.value = 'admin@demo.com';
        passwordField.value = 'Admin@123';
    }
}
