# CyberGenie

![Build Status](https://img.shields.io/github/actions/workflow/status/canstralian/CyberGenie/your-workflow.yml?branch=main)
![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0.1-blue)
![License](https://img.shields.io/github/license/canstralian/CyberGenie)
![Last Commit](https://img.shields.io/github/last-commit/canstralian/CyberGenie)
![Open Issues](https://img.shields.io/github/issues/canstralian/CyberGenie)

**CyberGenie** is a Flask-based web application that leverages SQLAlchemy for ORM and Flask-Login for user authentication.

## Features

- User authentication
- Dashboard with user-specific data
- Scanning functionality
- Centralized logging

## Project Structure

```
CyberGenie/
├── app.py                # Main application setup
├── config.py             # Configuration settings
├── models.py             # Database models
├── routes/
│   ├── auth.py           # Authentication routes
│   ├── dashboard.py      # Dashboard routes
│   └── scans.py          # Scanning routes
├── templates/            # HTML templates
├── static/               # Static files (CSS, JavaScript)
└── instance/             # Instance folder for app-specific data
```

## Getting Started

### Prerequisites

- Python 3.7+
- Flask
- Flask-SQLAlchemy
- Flask-Login

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/canstralian/CyberGenie.git
   cd CyberGenie
   ```

2. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up the configuration:
   Create a `config.py` file with the necessary configuration settings.

### Running the Application

1. Initialize the database:
   ```sh
   flask db init
   flask db migrate
   flask db upgrade
   ```

2. Run the application:
   ```sh
   flask run
   ```

### Logging

The application uses Python's built-in logging module to log messages to the console. The logging configuration is set up in `app.py`.

### Error Handling

Custom error handlers are defined for 404 and 500 errors to provide user-friendly error messages and log the errors.

### Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

### License

This project is licensed under the MIT License.

## Detailed Setup Instructions

### Setting Up the Development Environment

1. **Clone the repository:**
   ```sh
   git clone https://github.com/canstralian/CyberGenie.git
   cd CyberGenie
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the configuration:**
   Create a `config.py` file with the necessary configuration settings.

### Running Tests

1. **Run unit tests:**
   ```sh
   pytest
   ```

2. **Run integration tests:**
   ```sh
   pytest --integration
   ```

### Deploying the Application

1. **Set up the production environment:**
   ```sh
   export FLASK_ENV=production
   ```

2. **Run the application:**
   ```sh
   flask run
   ```

## Major Components and Their Functionalities

### `app.py`
This file sets up the main Flask application, initializes extensions like SQLAlchemy and Flask-Login, and registers blueprints for different routes.

### `config.py`
Contains configuration settings for the application, including environment variables and database URI.

### `main.py`
Initializes and starts the Flask application, configuring logging and handling application startup.

### `models.py`
Defines the database models for the application, including `User`, `Scan`, and `Finding` models.

### `routes/auth.py`
Contains routes related to user authentication, including registration, login, and logout.

### `routes/dashboard.py`
Manages the dashboard routes, displaying user-specific data and recent scans.

### `routes/scans.py`
Handles routes related to scanning functionality, including initiating new scans and displaying scan details.

### `services/mistral_service.py`
Provides functionality to interact with the Mistral client, including starting scan workflows.

### `services/ml_service.py`
Manages machine learning tasks, such as analyzing code snippets for vulnerabilities using a pre-trained model.

### `services/scan_service.py`
Handles the logic for starting and managing vulnerability scans, including URL validation and database interactions.

### `services/snowflake_service.py`
Manages the connection to the Snowflake database and provides methods for storing scan findings.

### `README.md`
Provides an overview of the project, including features, project structure, installation instructions, and usage guidelines.

### `.github/workflows/ci.yml`
Defines the continuous integration workflow, including setting up Python, installing dependencies, running linters, and executing tests.

### `.github/workflows/deploy-production.yml`
Manages the deployment process to production, including setting up Python, caching dependencies, and running deployment scripts.

### `pyproject.toml`
Specifies project metadata and dependencies, including Python version requirements and package dependencies.

### `requirements.txt`
Lists the required Python packages for the project.
