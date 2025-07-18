import random
from datetime import datetime, timedelta

def generate_otp(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def get_expiry(minutes=5):
    return datetime.utcnow() + timedelta(minutes=minutes)
