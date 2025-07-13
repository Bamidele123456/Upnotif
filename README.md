# Upnotif

A Flask web application that allows users to register their email and an RSS feed URL (e.g., Upwork job feed). The app monitors the RSS feed and sends email notifications when new jobs are posted.

## Features
- User registration with email and RSS feed URL
- Periodic checking of RSS feeds for new jobs
- Email notifications for new job postings
- MongoDB for user data storage

## Setup Instructions

### Prerequisites
- Python 3.8+
- MongoDB Atlas account (or local MongoDB instance)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Bamidele123456/Upnotif.git
   cd Upnotif
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
- Update the MongoDB URI and email credentials in `app.py`:
  - `uri`: Your MongoDB connection string
  - `sender_email` and `password`: Your Gmail address and app password

### Running the App
```bash
python app.py
```
The app will be available at [http://localhost:8080](http://localhost:8080).

## Usage
1. Go to `/testing` to access the registration form.
2. Enter your email and the RSS feed URL you want to monitor.
3. The app will periodically check the feed and send you email notifications for new jobs.

## File Structure
```
.
├── app.py                # Main Flask app
├── requirements.txt      # Python dependencies
├── templates/
│   └── register.html     # Registration form
├── .gitignore            # Git ignore file
```

## Notes
- The `.idea/` directory is ignored (for JetBrains IDE users).
- Email credentials and MongoDB URI should be kept secure and not committed to public repositories.

## License
MIT 