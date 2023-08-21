import smtplib

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from oauth2client.service_account import ServiceAccountCredentials
import razorpay
import gspread
from premailer import transform
from datetime import datetime
from PIL import Image
import base64
from email.mime.image import MIMEImage
from cashfree_sdk.payouts import Payouts




import hmac
import hashlib

app = Flask(__name__)

# Google Sheets API credentials
scopes = ['https://www.googleapis.com/auth/spreadsheets']

# Load the credentials from the JSON key file
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scopes)
client = gspread.authorize(credentials)

# Google Sheet details
sheet_key = '1cJdiWjKzOMK6kVkPWBfhBVGTy_bsxDBwDbwlagkQfY4'
sheet_name = 'Sheet1'

# Razorpay payment gateway credentials
razorpay_key_id = 'rzp_test_9Yy2azW5HeczxN'
razorpay_key_secret = 'QhcRWMasciGh2iZUhNe6m786'

# Create a Razorpay client
razorpay_client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))


# Your Cashfree API credentials
cashfree_app_id = 'TEST43522824da29604a286cb40521822534'
cashfree_secret_key = 'TEST613bfce859f23cd24f50d9664812fb224423c712'



Payouts.init(cashfree_app_id, cashfree_secret_key, "TEST")

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

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_receipt(receiver_mail, rendered_html):

    my_email = "singhalshivek24@gmail.com"
    password = "lzjkbgcrngzalkhc"
    smtp_server= "smtp.gmail.com"
    smtp_port = 587


    inlined_html = transform(rendered_html)

    msg = MIMEMultipart()
    msg["From"] = my_email
    msg["To"] = receiver_mail
    msg["Subject"] = "Test Email"

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
name_password_pairs = {
    'Priyanshi': 'priyanshi_password',
    'Kajal': 'kajal_password',
    'Jhilmil': 'jhilmil_password',
    'Rubani': 'rubani_password',
    'Jahnvi': 'jahnvi_password',
    'Muskan': 'muskan_password',
    'Tarun': 'tarun_password',


}




@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)




@app.route('/', methods=['GET', 'POST'])
def registration_form():
    return render_template('index.html')
#
# @app.route('/payment_mode',methods=['GET', 'POST'])
# def payment_method():
@app.route('/batch', methods=['GET', 'POST'])
def select_batch():
    global name, phone, email, studio

    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    studio = request.form['Studio']
    batch_scenario = ""
    if studio in ["Noida", "Rajouri Garden", "Pitampura"]:
        batch_scenario = "twice"


    elif studio in ["Gurgaon", "South Delhi", "Indirapuram"]:
        batch_scenario = "heels_once"

    else:
        batch_scenario = "once"

    print(studio)

    print(batch_scenario)



    return render_template('selectbatch.html', batch_scenario=batch_scenario)


@app.route('/payment', methods=['GET', 'POST'])
def make_payment():
    global order_response, batches, fee, order_receipt, order_id, paid_to, validity


    fee = request.form['fee']
    batches = request.form.getlist('batch[]')
    paid_to = "Pink Grid"
    validity = request.form['validity']

    if validity == "two_months_grid":
        validity = "August, September, Grid 2.0"

    if validity == "three_months":
        validity = "August, September, December"
    if validity == "grid":
        validity = "Grid 2.0"


        # Get the selected batches as a list


        # Create a new order in Razorpay
    order_amount = int(float(fee) * 100)  # Convert fee to the smallest currency unit (in paisa)
    order_currency = 'INR'
    order_receipt = get_current_receipt_number()  # Replace with your own logic to generate a unique order receipt ID

    order_data = {
            'amount': order_amount,
            'currency': order_currency,
            'receipt': order_receipt,
            'payment_capture': 1,  # Auto-capture the payment
            # Add any other parameters as required
        }

    order_response = razorpay_client.order.create(data=order_data)

    if order_response.get('id'):
        order_id = order_response['id']

        # Redirect the user to the Razorpay payment page
        return render_template("pay.html", payment=order_response)
    else:
        # Failed to create the order
        return render_template('failed.html')

@app.route('/cash_payment', methods=['GET','POST'])
def cash_payment():
    return render_template('cash.html')


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

    else :
        mode_of_payment = "Bank Transfer"
        paid_to = "Pink Grid"

    print(source)







    row = [today_date, name, phone, email,batch_str, fee, "#" + order_receipt,validity, order_id, studio,mode_of_payment, paid_to]
    gross_amount = round(float(fee)/1.18, 2)
    gst = round(gross_amount*0.18, 2)

    hashtag_logo = image_to_base64('./static/images/Hashtag_logo.png')
    hashtag_watermark = image_to_base64('./static/images/pink.png')

    sheet.append_row(row)
    print("Succesfully added to sheets")

    increment_receipt_number()
    rendered_receipt =render_template("receipt2.html",date=today_date, name=name, batch=batch_str, phone=phone,validity=validity, email=email, studio=studio, gross_amount=gross_amount, gst=gst, fee=fee, order_receipt=f"#{str(order_receipt)}",mode_of_payment=mode_of_payment, paid_to=paid_to, hashtag_logo=hashtag_logo, watermark=hashtag_watermark)

    send_receipt(receiver_mail=email,rendered_html=rendered_receipt)
    return render_template("success.html")

@app.route('/terms')
def terms_and_conditions():
    return render_template("terms.html")

@app.route('/failed', methods=['GET','POST'])
def payment_failed():
    return render_template('failed.html')

if __name__ == '__main__':
    app.run(debug=True, port=4900)
