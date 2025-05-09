# SwapSpot

SwapSpot is a Django web application that allows users to list items they no longer need and propose swaps with other users. It features user authentication, item categorization, and an exchange request system to manage swapping activity.

---

## 🌟 Features

- ✅ User registration and authentication (login/logout)
- 📦 Item upload with categories and images
- 🔄 Swap proposal functionality
- 📥 Inbox for managing incoming swap requests
- 💬 Messaging system between users
- ⭐ Leave reviews after completed exchanges

---

## 🛠️ Tech Stack

- **Backend**: Django, Python
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Hosting**: [Render](https://render.com)

---

## 🧪 Local Setup Instructions

1. **Clone the repository**  
   `git clone https://github.com/tati1904/swapspot.git`

2. **Navigate to the project folder**  
   `cd swapspot`

3. **Create and activate a virtual environment**  
   Windows:  
   `python -m venv venv`  
   `venv\Scripts\activate`  

   macOS/Linux:  
   `python3 -m venv venv`  
   `source venv/bin/activate`

4. **Install dependencies**  
   `pip install -r requirements.txt`

5. **Create `.env` file and add your database settings**  
   Example:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=your-local-postgres-url
Run migrations
python manage.py migrate

Collect static files
python manage.py collectstatic

Start the server
python manage.py runserver
🚀 Deployment on Render
Live site:
https://swapspot.onrender.com

GitHub repository:
https://github.com/tati1904/swapspot

Deployment Steps:
Go to Render Dashboard and create a new Web Service.

Connect your GitHub repo, and choose the swapspot repository.

Set the following Environment Variables:

DATABASE_URL: (provided by Render PostgreSQL database)

RENDER: true

SECRET_KEY: (your Django secret key)

Set Build Command:
pip install -r requirements.txt

Set Start Command:
gunicorn swapspot.wsgi:application

Create a file named render.yaml to automate setup:
services:
  - type: web
    name: swapspot
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn swapspot.wsgi:application"
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: swapspot_db
          property: connectionString
      - key: RENDER
        value: true
Add a release command in the Render Dashboard:
python manage.py collectstatic --noinput && python manage.py migrate
