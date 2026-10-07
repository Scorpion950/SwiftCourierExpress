"""Tracking number generation utilities."""

import random
from datetime import datetime


def generate_tracking_number():
    """Return a unique tracking number in the required format."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    suffix = f"{random.randint(10, 99):02d}"
    return f"TRK{timestamp}{suffix}"
