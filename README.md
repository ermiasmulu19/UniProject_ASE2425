# **Gacha Game**

## **Description**

Gacha Game is a Django-based web application. Users can register, log in, and spin to collect virtual ducks with varying rarities. The game allows for collecting, managing, and viewing multiple ducks in a fun, randomized manner.

---

## **Features**

- User registration and authentication.
- Randomized "spin" feature to collect ducks.
- Ducks categorized by rarity (common, rare, etc.).
- Ability to own multiple copies of the same duck.
- Admin panel for duck and user management.

---

## **Technologies Used**

- **Backend:** Python 3.x, Django 5.1.2, Django REST Framework
- **Database:** SQLite
- **Frontend:** HTML, CSS
- **Other:** Docker (optional for containerization)

---

## **Prerequisites**

Ensure you have the following installed:

- Python 3.x
- pip (Python package installer)
- Docker (optional, if you prefer to use containerization)

---

## **Installation (Local Environment)**

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
Open your web browser and navigate to http://127.0.0.1:8000/login



## **Installation with Docker**

1. **Build the Docker image:**

   ```bash
   docker build -t gacha-game .

2. **Run the container:**

   ```bash
   docker run -p 8000:8000 gacha-game

8. **Access the application:**
Open your web browser and navigate to http://127.0.0.1:8000/login

## **Usage**

1. **Register a new account:** Go to /register/ to sign up.
2. **Log in:** Use your credentials at /login/.
3. **Spin for ducks:** After logging in, visit /profile/ and click "Spin for a Duck!" to collect a random duck.
4. **View your collection:** Your ducks will be displayed on the profile page.

## **Admin Panel**

To manage ducks and view users:

1. Visit http://127.0.0.1:8000/admin/.
2. Log in with the superuser credentials created earlier.
3. Use the admin interface to manage ducks and user data.

## **Images**

Duck images should be added to the media/ducks/ directory (or as specified in your models.py).
Ensure the MEDIA_URL and MEDIA_ROOT settings in settings.py are properly configured.
