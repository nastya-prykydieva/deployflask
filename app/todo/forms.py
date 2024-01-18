from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ToDoForm(FlaskForm):
    todo = StringField("Enter a task here", validators=[DataRequired(), Length(min=1, max=50)])
    description = StringField("Enter a description here", validators=[DataRequired(), Length(min=1, max=255)])
    submit = SubmitField("Save")
