# Events Organizer App

This is an Events Organizer application built with Flask-web framework. It allows users to register, log in, and manage their to-do events and tasks.

## Features

- User registration and login
- Add, update, and delete tasks and events
- Flash messages for user feedback
- Responsive design

## Project Structure

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/harizonelopez/Events-Organizer.git
    cd Event-Organizer
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/Scripts/activate  # On Mac use `venv\bin\activate`
    ```

3. Initialize the database:
    ```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

## Usage

1. Run the Flask application:
    ```sh
    flask run
    ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

## API Endpoints

- `POST /api/register`: Register a new user
- `POST /api/login`: Log in a user
- `GET /api/tasks`: Fetch all tasks
- `POST /api/tasks`: Add a new task
- `PUT /api/tasks/<int:task_id>`: Update a task status
- `DELETE /api/tasks/<int:task_id>`: Delete a task

## License

This project is licensed under the MIT License.
