from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class FeedbackForm(FlaskForm):
    username = StringField("Enter your username", validators=[DataRequired(), Length(min=4, max=14)])
    text = StringField("Leave your feedback here", validators=[DataRequired()])
    submit = SubmitField("Submit")
