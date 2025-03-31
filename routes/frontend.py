from flask import Blueprint, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.task import Task


frontend_bp = Blueprint('frontend_bp',__name__)


@frontend_bp.route('/')
def home():
    return render_template('home.html')

@frontend_bp.route('login')
def login():
    return render_template('login.html')

@frontend_bp.route('/signup')
def signup():
    return render_template('signup.html')


@frontend_bp.route('/tasks/view')
@jwt_required()
def view_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return render_template('tasks.html', tasks=tasks)