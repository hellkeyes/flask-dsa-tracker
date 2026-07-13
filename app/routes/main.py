from flask import Blueprint, render_template, url_for, redirect, flash
from app.utils import fetch_problem
from app.forms import AddProblem, SelectPatternsForm, LogAttemptForm
from flask_login import login_required, current_user
from app.models import Problem, UserProblem, db, Pattern, Attempt
from datetime import timedelta, datetime

main = Blueprint('main',__name__)

@main.route('/dashboard')
@login_required
def dashboard():
    user_problems = UserProblem.query.filter_by(user_id=current_user.id).all()
    
    # to calculate the pattern weakness and its score (kpi)
    pattern_scores = {}

    for up in user_problems:
        print(up.problem.title)
        for pattern in up.patterns:
            if pattern.pattern_name not in pattern_scores:
                pattern_scores[pattern.pattern_name] = []
            for attempt in up.attempts:
                pattern_scores[pattern.pattern_name].append((attempt))

    pattern_attempts = {}

    for pattern_name, attempts in pattern_scores.items():
        total_attempts = len(attempts)
        if total_attempts == 0:
            continue
        else:
            all_time_average = sum(attempt.confidence for attempt in attempts)/total_attempts

            last_three_attempts = attempts[-3:]
            recent_average = (sum(attempt.confidence for attempt in last_three_attempts)/ len(last_three_attempts))

            if recent_average > all_time_average:
                trend = "Improving"
            elif recent_average < all_time_average:
                trend = "Declining"
            else:
                trend = "Stable"

            last_practiced = max(attempt.created_at for attempt in attempts)

            pattern_attempts[pattern_name] = {
            'total_attempts': total_attempts,
            'average_confidence': round(all_time_average, 1),
            'trend': trend,
            'last_practiced': last_practiced
            }

    review_today = []
    #this is for the spaced repetition 
    for up in user_problems:
        if not up.attempts:
            continue
        else:
            problem_title = up.problem.title
            last_attempt = max(up.attempts, key=lambda attempt: attempt.created_at)
            confidence = last_attempt.confidence
            last_practiced = last_attempt.created_at

            if confidence == 1:
                review_days = 0
            elif confidence == 2:
                review_days = 3
            elif confidence == 3:
                review_days =  7
            elif confidence == 4:
                review_days = 14
            else:
                review_days = 30
            next_review = last_practiced + timedelta(days=review_days)

            today = datetime.today()
            if next_review <= today:
                review_today.append({
                    "title": up.problem.title,
                    "last_practiced": last_practiced,
                    "next_review": next_review
                })


    return render_template('main/dashboard.html',user_problems=user_problems, pattern_attempts=pattern_attempts, review_today=review_today)


@main.route('/add_problem', methods=['GET','POST'])
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
    return render_template('main/log_attempt.html', form=form,user_problem=user_problem)


@main.route('/test')
def test():






    return "Done"