# Gacha Game

## Description

Gacha Game is a web application built with Django that allows users to register, log in, and participate in a "spin" feature to receive virtual ducks with varying rarities. Users can have multiple copies of the same duck, and the game simulates a gacha-style experience where players can collect and manage their ducks.

## Features

- User registration and authentication (login/logout)
- Spin feature to receive random ducks
- Collection of ducks with different rarities
- Admin interface to manage ducks
- Responsive design

## Technologies Used

- Python 3.x
- Django 5.1.2
- Django REST Framework
- SQLite (or any other database of your choice)
- HTML/CSS for front-end

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your machine
- pip (Python package installer)
- Virtual environment (optional but recommended)

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/gacha-game.git
   cd gacha-game

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv

3. **Activate the virtual environment:**

- On Windows:
   ```bash
   venv\Scripts\activate
   
- On macOS/Linux:
   ```bash
   source venv/bin/activate
   
4. **Install the required packages:**

   ```bash
   pip install django djangorestframework Pillow

5. **Set up the database:**
   Run the following command to create the database:

   ```bash
   python manage.py migrate

6. **Create a superuser (for accessing the admin panel):**

   ```bash
   python manage.py createsuperuser

7. **Run the development server:**

   ```bash
   python manage.py runserver


8. **Access the application:**
Open your web browser and navigate to http://127.0.0.1:8000/.

## Usage

1. Register a new user: Navigate to the /register/ page to create a new account.
2. Log in: Use your credentials to log in to the application at the /login/ page.
3. Spin for ducks: After logging in, go to your profile at /profile/ and click on the "Spin for a Duck!" button to receive a random duck.
4. View your ducks: Your collected ducks will be displayed on your profile page.

## Admin Panel

To manage ducks and view users:

1. Go to http://127.0.0.1:8000/admin/.
2. Log in using the superuser credentials created earlier.
3. Manage Duck and UserDuck entries through the admin interface.

## Images

To add images for ducks, place them in the media/ducks/ directory (or the directory specified in your models.py).
