from . import todo_bp
from flask import render_template, redirect, url_for, flash
from app import db
from .models import Todo
from .forms import ToDoForm


@todo_bp.route('/todo', methods=['GET', 'POST'])
def todo():
    form = ToDoForm()
    todo_list = db.session.query(Todo).all()
    if form.validate_on_submit():
        return redirect(url_for("todo_bp.todo"))
    return render_template("todo.html", form=form, todo_list=todo_list)


@todo_bp.route("/add", methods=['GET', 'POST'])
def add():
    form = ToDoForm()
    todo_list = Todo.query.all()
    if form.validate_on_submit():
        new_task = Todo(title=form.todo.data, description=form.description.data, complete=False)
        db.session.add(new_task)
        db.session.commit()
        flash("The new task was added successfully.", "success")
        return redirect(url_for("todo_bp.todo"))
    flash("The new task was not added!", "danger")
    return render_template('todo.html', form=form, todo_list=todo_list)


@todo_bp.route("/update/<int:id>")
def update(id):
    todo = Todo.query.get_or_404(id)
    todo.complete = not todo.complete
    db.session.commit()
    flash(f"The task №{id} was updated.", "success")
    return redirect(url_for("todo_bp.todo"))


@todo_bp.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash(f"Task №{id} was deleted.", "success")
    return redirect(url_for("todo_bp.todo"))
