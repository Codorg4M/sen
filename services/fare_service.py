import math
import hashlib

class FareService:
    """Service to calculate and estimate ride fares for the RideShare system."""

    DEFAULT_BASE_FARE = 30.0    # ₹30 Base Fare
    DEFAULT_RATE_PER_KM = 12.0  # ₹12 per km

    # Known landmark distances (in KM) for demo convenience
    DEMO_DISTANCES = {
        ('college road', 'railway station'): 5.8,
        ('railway station', 'college road'): 5.8,
        ('bus stand', 'city center'): 4.2,
        ('city center', 'bus stand'): 4.2,
        ('tech park', 'airport'): 26.5,
        ('airport', 'tech park'): 26.5,
        ('university campus', 'central mall'): 5.0,
        ('central mall', 'university campus'): 5.0,
        ('railway station', 'airport'): 18.0,
        ('airport', 'railway station'): 18.0,
    }

    @classmethod
    def estimate_distance(cls, pickup: str, destination: str) -> float:
        """
        Estimate distance in km between two locations.
        Uses lookup for common college project landmarks, or deterministic heuristic for demo locations.
        """
        if not pickup or not destination:
            return 5.0

        p = pickup.strip().lower()
        d = destination.strip().lower()

        # Check predefined routes
        if (p, d) in cls.DEMO_DISTANCES:
            return cls.DEMO_DISTANCES[(p, d)]

        # Deterministic pseudo-distance for any custom user input (between 3.0 and 25.0 km)
        combined = f"{p}->{d}".encode('utf-8')
        digest = int(hashlib.md5(combined).hexdigest()[:6], 16)
        simulated_km = round(3.5 + (digest % 215) / 10.0, 1)
        return simulated_km

    @classmethod
    def calculate_fare(cls, distance_km: float, base_fare: float = None, rate_per_km: float = None) -> dict:
        """
        Calculate fare using formula:
        Estimated Fare = Base Fare + (Estimated Distance × Rate Per KM)
        """
        base = base_fare if base_fare is not None else cls.DEFAULT_BASE_FARE
        rate = rate_per_km if rate_per_km is not None else cls.DEFAULT_RATE_PER_KM

        distance = max(1.0, float(distance_km))
        distance_charge = distance * rate
        total_fare = round(base + distance_charge, 2)

        return {
            'distance_km': round(distance, 1),
            'base_fare': round(base, 2),
            'rate_per_km': round(rate, 2),
            'estimated_fare': total_fare,
            'disclaimer': 'Estimated Fare: ₹' + str(total_fare) + ' (Project / Demo Calculation)'
        }
