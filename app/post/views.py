from sqlalchemy import desc
from . import post_bp
from app import db
from flask import render_template, request, redirect, url_for, flash, current_app
from app.post.models import Post, Category, Tag
from .forms import PostForm, CategoryForm, TagForm, SelectCategoryForm
from flask_login import login_required, current_user
from PIL import Image
import os
import secrets


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@post_bp.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    post_list = Post.query.all()
    tags = Tag.query.all()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    form.tags.choices = [(t.id, t.name) for t in tags]
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, text=form.text.data, type=form.type.data,
                        enabled=form.enabled.data, user_id=current_user.id, category_id=form.category.data,
                        tags=[tag for tag in tags if tag.id in form.tags.data])
        if form.image.data:
            image = save_picture(form.image.data)
            new_post.image = image
        db.session.add(new_post)
        db.session.commit()
        flash("The new post was added successfully.", "success")
        return redirect(url_for("post_bp.list_post"))
    elif request.method != "GET":
        flash("The new task was not added!", "danger")
    return render_template('create_post.html', form=form, post_list=post_list)


@post_bp.route("/", methods=['GET', 'POST'])
@login_required
def list_post():
    form = SelectCategoryForm()
    post_list = db.session.query(Post).all()
    page = request.args.get("page", 1, type=int)
    if request.method == "GET":
        category = request.args.get("category", "all")
    else:
        category = form.category.data
    posts = Post.query
    if (form.validate_on_submit() or request.method == "GET") and category != "all":
        form.category.data = category
        posts = posts.filter(Post.category.has(id=form.category.data))
    posts = posts.order_by(desc(Post.created)).paginate(page=page, per_page=2)
    return render_template('list_post.html', post_list=post_list, posts=posts, form=form)


@post_bp.route("/<int:id>", methods=["GET"])
@login_required
def view(id):
    post = Post.query.get_or_404(id)
    return render_template('view_post.html', post=post)


@post_bp.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update(id):
    form = PostForm()
    post = Post.query.get_or_404(id)
    tags = Tag.query.all()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    form.tags.choices = [(t.id, t.name) for t in tags]
    if form.validate_on_submit():
        if form.image.data:
            image = save_picture(form.image.data)
            post.image = image
        post.title = form.title.data
        post.text = form.text.data
        post.enabled = form.enabled.data
        post.type = form.type.data
        post.category_id = form.category.data
        post.tags = [tag for tag in tags if tag.id in form.tags.data]
        db.session.commit()
        flash(f"Post №{id} was updated.", "success")
        return redirect(url_for("post_bp.view", id=id))
    elif request.method == "GET":
        form.title.data = post.title
        form.text.data = post.text
        form.enabled.data = post.enabled
        form.type.data = post.type.name
        form.category.data = post.category_id
        form.tags.data = [tag.id for tag in post.tags]
    return render_template('update_post.html', form=form, post=post)


@post_bp.route("/<int:id>/delete", methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post №{id} was deleted.", "success")
    return redirect(url_for("post_bp.list_post"))


@post_bp.route("/category/create", methods=['GET', 'POST'])
@login_required
def create_category():
    form = CategoryForm()
    category_list = Category.query.all()
    if form.validate_on_submit():
        new_category = Category(name=form.name.data)
        db.session.add(new_category)
        db.session.commit()
        flash("The new category was added successfully.", "success")
        return redirect(url_for("post_bp.list_category"))
    elif request.method != "GET":
        flash("The new category was not added!", "danger")
    return render_template('category.html', form=form, category_list=category_list)


@post_bp.route("/category", methods=['GET'])
@login_required
def list_category():
    form = CategoryForm()
    category_list = db.session.query(Category).all()
    return render_template('category.html', form=form, category_list=category_list)


@post_bp.route("/category/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_category(id):
    form = CategoryForm()
    category = Category.query.get_or_404(id)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash(f"Category №{id} was edited.", "success")
        return redirect(url_for("post_bp.list_category", id=id))
    elif request.method == "GET":
        form.name.data = category.name
    return render_template('update_category.html', form=form, category=category)


@post_bp.route("/category/<int:id>/delete", methods=['GET', 'POST'])
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash(f"Category №{id} was deleted.", "success")
    return redirect(url_for("post_bp.list_category"))


@post_bp.route("/tag/create", methods=['GET', 'POST'])
@login_required
def create_tag():
    form = TagForm()
    tag_list = Tag.query.all()
    if form.validate_on_submit():
        new_tag = Tag(name=form.name.data)
        db.session.add(new_tag)
        db.session.commit()
        flash("The new tag was added successfully.", "success")
        return redirect(url_for("post_bp.list_tag"))
    elif request.method != "GET":
        flash("The new tag was not added!", "danger")
    return render_template('tag.html', form=form, tag_list=tag_list)


@post_bp.route("/tag", methods=['GET'])
@login_required
def list_tag():
    form = TagForm()
    tag_list = db.session.query(Tag).all()
    return render_template('tag.html', form=form, tag_list=tag_list)


@post_bp.route("/tag/<int:id>/delete", methods=['GET', 'POST'])
@login_required
def delete_tag(id):
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag №{id} was deleted.", "success")
    return redirect(url_for("post_bp.list_tag"))
