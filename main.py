from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import os
from flask_wtf.csrf import CSRFProtect
import jwt
import datetime
# from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Secret key (Use environment variable for security)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'aladinh00-010montext')

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
csrf = CSRFProtect(app)
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='Pending')

# Initialize database
with app.app_context():
    db.create_all()

# API endpoint for user registration
@app.route("/api/register", methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# API endpoint for user login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, 
                       app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({"token": token}), 200

# Fetch all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{ "id": task.id, "name": task.name, "status": task.status } for task in tasks])

# Add a new task
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task_name = data.get("task_name")
    if not task_name:
        return jsonify({"error": "Task name is required"}), 400

    new_task = Task(name=task_name)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully"}), 201

# Update a task status
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify({"message": "Task updated successfully"})

# Delete a task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
