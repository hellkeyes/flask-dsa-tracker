from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, widgets, SelectField, IntegerField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp

class RegistrationForm(FlaskForm):
    username = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[Email(), DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), Regexp(r"^[A-Za-z0-9_-]+$", message="Username can only contain letters, numbers, and underscores.")])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    login = StringField('', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddProblem(FlaskForm):
    title = StringField('Title name', validators=[DataRequired()])
    submit = SubmitField('Add Problem')

class SelectPatternsForm(FlaskForm):
    patterns = SelectMultipleField(
        'Patterns',
        coerce=int,
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )
    submit = SubmitField('Save Pattern')

class LogAttemptForm(FlaskForm):
    confidence = SelectField(
        'Confidence (1-5)', 
        choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],
        coerce=int)
    time_taken_mins = IntegerField('Time Taken (Mins)', validators=[DataRequired()])
    solved = BooleanField('Solved?')
    notes = TextAreaField('Notes')
    submit = SubmitField('Log Attempt')


