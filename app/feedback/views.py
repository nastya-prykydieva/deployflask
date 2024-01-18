from . import feedback_bp
from flask import render_template, redirect, url_for, flash
from app import db
from .models import Feedback
from .forms import FeedbackForm
from datetime import datetime


@feedback_bp.route("/feedback", methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    feedbacks = db.session.query(Feedback).all()
    if form.validate_on_submit():
        username = form.username.data
        text = form.text.data
        date = datetime.now()
        if username and text:
            db.session.add(Feedback(username=username, text=text, date=date))
            db.session.commit()
            flash("Feedback was added.", category="success")
        else:
            flash("Feedback was not added.", category="danger")
        return redirect(url_for("feedback_bp.feedback"))
    return render_template('feedback.html', feedbacks=feedbacks, form=form)


@feedback_bp.route("/feedbacks/delete/<int:id>")
def delete_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    try:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback was successfully deleted!", category="success")
    except:
        db.session.rollback()
        flash("Error!", category="danger")
    return redirect(url_for("feedback_bp.feedback"))
