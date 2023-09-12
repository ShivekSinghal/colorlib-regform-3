import json
import random
from datetime import datetime, timedelta
import os

def generate_random_promo_code(length=8):
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))

def load_promo_data(filename):
    try:
        if not os.path.exists(filename):
            return []  # Return an empty list if the file doesn't exist

        with open(filename, 'r') as json_file:
            promo_data = json.load(json_file)

        # Ensure that promo_data is a list, or initialize an empty list
        if not isinstance(promo_data, list):
            promo_data = []

        return promo_data

    except (FileNotFoundError, json.JSONDecodeError):
        return []

def check_promo_validity(expiry_date):
    try:
        return expiry_date >= datetime.now()
    except ValueError:
        return False  # Handle invalid date format

def create_promo_json(name, email, phone, amount, dropin_date, filename):
    promo_code = generate_random_promo_code()
    today = datetime.strptime(dropin_date, "%Y-%m-%d")
    expiry = today + timedelta(hours=23, minutes=59, seconds=59)

    promo_entry = ({
        "promo_code": promo_code,
        "expiry": expiry.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "email": email,
        "phone": phone,
        "amount": amount
    })

    promo_data = load_promo_data(filename)
    promo_data.append(promo_entry)

    with open(filename, 'w') as json_file:
        json.dump(promo_data, json_file, indent=4)

    return promo_code  # Return the generated promo code

def apply_promo_code(name, email, phone, promo_code, filename):
    try:
        promo_data = load_promo_data(filename)

        for promo_entry in promo_data:
            if (
                promo_entry.get("name") == name
                and promo_entry.get("email") == email
                and promo_entry.get("phone") == phone
                and promo_entry.get("promo_code") == promo_code
                and check_promo_validity(datetime.strptime(promo_entry["expiry"], "%Y-%m-%d %H:%M:%S"))
            ):

                return promo_entry.get('amount')
            else:
                return 0

        return 0  # No matching or valid promo code found

    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return False  # Handle exceptions gracefully

def remove_promo_code(name, email, phone, promo_code, filename):
    promo_data = load_promo_data(filename)

    for promo_entry in promo_data:
        if (
                promo_entry.get("name") == name
                and promo_entry.get("email") == email
                and promo_entry.get("phone") == phone
                and promo_entry.get("promo_code") == promo_code
                and check_promo_validity(datetime.strptime(promo_entry["expiry"], "%Y-%m-%d %H:%M:%S"))
        ):
            promo_data.remove(promo_entry)

            with open(filename, 'w') as json_file:
                json.dump(promo_data, json_file, indent=4)