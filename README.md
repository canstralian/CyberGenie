# CyberGenie

CyberGenie is a Flask-based web application that leverages SQLAlchemy for ORM and Flask-Login for user authentication.

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
