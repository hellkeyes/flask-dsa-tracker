from flask import Blueprint, render_template, url_for, redirect, flash
from app.utils import fetch_problem
from app.forms import AddProblem, SelectPatternsForm, LogAttemptForm
from flask_login import login_required, current_user
from app.models import Problem, UserProblem, db, Pattern, Attempt

up = UserProblem.query.first()

print(up)
print(up.patterns)
print(up.attempts)
