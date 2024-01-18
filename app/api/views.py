from . import api_bp
from app.todo.models import Todo
from app.auth.models import User
from .models import TokenBlocklist
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from app import db, jwt_manager
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        return username


@basic_auth.error_handler
def auth_error():
    return jsonify({"message": "Invalid username or password"}), 401


@api_bp.route('/login', methods=['POST'])
@basic_auth.login_required
def login():
    access_token = create_access_token(identity=basic_auth.current_user())
    refresh_token = create_refresh_token(identity=basic_auth.current_user())
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@api_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@jwt_manager.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_data):
    jti = jwt_data['jti']
    token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()
    return token is not None


@api_bp.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    jwt = get_jwt()
    jti = jwt['jti']
    token_type = jwt['type']
    token_b = TokenBlocklist(jti=jti)
    token_b.save()
    return jsonify({"message": f"{token_type} token revoked with success"}), 200


@api_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({
        "message": "pong"
    })


@api_bp.route("/todos", methods=["GET"])
@jwt_required()
def get_todos():
    todos = Todo.query.all()
    todo_dict = []
    for todo in todos:
        item = dict(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            complete=todo.complete
        )
        todo_dict.append(item)
    return jsonify(todo_dict)


@api_bp.route("/todos", methods=["POST"])
@jwt_required()
def post_todos():
    new_data = request.get_json()

    if not new_data:
        return jsonify({"message": "no input data provided"}), 400

    if not new_data.get("title") or not new_data.get("description"):
        return jsonify({"message": "no keys"}), 422

    todo = Todo(title=new_data.get("title"), description=new_data.get("description"))
    db.session.add(todo)
    db.session.commit()

    new_todo = Todo.query.filter_by(id=todo.id).first()

    return jsonify({
        "message": "todo was added",
        "id": new_todo.id,
        "title": new_todo.title,
        "description": new_todo.description,
    }), 201


@api_bp.route("/todos/<int:id>", methods=["GET"])
@jwt_required()
def get_todo(id):
    todo = Todo.query.filter_by(id=id).first()

    if not todo:
        return jsonify({"message": f"todo with id {id} not found"}), 404

    return jsonify({
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
    }), 200


@api_bp.route("/todos/<int:id>", methods=["PUT"])
@jwt_required()
def update_todo(id):
    todo = Todo.query.filter_by(id=id).first()

    if not todo:
        return jsonify({"message": f"todo with id {id} not found"}), 404

    new_data = request.get_json()

    if not new_data:
        return jsonify({"message": "no input data provided"}), 400

    if new_data.get("title"):
        todo.title = new_data.get("title")

    if new_data.get("description"):
        todo.description = new_data.get("description")

    if not new_data.get("title") or not new_data.get("description"):
        return jsonify({"message": "no keys"}), 422

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "unexpected data"}), 422

    return jsonify({
        "message": "todo was updated"
    }), 200


@api_bp.route("/todos/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_todo(id):
    todo = Todo.query.filter_by(id=id).first()

    if not todo:
        return jsonify({"message": f"todo with id {id} not found"}), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({
        "message": "todo was deleted"
    }), 200
