
import smtplib
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, flash
import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from premailer import transform
from datetime import datetime
from PIL import Image
import base64
from email.mime.image import MIMEImage
from ccavutil import encrypt, decrypt
import json
import random
from datetime import datetime, timedelta

# import hmac
# import hashlib

app = Flask(__name__)

# Google Sheets API credentials
scopes = ['https://www.googleapis.com/auth/spreadsheets']

# Load the credentials from the JSON key file
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scopes)
client = gspread.authorize(credentials)

os.environ['SHEET_KEY'] = '1cJdiWjKzOMK6kVkPWBfhBVGTy_bsxDBwDbwlagkQfY4'
os.environ['SHEET_NAME'] = 'Sheet1'
os.environ['WORKING_KEY'] = "868E43E034DB2953A9E18EC401CA3268	"
os.environ['ACCESS_CODE'] = "AVKR14KI19BL44RKLB"
os.environ['MERCHANT_ID'] = "2538003"
os.environ['THREE_MONTHS_VALIDITY'] = "false"
os.environ['GRID_VALIDITY'] = "false"

# Environment variables with values in the desired format
os.environ['PRIYANSHI_PASSWORD'] = "priyanshi_password"
os.environ['KAJAL_PASSWORD'] = "kajal_password"
os.environ['JHILMIL_PASSWORD'] = "jhilmil_password"
os.environ['RUBANI_PASSWORD'] = "rubani_password"
os.environ['JAHNVI_PASSWORD'] = "jahnvi_password"
os.environ['MUSKAN_PASSWORD'] = "muskan_password"
os.environ['TARUN_PASSWORD'] = "tarun_password"

# Google Sheet details
sheet_key = os.environ.get('SHEET_KEY')
sheet_name = os.environ.get('SHEET_NAME')

#PROMO CODE HANDLER


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
                print("applied")
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



##

# Razorpay payment gateway credentials
# razorpay_key_id = 'rzp_test_9Yy2azW5HeczxN'
# razorpay_key_secret = 'QhcRWMasciGh2iZUhNe6m786'

# Create a Razorpay client
# razorpay_client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))

# Your Cc avenue API credentials


workingKey = os.environ.get("WORKING_KEY")
accessCode = os.environ.get("ACCESS_CODE")



# Receipt Number Generation

def get_current_receipt_number():
    # Code to retrieve the current receipt number from storage (file or database)
    # Return the current receipt number as an integer
    # Example: read from a file
    with open("receipt_number.txt", "r") as file:
        current_receipt_number = int(file.read())
    return str(current_receipt_number)


# Increment Receipt number

def increment_receipt_number():
    # Get the current receipt number
    current_receipt_number = int(get_current_receipt_number())

    # Increment the receipt number by one
    new_receipt_number = current_receipt_number + 1

    # Update the storage with the new receipt number
    # Example: write to a file
    with open("receipt_number.txt", "w") as file:
        file.write(str(new_receipt_number))

    # Return the new receipt number
    return str(new_receipt_number)

def increment_receipt_number():
    # Get the current receipt number
    current_receipt_number = int(get_current_receipt_number())

    # Increment the receipt number by one
    new_receipt_number = current_receipt_number + 1

    # Update the storage with the new receipt number
    # Example: write to a file
    with open("receipt_number.txt", "w") as file:
        file.write(str(new_receipt_number))

    # Return the new receipt number
    return str(new_receipt_number)


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_receipt(receiver_mail, rendered_html):
    my_email = "singhalshivek24@gmail.com"
    password = 'lzjkbgcrngzalkhc'
    smtp_server = "smtp.gmail.com"
    email_subject = "Registration Receipt Sep'23"
    smtp_port = 587

    inlined_html = transform(rendered_html)

    msg = MIMEMultipart()
    msg["From"] = my_email
    msg["To"] = receiver_mail
    msg["Subject"] = email_subject

    body = MIMEText(inlined_html, "html")
    msg.attach(body)
    with open('./static/images/Hashtag_logo.png', 'rb') as image_file:
        image = MIMEImage(image_file.read())
        image.add_header('Content-ID', '<logo_image>')
        msg.attach(image)
    with open('./static/images/phone.png', 'rb') as image_file:
        image_phone = MIMEImage(image_file.read())
        image_phone.add_header('Content-ID', '<phone>')
        msg.attach(image_phone)
    with open('./static/images/whatsapp.png', 'rb') as image_file:
        image_whatsapp = MIMEImage(image_file.read())
        image_whatsapp.add_header('Content-ID', '<whatsapp>')
        msg.attach(image_whatsapp)
    with open('./static/images/instagram.png', 'rb') as image_file:
        image_instagram = MIMEImage(image_file.read())
        image_instagram.add_header('Content-ID', '<instagram>')
        msg.attach(image_instagram)

    with open('./static/images/email.png', 'rb') as image_file:
        image_email = MIMEImage(image_file.read())
        image_email.add_header('Content-ID', '<email>')
        msg.attach(image_email)

    with open('./static/images/pink.png', 'rb') as image_file:
        image_watermark = MIMEImage(image_file.read())
        image_watermark.add_header('Content-ID', '<watermark>')
        msg.attach(image_watermark)

    with smtplib.SMTP(smtp_server, smtp_port) as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.send_message(msg)


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_image


# Dictionary of name-password pairs

name_password_pairs = dict(Priyanshi=os.environ.get("PRIYANSHI_PASSWORD"), Kajal=os.environ.get("KAJAL_PASSWORD"), Jhilmil=os.environ.get("JHILMIL_PASSWORD"),
                           Rubani=os.environ.get("RUBANI_PASSWORD"), Jahnvi=os.environ.get("JAHNVI_PASSWORD"), Muskan=os.environ.get("MUSKAN_PASSWORD"),
                           Tarun=os.environ.get("TARUN_PASSWORD"))


@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)


# Drop In
@app.route('/dropin', methods=['GET', 'POST'])
def registration_form_dropin():
    return render_template('dropin.html')


@app.route('/dropinbatch', methods=['GET', 'POST'])
def select_dropin():
    global name, phone, email, studio
    three_months_validty = os.environ.get('THREE_MONTHS_VALIDITY')
    grid_validity = os.environ.get('GRID_VALIDITY')
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    studio = request.form['Studio']

    if studio in ["Noida", "Rajouri Garden", "Pitampura"]:
        batch_scenario = "twice"


    elif studio in ["Gurgaon", "South Delhi", "Indirapuram"]:
        batch_scenario = "heels_once"

    else:
        batch_scenario = "once"

    return render_template('selectdropin.html', dropin_studio=studio, batch_scenario=batch_scenario, three_months_validty=three_months_validty,grid_validity=grid_validity)


# Registration Form


@app.route('/', methods=['GET', 'POST'])
def registration_form():

    return render_template('index.html')




#
# @app.route('/payment_mode',methods=['GET', 'POST'])
# def payment_method():
@app.route('/batch', methods=['GET', 'POST'])
def select_batch():
    global name, phone, email, studio, promo_code_applied, batch_scenario

    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    studio = request.form['Studio']
    promo_code_applied = request.form['promo']



    batch_scenario = ""
    if studio in ["Noida", "Rajouri Garden", "Pitampura"]:
        batch_scenario = "twice"


    elif studio in ["Gurgaon", "South Delhi", "Indirapuram"]:
        batch_scenario = "heels_once"

    else:
        batch_scenario = "once"

    promo_data = load_promo_data("promo_data.json")
    if promo_data is not None:
        discount = int(apply_promo_code(name, email, phone, promo_code_applied, filename="promo_code.json"))
        if promo_code_applied == "":
            discount = 0
            return render_template('selectbatch.html', batch_scenario=batch_scenario, discount=discount)

        if discount > 0:
            print(discount)
            # with open("promo_code.json", 'r') as json_file:
            #     data = json.load(json_file)
            #     discount = 0

            #     for item in data:
            #         if isinstance(item, dict) and 'promo_code' in item and item['promo_code'] == promo_code:
            #             if 'amount' in item:
            #                 discount = item['amount']
            #                 print(discount)
            #             break

            return render_template('selectbatch.html', batch_scenario=batch_scenario, discount=discount, promo_message=f"Promo Code worth {discount} applied successfully")
        if discount == 0:
            return render_template('selectbatch.html', batch_scenario=batch_scenario, discount=discount, promo_message=f"Promo Code expired or invalid user details")


@app.route('/payment', methods=['GET', 'POST'])
def make_payment():
    print(request.form['fee'])
    if request.form['fee'] == 0 or request.form['fee'] == "":
        print("Cancelled")
        return redirect(url_for('select_batch'))
        flash("Select 1 batch")
    else:

        global order_response, batches, fee, order_receipt, paid_to, validity, p_order_id, dropin_date, fee_without_gst
        order_receipt = get_current_receipt_number()  # Replace with your own logic to generate a unique order receipt ID
        p_merchant_id = os.environ.get('MERCHANT_ID')
        p_order_id = f"order_{order_receipt}"
        p_currency = 'INR'
        p_redirect_url = url_for('payment_successful')
        p_cancel_url = url_for('payment_failed')

        batches = request.form.getlist('batch[]')
        fee_without_gst = request.form['fee']
        fee = str(round(float(fee_without_gst)*1.18))
        paid_to = "Pink Grid"
        validity = request.form['validity']
        merchant_data = 'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + fee + '&' + 'redirect_url=' + p_redirect_url + '&' + 'cancel_url=' + p_cancel_url + '&'
        encryption = encrypt(merchant_data, workingKey)
        if validity == "two_months_grid":
            validity = "August, September, Grid 2.0"
        if validity == "three_months":
            validity = "August, September, December"
        if validity == "grid":
            validity = "Grid 2.0"
        if validity == "Drop In":
            dropin_date = request.form['dropin_date']
            batch = request.form['batch']
            batches = batch
            print(batches)


        # Get the selected batches as a list

        #     # Create a new order in Razorpay
        # order_amount = int(float(fee) * 100)  # Convert fee to the smallest currency unit (in paisa)
        # order_currency = 'INR'
        #
        # order_data = {
        #         'amount': order_amount,
        #         'currency': order_currency,
        #         'receipt': order_receipt,
        #         'payment_capture': 1,  # Auto-capture the payment
        #         # Add any other parameters as required
        #     }
        #
        # order_response = razorpay_client.order.create(data=order_data)
        #
        # if order_response.get('id'):
        #     order_id = order_response['id']
        #
        #     # Redirect the user to the Razorpay payment page
        #     return render_template("pay.html", payment=order_response)
        # else:
        #     # Failed to create the order
        #     return render_template('failed.html')


        return render_template('pay.html', mid=p_merchant_id, encReq=encryption, order_id=p_order_id, xscode=accessCode)


@app.route('/cash_payment', methods=['GET', 'POST'])
def cash_payment():
    return render_template('cash.html', fee=fee)


@app.route('/process_cash', methods=['GET', 'POST'])
def process_cash():
    if request.method == "POST":
        global wingperson_name
        wingperson_name = request.form.get('wingperson_name')
        password = request.form.get('password')
        mode_of_payment = "Cash"

        if wingperson_name in name_password_pairs and password == name_password_pairs[wingperson_name]:
            # Password verification succeeded
            return redirect(url_for('payment_successful', source=mode_of_payment))
        else:
            # Password verification failed
            return redirect(url_for('payment_failed'))

    else:
        return render_template("cash.html")


@app.route('/success', methods=['GET', 'POST'])
def payment_successful():
    request.form.get('')
    sheet = client.open_by_key(sheet_key).worksheet(sheet_name)
    batch_str = ', '.join(batches)  # Join the batches list with a comma separator
    today_date = datetime.today().strftime('%d-%b-%Y')
    source = request.args.get('source')
    if source == "Cash":
        mode_of_payment = "Cash"
        paid_to = wingperson_name

    else:
        mode_of_payment = "Bank Transfer"
        paid_to = "Pink Grid"

    if validity == "Drop In":
        batch_str = batches
        promo_data = load_promo_data("promo_code.json")

        # if promo_data is not None:

        promo_code = create_promo_json(name, email, phone, fee_without_gst, dropin_date, "promo_code.json")


    else:
        remove_promo_code(name, email, phone, promo_code_applied, filename="promo_code.json")

        promo_code = "N/A"


    print(source)

    row = [today_date, name, phone, email, "#" + order_receipt, validity, batch_str, fee, p_order_id, studio,
           mode_of_payment, paid_to, promo_code]
    gross_amount = round(float(fee) / 1.18, 2)
    gst = round(gross_amount * 0.18, 2)

    hashtag_logo = image_to_base64('./static/images/Hashtag_logo.png')
    hashtag_watermark = image_to_base64('./static/images/pink.png')
    increment_receipt_number()

    sheet.append_row(row)
    print("Succesfully added to sheets")

    rendered_receipt = render_template("receipt2.html", date=today_date, name=name, batch=batch_str, phone=phone,
                                       validity=validity, email=email, studio=studio, gross_amount=gross_amount,
                                       gst=gst, fee=fee, order_receipt=f"#{str(order_receipt)}",
                                       mode_of_payment=mode_of_payment, paid_to=paid_to, hashtag_logo=hashtag_logo,
                                       watermark=hashtag_watermark, promo_code=promo_code)

    send_receipt(receiver_mail=email, rendered_html=rendered_receipt)
    return render_template("success.html")


@app.route('/terms')
def terms_and_conditions():
    return render_template("terms.html")


@app.route('/failed', methods=['GET', 'POST'])
def payment_failed():
    return render_template('failed.html')


if __name__ == '__main__':
    app.run(debug=True, port=4900)
