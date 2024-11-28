from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_cors import CORS
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aladinh00-01montext'
CORS(app)

# File to store tasks
TASKS_FILE = 'data.json'
users = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/home')
def home_page():
    if 'userID' not in session:
        return redirect(url_for('home'))  # Redirect to login page if not logged in
    return render_template("home_page.html")

@app.route('/api/login', methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return render_template("index.html", error="Username and password are required")

    # Check if user exists and password matches
    if username in users and users[username] == password:
        session['userID'] = username  # Store user ID in session for authentication
        return redirect(url_for('home_page'))  # Redirect to the home page after successful login
    else:
        return render_template("index.html", error="Invalid username or password")


# API endpoint for user registration
@app.route("/api/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return render_template("index.html", error="Username and password are required")

    if username in users:
        return render_template("index.html", error="User already exists")

    # Register the user
    users[username] = password
    return render_template("index.html", success="User created successfully! Please log in.")


# Serve static files (e.g., JavaScript, CSS)
app.static_folder = "static"


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
