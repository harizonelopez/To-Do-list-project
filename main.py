from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aladinh00-010montext'
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Class model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()


# File to store tasks
TASKS_FILE = 'data.json'
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

# API endpoint for user registration
@app.route("/api/register", methods=['POST'])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Username and password are required", "error")
        return redirect(url_for('home'))

    # check if the user account already exists in the database
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash("The Username already exists", "error")
        return redirect(url_for('home'))

    # Register the user to the database
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash("User account created successfully", "success")
    return redirect(url_for('home'))

# API endpoint for user login
@app.route('/api/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # print(f"Username: {username}, Password: {password}")--> Used for debugging purpose.

    # Authenticate the user credentials
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password): 
        return redirect(url_for('home_page'))  
    else:
        flash("Invalid username or password!", "error")
        return redirect(url_for('home')) 

@app.route('/home_page')
def home_page():  
    return render_template("home_page.html")

# Helper to read tasks and events
def read_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Helper to write tasks
def write_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)

# Route: Fetch all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = read_tasks()
    return jsonify(tasks)

# Route: Add a new task 
@app.route('/api/tasks', methods=['POST'])
def add_task():
    new_task = request.json
    tasks = read_tasks()
    new_task['id'] = len(tasks) + 1 
    tasks.append(new_task)
    write_tasks(tasks)
    flash("Task added successfully", "success")

# Route: Update a task status
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = request.json.get('status', task['status'])
            write_tasks(tasks)
            flash("Task updated successfully", "info")
    flash("Task not found", "error")

# Route: Delete a task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = read_tasks()
    updated_tasks = [task for task in tasks if task['id'] != task_id]
    if len(tasks) == len(updated_tasks):
        flash("Task not found", "error")
    write_tasks(updated_tasks)
    flash("Task deleted successfully", "warning")

if __name__ == "__main__":
    app.run(debug=True)
