from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old password", validators=[DataRequired(), Length(min=4, max=10)])
    new_password = PasswordField("New password", validators=[DataRequired(), Length(min=4, max=10)])
    confirm_password = PasswordField("Confirm new password", validators=[DataRequired(),
                                                                         Length(min=4, max=10),
                                                                         EqualTo('new_password')])
    submit = SubmitField("Submit")
