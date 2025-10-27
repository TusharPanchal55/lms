
# 📘 Learning Management System (LMS)

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.0-darkgreen?logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Project%20Phase-Completed-brightgreen)

🧩 Overview

A full-featured Learning Management System built with Django and PostgreSQL, enabling teachers to create courses and quizzes while students can enroll, learn through video lessons, track progress, and take assessments.

This project demonstrates complete backend and frontend integration, authentication, and data management — designed for scalability, clean architecture, and clarity of learning flow.

🚀 Features
👨‍🏫 For Teachers

Create, edit, and delete courses

Upload lessons with videos and resources

Create and manage quizzes with questions and answers

View student progress

👩‍🎓 For Students

Register, log in, and browse available courses

Enroll in courses and access lessons

Track learning progress with visual progress bars

Attempt quizzes and get instant graded results

⚙️ Core System Features

Role-based authentication (Admin, Teacher, Student)

Dark-themed modern responsive UI

Secure session management

Progress tracking per lesson

PostgreSQL database integration

Media upload support for thumbnails and videos

🛠️ Tech Stack
Layer	Technology
Backend	Django, Python
Database	PostgreSQL
Frontend	HTML, CSS, Bootstrap
Auth & Security	Django Auth System
Storage	Local media (configurable to S3)
📂 Project Structure
LMS/
│
├── users/                # User auth, registration, roles, dashboards
├── courses/              # Course & Lesson management
├── quizzes/              # Quiz and assessment module
├── templates/            # HTML templates
├── static/               # CSS, JS, and static assets
├── media/                # Uploaded thumbnails & videos
├── manage.py
└── requirements.txt

⚡ Setup Instructions

Clone the repository

git clone https://github.com/your-username/LMS.git
cd LMS


Create a virtual environment & activate

python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate      # For Windows


Install dependencies

pip install -r requirements.txt


Setup PostgreSQL and run migrations

python manage.py makemigrations
python manage.py migrate


Create a superuser

python manage.py createsuperuser


Run the server

python manage.py runserver


Access the app

App: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

🎯 Future Enhancements

Certificates after course completion

Discussion forums for learners

Recommendation system for personalized learning

Advanced analytics dashboard

🧠 Key Learnings

Implemented role-based access control (RBAC)

Built dynamic progress tracking with relational data

Designed reusable Django models and views

Understood real-world LMS architecture and flow

📜 License

This project is open-source and available under the MIT License.
