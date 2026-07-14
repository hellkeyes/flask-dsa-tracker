# Flask DSA Tracker

> **Version:** v1.0  
> **Status:** Completed (Learning Project)

Flask DSA Tracker is a web application built to help students practice Data Structures & Algorithms more effectively.

Instead of simply counting solved LeetCode problems, the application tracks solving confidence, identifies weak DSA patterns, stores every practice attempt, and recommends when to revisit problems using a confidence-based spaced repetition system.

This project was built as my **first full-stack Flask application** while learning backend development, relational database design, SQLAlchemy, authentication, and software engineering principles.

---

# Table of Contents

- Features
- Tech Stack
- Project Architecture
- Database Design
- Project Structure
- Getting Started
- Future Roadmap
- Learning Outcomes

---

# Features

## User Authentication

- User registration
- Login using username or email
- Password hashing with Flask-Bcrypt
- Session management using Flask-Login

---

## Problem Management

Users can add LeetCode problems by entering the problem title.

The application automatically:

- Converts the title into a slug
- Fetches problem information from the Alfa LeetCode API
- Stores the problem globally
- Creates a user-specific tracking entry
- Prevents duplicate entries

---

## Pattern Tracking

Each problem can be linked with multiple DSA patterns.

Examples:

- Arrays
- Dynamic Programming
- Sliding Window
- Graphs
- Binary Search
- Trees

Pattern assignments can be updated at any time.

---

## Attempt Logging

Every solve session is recorded independently.

Each attempt stores:

- Confidence (1–5)
- Time Taken
- Solved / Not Solved
- Personal Notes
- Practice Date

This allows progress to be tracked over time rather than only storing the latest result.

---

## Weakness Analysis

The dashboard calculates weak patterns using:

- Average confidence
- Number of attempts
- Trend (Improving / Stable / Declining)
- Last practiced date

Patterns are ranked automatically to help prioritize revision.

---

## Spaced Repetition

Problems become due for review depending on confidence.

| Confidence Rating (1–5) | Review After |
|-------------------------:|-------------:|
| 1 (Very Low)  | 1 day |
| 2 (Low)       | 3 days |
| 3 (Moderate)  | 7 days |
| 4 (High)      | 14 days |
| 5 (Very High) | 30 days |

The goal is to spend more time reviewing weaker topics while reducing unnecessary repetition.

---

## Dashboard

The dashboard displays:

- Recently practiced problems
- Weakest DSA patterns
- Problems due for review
- Difficulty badges
- Pattern tags
- Quick access to problem history

---

# Tech Stack

## Backend

- Python
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-Login
- Flask-Bcrypt

## Database

- SQLite

## Frontend

- HTML
- CSS
- Jinja2

## External APIs

- Alfa LeetCode API

---

# Project Architecture

```
User
 │
 ├── Authentication
 │
 └── UserProblem
       │
       ├── Problem
       │
       ├── Pattern (Many-to-Many)
       │
       └── Attempts
```

The project follows Flask's application factory pattern and separates authentication and application routes using Blueprints.

---

# Database Design

Core models:

- User
- Problem
- UserProblem
- Pattern
- Attempt

Relationships:

- User → UserProblem (One-to-Many)
- UserProblem → Pattern (Many-to-Many)
- UserProblem → Attempt (One-to-Many)

This design allows multiple users to track the same LeetCode problem independently while maintaining separate practice histories.

---

# Project Structure

```
flask-dsa-tracker/
│
├── app/
│   ├── auth.py
│   ├── main.py
│   ├── models.py
│   ├── forms.py
│   ├── utils.py
│   ├── templates/
│   ├── static/
│   └── __init__.py
│
├── migrations/
├── seed.py
├── run.py
├── requirements.txt
└── README.md
```

---

# Getting Started

## Clone the repository

```bash
git clone https://github.com/yourusername/flask-dsa-tracker.git
cd flask-dsa-tracker
```

## Create a virtual environment

```bash
python -m venv venv
```

## Activate it

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run migrations

```bash
flask db upgrade
```

## Seed default DSA patterns

```bash
python seed.py
```

## Run the application

```bash
python run.py
```

---

# Future Roadmap (v2)

- LeetCode username synchronization
- User-created custom patterns
- Statistics page
- Daily streak tracking
- Charts & analytics
- Individual attempt deletion
- React frontend
- Search & filtering

---

# About This Project

This is **Version 1** of the Flask DSA Tracker.

The goal of this project was not only to build a useful tool for DSA practice but also to strengthen my understanding of backend development by designing and implementing a complete web application from scratch.

As I continue learning, future versions will introduce more advanced features, improved architecture, and a modern frontend.