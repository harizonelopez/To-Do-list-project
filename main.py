from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aladinh00-01montext'
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
# users = {}

@app.route("/")
def home():
    return render_template("index.html")

# API endpoint for user registration
@app.route("/api/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Username and password are required", "error")
        return redirect(url_for('home'))

    # check if the user already exists in the database
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash("User already exists", "error")
        return redirect(url_for('home'))

    # Register the user
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash("User created successfully", "success")
    return redirect(url_for('home'))

# API endpoint for user login
@app.route('/api/login', methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    print(f"Username: {username}, Password: {password}")

    # Authenticate the user
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password): 
        # flash(f"Welcome back, {username}!", "success")
        return redirect(url_for('home_page'))  
    else:
        flash("Invalid username or password!", "error")
        return redirect(url_for('home')) 

    # flash("Invalid username or password !!", "error")


@app.route('/home_page')
def home_page():
    # if 'userID' not in session:
        # return redirect(url_for('home'))  
    return render_template("home_page.html")

# Helper to read tasks
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
    new_task['id'] = len(tasks) + 1  # Simple auto-increment logic
    tasks.append(new_task)
    write_tasks(tasks)
    return jsonify({"message": "Task added successfully"}), 201

# Route: Update a task status
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    tasks = read_tasks()
    for task in tasks:
        
        if task['id'] == task_id:
            task['status'] = request.json.get('status', task['status'])
            write_tasks(tasks)
            return jsonify({"message": "Task updated successfully"})
    return jsonify({"error": "Task not found"}), 404

# Route: Delete a task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = read_tasks()
    updated_tasks = [task for task in tasks if task['id'] != task_id]
    if len(tasks) == len(updated_tasks):
        return jsonify({"error": "Task not found"}), 404
    write_tasks(updated_tasks)
    return jsonify({"message": "Task deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
