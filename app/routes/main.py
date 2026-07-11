from flask import Blueprint, render_template, url_for, redirect, flash
from app.utils import fetch_problem
from app.forms import AddProblem, SelectPatternsForm, LogAttemptForm
from flask_login import login_required, current_user
from app.models import Problem, UserProblem, db, Pattern, Attempt


main = Blueprint('main',__name__)

@main.route('/dashboard')
@login_required
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
        return redirect(url_for('main.select_patterns', user_problem_id=user_problem.id))

    else:
        return render_template('main/add_problem.html', form=form)

@main.route('/select-patterns/<int:user_problem_id>', methods=['GET', 'POST'])
@login_required
def select_patterns(user_problem_id):
    user_problem = UserProblem.query.get_or_404(user_problem_id)
    if user_problem.user_id != current_user.id:
        flash("You don't have access to this.", "danger")
        return redirect(url_for('main.dashboard'))
    patterns = Pattern.query.filter((Pattern.user_id == None) | (Pattern.user_id == current_user.id)).all()
    form = SelectPatternsForm()
    form.patterns.choices = [(p.id, p.pattern_name) for p in patterns]
    if form.validate_on_submit():
        selected = Pattern.query.filter(Pattern.id.in_(form.patterns.data)).all()
        user_problem.patterns = selected
        db.session.commit()
        return redirect(url_for('main.log_attempt', user_problem_id=user_problem.id))
    return render_template('main/select_patterns.html', form=form, user_problem=user_problem)
        
@main.route('/log_attempt/<int:user_problem_id>', methods=['POST','GET'])
@login_required
def log_attempt(user_problem_id):
    user_problem = UserProblem.query.get_or_404(user_problem_id)
    if user_problem.user_id != current_user.id:
        flash("You don't have access to this.", "danger")
        return redirect(url_for('main.dashboard'))
    form = LogAttemptForm()
    if form.validate_on_submit():
        attempt = Attempt(
            user_problem_id = user_problem_id,
            confidence = form.confidence.data,
            time_taken_mins = form.time_taken_mins.data,
            solved = form.solved.data,
            notes = form.notes.data
        )
        db.session.add(attempt)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('main/log-attempt.html', form=form,user_problem=user_problem)