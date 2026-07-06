# Flask DSA Tracker

> **Work in Progress:** This project is currently under active development. New features and improvements are being added as I continue learning Flask and backend development.

A web application built with Flask to help students practice Data Structures & Algorithms more effectively.

Rather than simply tracking solved problems, the goal is to identify weak DSA patterns, measure solving confidence, and recommend when to revisit topics using spaced repetition.

## Current Progress

* Designed the database schema using SQLAlchemy
* Implemented `User`, `Pattern`, `Problem`, and `Attempt` models
* Created many-to-many relationships between problems and patterns
* Configured the Flask application factory
* Set up Blueprints
* Configured Flask-Migrate and database migrations
* Added support for both global and user-created DSA patterns
* Seeding default DSA patterns

### In Progress

* User authentication
* Problem management
* Attempt logging

### Planned

* Analytics dashboard
* Weakness scoring system
* Spaced repetition engine
* Progress visualization

## Planned Features

* User authentication
* Track solved DSA problems
* Categorize problems by DSA pattern
* Record solving time and confidence
* Progress dashboard
* Weakness analysis
* Spaced repetition scheduling
* Support for custom DSA patterns

## Tech Stack

* Python
* Flask
* SQLAlchemy
* Flask-Migrate
* SQLite
* HTML
* CSS
* Jinja2

## Purpose

This project is being developed as both a learning experience and a portfolio project. It is built incrementally to deepen my understanding of Flask, SQLAlchemy, authentication, database design, backend architecture, and software engineering best practices.
