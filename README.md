# **🦆 Gacha Game 🦆**

## **Description**

Gacha Game is a web application designed with a microservices architecture. Users can register, log in, and spin to collect virtual ducks with varying rarities. The game features functionalities to collect, manage, and view ducks in an engaging and randomized manner. Now, it includes enhanced backend capabilities and containerized deployment for ease of use.

---

## **Features**

- User registration and authentication.
- Randomized "spin" feature to collect ducks.
- Ducks categorized by rarity (common, rare, etc.).
- Ability to own multiple copies of the same duck.
- Auctions for trading ducks with other players.
- Admin panel for managing ducks, users, and auctions.

---

## **Technologies Used**

- **Backend:** Python 3.x, Django, Django REST Framework
- **Microservices:** Separate services for players, ducks, users, and auctions.
- **Database:** SQLite, PostgreSQL
- **Other:** Docker (required for deployment)

---

## **Prerequisites**

Ensure you have the following installed:

- Docker
- Docker Compose

---

## **Installation (Local Environment)**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/gacha-game.git
   cd gacha-game

2. **Set up environment variables:**
   Create a .env file in the root directory with the following content:

   ```bash
   POSTGRES_DB=gacha
   POSTGRES_USER=gachadb
   POSTGRES_PASSWORD=gachadb
   DB_HOST=db
   DB_PORT=5432

3. **Build and run the application:**

   ```bash
   docker-compose up --build
   
4. **Access the application:**

- Web application: http://0.0.0.0:8001/login/

5. **Stop the application:**

   ```bash
   docker-compose down


## **Usage**

1. **Register a new account:** Visit /register/ to sign up.
2. **Log in:** Use your credentials at /login/.
3. **Spin for ducks:** After logging in, visit /profile/ and click "Spin for a Duck!" to collect a random duck.
4. **View your collection:** Your ducks will be displayed on the profile page.
5. **Participate in auctions:** Use the /auctions/ page to trade ducks with other players.

## **Admin Panel**

To manage ducks and view users:

1. Visit http://0.0.0.1:8000/admin/.
2. Log in with the superuser credentials created earlier.
3. Use the admin interface to manage ducks and user data.
