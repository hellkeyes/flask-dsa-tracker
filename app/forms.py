from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp

class RegistrationForm(FlaskForm):
    username = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[Email(), DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), Regexp(r"^[A-Za-z0-9_-]+$", message="Username can only contain letters, numbers, and underscores.")])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')


class LoginForm(FlaskForm):
    login = StringField('', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('submit')
