#!/usr/bin/env python3
"""
RideShare – Ride Sharing Web Application
College Software Engineering Mini Project Entry Point
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    banner = """
====================================================================
 🚗  RideShare - Ride Sharing Web Application
     College Software Engineering Mini Project
====================================================================
 Server URL:      http://127.0.0.1:5000
 
 Demo Accounts for Academic Presentation:
   • Rider:       rider@demo.com  /  Rider@123
   • Driver:      driver@demo.com /  Driver@123
   • Admin:       admin@demo.com  /  Admin@123

 Features Enabled:
   [x] Role-Based Access Control (Rider, Driver, Admin)
   [x] Seat Inventory & Overbooking Prevention Guard
   [x] Live Fare Estimation (Base ₹30 + ₹12/KM)
   [x] Relational Database Schema & Foreign Key Constraints
   [x] Interactive Leaflet OpenStreetMap Route Preview
====================================================================
 Press CTRL+C to quit server.
"""
    print(banner)
    app.run(debug=True, host='127.0.0.1', port=5000)
