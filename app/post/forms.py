from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed
from app import db
from app.post.models import Type, Category, Tag


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    text = TextAreaField('Text', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(["jpg", "png"])])
    type = SelectField('Type', choices=[e.name for e in Type])
    enabled = BooleanField('Enabled')
    category = SelectField('Category', coerce=int)
    tags = SelectMultipleField('Tags', coerce=int)
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Submit')


class TagForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField(label="Save tag")


class SelectCategoryForm(FlaskForm):
    category = SelectField('Select Category', default='all',
                           choices=[('all', 'All')] + [(c.id, c.name) for c in db.session.query(Category)])
    submit = SubmitField('Submit')
