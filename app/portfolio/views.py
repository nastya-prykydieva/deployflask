from . import portfolio
from flask import render_template, request
from datetime import datetime
import os

skills = ["Python", "SQL", "Flask", "English", "Teamwork"]


@portfolio.context_processor
def inject_system_info():
    return dict(data=os.name, user_agent=request.headers.get('User-Agent'), time=datetime.now())


@portfolio.route('/')
@portfolio.route('/about')
def about():
    return render_template('about.html')


@portfolio.route('/ipz')
def ipz():
    return render_template('ipz.html')


@portfolio.route('/skills')
@portfolio.route('/skills/<int:num>')
def skills_page(num=None):
    if num is not None and num < len(skills):
        return render_template('skill.html', num=num+1, skill=skills[num])
    else:
        return render_template('skills.html', skills=skills)


@portfolio.route('/contact')
def contact():
    return render_template('contact.html')
