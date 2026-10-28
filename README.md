# 🚗 RideShare – Ride Sharing Web Application

> **College Software Engineering Mini Project**  
> *"Share rides. Save time. Travel together."*

RideShare is a functional, beginner-friendly web application developed to demonstrate core Software Engineering concepts including requirements modeling, modular multi-tier architecture, role-based access control, relational database management, CRUD operations, business validation, error handling, automated testing, and responsive UI design.

---

## 📋 Table of Contents
1. [Project Overview & Objectives](#-project-overview--objectives)
2. [Software Engineering Concepts Demonstrated](#-software-engineering-concepts-demonstrated)
3. [User Roles & Permissions](#-user-roles--permissions)
4. [Key Features](#-key-features)
5. [Technologies Used](#-technologies-used)
6. [System Requirements](#-system-requirements)
7. [Installation & Setup](#-installation--setup)
8. [Database Setup & Schema](#-database-setup--schema)
9. [Pre-Seeded Demo Accounts](#-pre-seeded-demo-accounts)
10. [Application Workflow](#-application-workflow)
11. [Fare Calculation Formula](#-fare-calculation-formula)
12. [Automated Testing (TC01–TC14)](#-automated-testing-tc01tc14)
13. [Future Scope](#-future-scope)

---

## 🎯 Project Overview & Objectives

Urban commuters and college students frequently travel along identical routes in single-occupant vehicles, leading to unnecessary expenses and heavy traffic. **RideShare** connects drivers with empty seats to commuters seeking economical travel.

### Objectives:
- Demonstrate structured Software Engineering principles at a college level.
- Provide a functional web application with clean role separation (Rider, Driver, Admin).
- Maintain transactional consistency in seat allocation and booking statuses.
- Prevent overbooking and duplicate requests.
- Provide a transparent, simulated demo fare calculation without external payment gateway overheads.

---

## 🧠 Software Engineering Concepts Demonstrated

- **Modular Architecture:** Clean separation of concerns (Controllers/Blueprints, Services, Models, Database DDL, Views/Templates, Static assets).
- **Relational Integrity:** Foreign key enforcement (`PRAGMA foreign_keys = ON;`), relational mapping (`1:1` User-Driver, `1:M` Driver-Rides, `1:M` Rider-Bookings, `1:M` Ride-Bookings).
- **Authentication & Security:** PBKDF2:SHA256 password hashing (via `werkzeug.security`), session cookies, and role-based route decorators (`@role_required`).
- **State Transition Enforcement:** Strict lifecycle transitions for Rides (`Available` ➔ `Full` ➔ `Completed` / `Cancelled`) and Bookings (`Pending` ➔ `Accepted` / `Rejected` / `Cancelled` ➔ `Completed`).
- **Overbooking Prevention Guard:** Validates remaining capacity during request submission and upon driver approval.
- **Verification & Testing:** Fully automated test suite (`tests/test_rideshare.py`) verifying test cases TC01 to TC14.

---

## 👥 User Roles & Permissions

| Role | Permissions & Dashboards |
|:---|:---|
| **👤 Rider** | Search rides with filters, request booking, track status (Pending, Accepted, Rejected), cancel bookings, view completed ride history, manage profile. |
| **🚗 Driver** | Register vehicle & driving license, create ride listings, view incoming requests, accept/reject requests, manage seat inventory, mark rides completed, view history. |
| **🛡️ Administrator** | View platform statistics, view all users and toggle active/inactive status, inspect all posted rides and delete invalid ones, audit all bookings. |

---

## ✨ Key Features

1. **Role-Based Registration & Login:** Dedicated registration flows for Riders and Drivers (capturing license number, vehicle type, vehicle model, registration number, and total capacity).
2. **Ride Search & Advanced Filters:** Search by pickup location, destination, travel date, vehicle type, and number of passengers with case-insensitive matching.
3. **Seat Inventory & Overbooking Protection:** Seats are checked before booking and automatically deducted upon driver acceptance. If seats reach 0, the ride automatically transitions to `Full`.
4. **Duplicate Booking Prevention:** Riders cannot submit multiple pending or accepted bookings for the same ride.
5. **Two-Way Booking Lifecycle:**
   - Rider requests ➔ Status: `Pending`
   - Driver accepts ➔ Status: `Accepted`, seats reduced
   - Driver rejects ➔ Status: `Rejected`, seats preserved
   - Rider cancels ➔ Status: `Cancelled`, seats refunded if previously accepted
   - Driver completes ride ➔ Status: `Completed` (both ride and accepted bookings)
6. **Fare Calculation Engine:** Computes fair travel estimates using `Base Fare (₹30) + (Distance × ₹12/KM)` with driver manual override.
7. **Interactive Route Preview:** Integrated with open-source **Leaflet and OpenStreetMap** (zero paid APIs required; includes offline fallback).
8. **Responsive UI:** Clean design matching academic presentation standards, accessible on mobile, tablet, and desktop screens.

---

## 💻 Technologies Used

- **Backend:** Python 3.10+ / Python 3.14, Flask 3.x, Werkzeug (security & hashing)
- **Database:** SQLite (built-in relational SQL engine) & Supabase PostgreSQL compatible DDL schema
- **Frontend:** HTML5, CSS3 (Modern Flexbox & Grid, responsive variables), JavaScript (Fetch API, DOM manipulation)
- **Mapping:** Leaflet.js with OpenStreetMap (zero API keys required)
- **Testing:** Python `unittest` framework

---

## ⚙️ System Requirements

- Python 3.9 or higher (tested on Python 3.14)
- Web Browser (Chrome, Firefox, Edge, Safari)
- Internet connection (optional, only for loading Leaflet map tiles)

---

## 🚀 Installation & Setup

1. **Clone or Navigate to the project directory:**
   ```bash
   cd "sen project"
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Only `flask` and `werkzeug` are required!)*

3. **Run the Application:**
   ```bash
   python run.py
   ```
   *Or:*
   ```bash
   python app.py
   ```

4. **Access the application in your browser:**
   Open: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🗄️ Database Setup & Schema

The application automatically creates and initializes the SQLite relational database at `database/rideshare.db` upon first launch, runs `database/schema.sql`, and seeds realistic demo data.

For cloud deployments (such as Supabase PostgreSQL), a complete PostgreSQL schema with Row-Level Security (RLS) policies is included in `database/supabase_schema.sql`.

### Relational Entity Structure:
- `users`: Core identity table with hashed passwords, status, and role.
- `drivers`: 1-to-1 extension of `users` storing license and vehicle specifications.
- `rides`: 1-to-many child of `drivers` storing itineraries, date/time, seats, fare, and status.
- `bookings`: Join entity connecting `users` (riders) and `rides` with seat count, fare, and status.

---

## 🔑 Pre-Seeded Demo Accounts

For immediate academic evaluation without manual sign-up, the database is pre-populated with demo credentials (also selectable with 1-click on the Login page):

| Role | Email | Password | Details |
|:---|:---|:---|:---|
| **Rider** | `rider@demo.com` | `Rider@123` | Demo Rider (Aman Verma) with pre-seeded ride history |
| **Driver** | `driver@demo.com` | `Driver@123` | Demo Driver (Rahul Sharma) - Honda City Sedan (DL-03-AB-1020) |
| **Admin** | `admin@demo.com` | `Admin@123` | System Administrator with full moderation console |

---

## 🔄 Application Workflow

```
[Guest] 
   └── Browses Landing Page / Reviews Rides
   └── Registers as Rider or Driver (or uses 1-Click Demo Login)

[Rider Flow]
   └── Logs in ➔ Rider Dashboard
   └── Enters search: Pickup, Destination, Date, Vehicle Type, Seats
   └── Views matching ride cards with driver details and fare estimate
   └── Clicks "Request Ride" ➔ Booking created as "Pending"
   └── Tracks status on "My Bookings" (can cancel pending request)
   └── When journey completes ➔ Appears in "Ride History"

[Driver Flow]
   └── Logs in ➔ Driver Dashboard
   └── Posts Ride via "Create Ride" form (with live distance & fare calculator)
   └── Receives passenger booking in "Ride Requests"
   └── Clicks "Accept" (seats automatically deduct; marks "Full" if 0 remaining)
   └── Or clicks "Reject" (seats preserved)
   └── Clicks "Mark as Completed" upon reaching destination

[Admin Flow]
   └── Logs in ➔ Admin Dashboard
   └── Monitors platform metrics (total users, drivers, riders, rides, bookings)
   └── Toggles user active/inactive status
   └── Moderates / deletes invalid rides
```

---

## 💰 Fare Calculation Formula

The application uses an algorithmic distance calculation and fare formula:

$$\text{Estimated Fare} = \text{Base Fare} + (\text{Estimated Distance (km)} \times \text{Rate per KM})$$

- **Base Fare:** ₹30.00
- **Rate per KM:** ₹12.00
- **Example:** For a 5.8 km trip from *College Road* to *Railway Station*:  
  $$\text{Fare} = 30 + (5.8 \times 12) = 30 + 69.6 = ₹100 \text{ (approx)}$$

*Note: All fares are demo/simulated values for academic demonstration.*

---

## 🧪 Automated Testing (TC01–TC14)

Run the full automated test suite using Python's standard `unittest`:

```bash
python -m unittest tests/test_rideshare.py
```

### Verified Test Cases:
- **TC01:** Valid rider registration (Asserts record creation & active status)
- **TC02:** Invalid email registration (Asserts rejection of invalid email syntax)
- **TC03:** Valid user login (Asserts session creation and dashboard redirect)
- **TC04:** Invalid login (Asserts authentication failure and error message)
- **TC05:** Driver creates ride (Asserts ride listing creation with status 'Available')
- **TC06:** Rider searches ride (Asserts query filtering by location)
- **TC07:** Rider requests available ride (Asserts booking status 'Pending')
- **TC08:** Driver accepts booking (Asserts status 'Accepted' and seat decrement)
- **TC09:** Driver rejects booking (Asserts status 'Rejected' and seat preservation)
- **TC10:** Prevent overbooking (Asserts rejection when requested seats exceed capacity)
- **TC11:** Rider cancels booking (Asserts status 'Cancelled' and seat restitution)
- **TC12:** Driver completes ride (Asserts transition of ride & bookings to 'Completed')
- **TC13:** Unauthorized user access guard (Asserts redirection and access denial)
- **TC14:** User logout (Asserts session termination)

---

## 🔮 Future Scope

Possible extensions for future semesters or advanced coursework:
- Real-time GPS driver tracking via WebSockets
- Integrated SMS / Push notifications for ride confirmation
- Multi-stop route waypoints
- Driver and rider star ratings and reviews
- Payment gateway integration (Razorpay / Stripe)
- Emergency / SOS alerting system

---

## 👨‍💻 Academic Integrity Notice

This project was built strictly as an educational college-level Software Engineering mini project. It does not use copyrighted brand names, proprietary assets, or paid API keys.
