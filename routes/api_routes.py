from flask import Blueprint, request, jsonify
from services.fare_service import FareService

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/fare/calculate', methods=['GET', 'POST'])
def calculate_fare():
    """API endpoint to calculate estimated fare based on distance or pickup/destination."""
    data = request.get_json(silent=True) or request.args
    pickup = data.get('pickup', '').strip()
    destination = data.get('destination', '').strip()
    distance_str = data.get('distance')

    if distance_str:
        try:
            distance = float(distance_str)
        except ValueError:
            return jsonify({'error': 'Invalid distance value'}), 400
    else:
        distance = FareService.estimate_distance(pickup, destination)

    result = FareService.calculate_fare(distance)
    return jsonify(result)

@api_bp.route('/locations', methods=['GET'])
def get_locations():
    """Return common landmark locations for autocompletion."""
    locations = [
        "College Road",
        "Railway Station",
        "Bus Stand",
        "City Center",
        "Tech Park",
        "Airport",
        "University Campus",
        "Central Mall",
        "Metro Station Gate 2",
        "Civil Hospital",
        "Gandhi Chowk"
    ]
    return jsonify({'locations': locations})
