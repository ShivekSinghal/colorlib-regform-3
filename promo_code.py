import json
import random
from datetime import datetime, timedelta

def generate_random_promo_code(length=8):
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))


def check_promo_validity(filename):
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)

        expiry_date = datetime.strptime(data["expiry"], "%Y-%m-%d %H:%M:%S")
        if expiry_date >= datetime.now():
            return True
        else:
            return False
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return False

def create_promo_json(name, email, phone,amount,promo_code,dropin_date, filename):
    promo_code = promo_code
    today = datetime.strptime(dropin_date, "%Y-%m-%d")  # Convert dropin_date to datetime with just the date part
    expiry = today + timedelta(hours=23, minutes=59, seconds=59)

    data = {
        "promo_code": promo_code,
        "expiry": expiry.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "email": email,
        "phone": phone,
        "amount": amount
    }
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def apply_promo_code(name, email, phone, promo_code, filename):
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)

        if data["name"] == name and data["email"] == email and data["phone"] == phone:
            if check_promo_validity(filename):
                if data["promo_code"] == promo_code:

                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return False
