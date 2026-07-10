from flask import Blueprint, render_template, url_for, redirect, flash
from app.utils import fetch_problem
from app.forms import AddProblem
from flask_login import login_required, current_user
from app.models import Problem, UserProblem, db


main = Blueprint('main',__name__)

@main.route('/dashboard')
def dashboard():
    return render_template('main/dashboard.html')

@main.route('/add-problem', methods=['GET','POST'])
@login_required
def add_problem():
    form = AddProblem()
    if form.validate_on_submit():
        title_slug = form.title.data.lower().strip().replace(' ', '-')
        problem_details = fetch_problem(title_slug)
        if problem_details is None:
            flash("Problem not found.", "danger")
            return render_template('main/add_problem.html', form=form)

        exist_in_problem = Problem.query.filter_by(problem_number=problem_details["problem_number"]).first()
        if not exist_in_problem:
            problem = Problem(**problem_details)
            db.session.add(problem)
            db.session.flush()
        else:
            problem = exist_in_problem

        already_added = UserProblem.query.filter_by(user_id=current_user.id, problem_id=problem.problem_id).first()
        if already_added:
            flash('Problem already added.','warning')
            return redirect(url_for('main.add_problem'))

        user_problem = UserProblem(
            user_id=current_user.id, 
            problem_id=problem.problem_id
            )
        db.session.add(user_problem)
        db.session.commit()
        return redirect(url_for('main/select_patterns', user_problem_id=user_problem.id))

    else:
        return render_template('main/add_problem.html', form=form)

@main.route('/select-patterns/<int:user_problem_id>', methods=['GET', 'POST'])
@login_required
def select_patterns(user_problem_id):
    return "this is select patterns"