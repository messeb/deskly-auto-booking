# desk.ly Auto Booking

This project automates the booking of seats using the desk.ly API. It logs in with provided credentials, calculates the booking date based on the number of days from the current date, and attempts to book a seat.

## Features

- Automated seat booking
- Configurable booking date
- Error handling for common booking issues
- Scheduled execution using GitHub Actions

## Setup

### Prerequisites

- Python 3.x
- `pip` (Python package installer)
- `make` (optional, for using the Makefile)


### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/deskly-auto-booking.git
    cd deskly-auto-booking
    ```

2. Create a `.env` file (from `.env.example`) in the project directory with the following content:
    ```sh
    USERNAME=your_username
    PASSWORD=your_password
    SEAT_UUID=your_seat_uuid
    DAYS_UNTIL_BOOKING=5
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```


### Usage

1. Run the script:
    ```sh
    python3 seatbooking.py
    ```

    Alternatively, if you have make installed, you can use the Makefile:
    ```sh
    make install
    make run
    ```

### GitHub Actions Workflow

This project includes a GitHub Actions workflow that runs every weekday at 9:00 AM UTC. The workflow is defined in `.github/workflows/bookseat.yml`.

The workflow performs the following steps:

1. Checks out the repository
1. Sets up Python
1. Installs dependencies
1. Runs the script

#### Add Secrets to Your GitHub Repository

1. Navigate to Your Repository:
    - Go to your GitHub repository on the GitHub website.

1. Go to Settings:
    - Click on the `Settings` tab in your repository.

1. Access Secrets:
    - In the left sidebar, click on `Secrets and variables` > `Actions`.

1. Add New Secrets:
    - Click on the `New repository secret` button.
    - Add the following secrets one by one:
        - `USERNAME`: Your Deskly username.
        - `PASSWORD`: Your Deskly password.
        - `SEAT_UUID`: The UUID of the seat you want to book.
        - `DAYS_UNTIL_BOOKING`: The number of days from today until the booking date.

#### Makefile

The Makefile includes the following targets:

- `install`: Installs the required dependencies
- `run`: Runs the script


### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
