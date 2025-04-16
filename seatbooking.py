"""
Deskly Auto Booking Script

This script automates the process of booking seats using the desk.ly API. It logs in with provided credentials,
calculates the booking date based on the number of days from the current date, and attempts to book a seat.
It includes error handling for common booking issues and supports scheduled execution using GitHub Actions.

Environment Variables:
    USERNAME (str): Deskly username.
    PASSWORD (str): Deskly password.
    SEAT_UUID (str): UUID of the seat to book.
    DAYS_UNTIL_BOOKING (int): Number of days from today until the booking date.
"""

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

# Define global variables for booking times on a working day
BOOKING_FROM_TIME = "08:00:00"
BOOKING_UNTIL_TIME = "18:00:00"

def load_env():
    """
    Load environment variables and validate them.

    Returns:
        tuple: A tuple containing username, password, seat_uuid, and days_until_booking.

    Raises:
        ValueError: If one or more environment variables are not set.
    """
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    seat_uuid = os.getenv('SEAT_UUID')
    days_until_booking = os.getenv('DAYS_UNTIL_BOOKING')

    # Check if any environment variable is not set
    if not all([username, password, seat_uuid, days_until_booking]):
        raise ValueError("One or more environment variables are not set")

    days_until_booking = int(days_until_booking)
    return username, password, seat_uuid, days_until_booking

def login(username, password):
    """
    Perform login to desk.ly API and retrieve token and user id.

    Args:
        username (str): desk.ly username.
        password (str): desk.ly password.

    Returns:
        tuple: A tuple containing the token and user id.
    """
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
    """
    Perform the booking request to Deskly API.

    Args:
        token (str): Authorization token.
        user_id (str): User ID.
        seat_uuid (str): UUID of the seat to book.
        booking_date (str): Date of the booking in YYYY-MM-DD format.

    Returns:
        dict: The response data from the booking request.
    """
    # Booking seat form data payload
    form_data = {
        'booking[seatDayBookings][0][from]': (None, BOOKING_FROM_TIME),
        'booking[seatDayBookings][0][until]': (None, BOOKING_UNTIL_TIME),
        'booking[seatDayBookings][0][date]': (None, booking_date),
        'booking[seatDayBookings][0][seat]': (None, seat_uuid),
        'booking[email]': (None, 'false'),
        'booking[bookedFor]': (None, user_id),
    }

    # Auth header with token
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Perform booking request
    booking_response = requests.post(BOOKING_ENDPOINT, files=form_data, headers=headers)
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
    """
    Book a seat using the Deskly API.

    Args:
        username (str): Deskly username.
        password (str): Deskly password.
        seat_uuid (str): UUID of the seat to book.
        days_until_booking (int): Number of days from today until the booking date.
    """
    token, user_id = login(username, password)
    booking_date = (datetime.now() + timedelta(days=days_until_booking)).strftime('%Y-%m-%d')
    booking_response_data = book(token, user_id, seat_uuid, booking_date)
    print(booking_response_data)

if __name__ == "__main__":
    try:
        username, password, seat_uuid, days_until_booking = load_env()
        book_seat(username, password, seat_uuid, days_until_booking)
    except ValueError as e:
        print(f"Error: {e}")