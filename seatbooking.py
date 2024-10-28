import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Define API host and endpoints
API_HOST = 'https://app.desk.ly/de/api'
LOGIN_ENDPOINT = f'{API_HOST}/authorize/accessToken'
BOOKING_ENDPOINT = f'{API_HOST}/booking'

def load_env():
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    seat_uuid = os.getenv('SEAT_UUID')
    days_until_booking = int(os.getenv('DAYS_UNTIL_BOOKING', 0))
    return username, password, seat_uuid, days_until_booking

def login(username, password):
    # Login payload
    login_payload = {
        'username': username,
        'password': password
    }

    # Perform login request
    response = requests.post(LOGIN_ENDPOINT, json=login_payload)
    response_data = response.json()

    # Extract values from response
    token = response_data.get('token')
    user_id = response_data['data']['user']['id']

    return token, user_id

def book(token, user_id, seat_uuid, booking_date):
    # Form data payload
    form_data = {
        "booking[seatDayBookings][0][from]": "08:00:00",
        "booking[seatDayBookings][0][until]": "18:00:00",
        "booking[seatDayBookings][0][date]": booking_date,
        "booking[seatDayBookings][0][seat]": seat_uuid,
        "booking[email]": "false",
        "booking[bookedFor]": user_id
    }

    # Headers with token
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Perform booking request
    booking_response = requests.post(BOOKING_ENDPOINT, data=form_data, headers=headers)
    booking_response_data = booking_response.json()

    # Handle response
    if booking_response.status_code == 201:
        print("Booking successful:", booking_response_data)
    elif booking_response.status_code == 400:
        error_type = booking_response_data.get('type')
        if error_type == 'booking.invalid.ly':
            print("Booking conflict:", booking_response_data['data']['errors'])
        elif error_type == 'form.invalid.ly':
            print("Form error:", booking_response_data['data']['formErrors'])
        else:
            print("Unknown error:", booking_response_data)
    elif booking_response.status_code == 401:
        print("Authentication error:", booking_response_data['detail'])
    else:
        print("Unexpected error:", booking_response_data)

    return booking_response_data

def book_seat(username, password, seat_uuid, days_until_booking):
    token, user_id = login(username, password)
    booking_date = (datetime.now() + timedelta(days=days_until_booking)).strftime('%Y-%m-%d')
    booking_response_data = book(token, user_id, seat_uuid, booking_date)
    print(booking_response_data)

if __name__ == "__main__":
    username, password, seat_uuid, days_until_booking = load_env()
    book_seat(username, password, seat_uuid, days_until_booking)
