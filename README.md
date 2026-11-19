# Application-Log-Correction
Application Log Correlation & Timeline Reconstruction

Project Overview

Application Log Correlation & Timeline Reconstruction is a Python Flask-based web application designed to analyze multiple application log files, correlate related events, reconstruct chronological timelines, and identify potential anomalies.

The application helps developers understand application behavior, investigate failed requests, and identify performance issues through an interactive dashboard.

Features

- Upload multiple application log files.
- Parse log events and timestamps.
- Reconstruct chronological event timelines.
- Correlate related events using Request IDs.
- Detect out-of-order events.
- Identify failed requests.
- Analyze request duration.
- Detect slow requests and anomalies.
- Identify potential incident impact.
- Display log severity statistics.
- Interactive analysis dashboard.

Technologies Used

- Python
- Flask
- HTML5
- CSS3
- Git and GitHub
- Linux / Ubuntu

Project Structure

Application-Log-Correlation/
├── app.py
├── log_engine.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── sample_logs/
    ├── app1.log
    └── app2.log

Installation and Setup

1. Clone the repository

git clone https://github.com/rvit24bcs060rvitm-stack/Application-Log-Correction.git

2. Navigate to the project folder

cd Application-Log-Correlation

3. Create a virtual environment

python3 -m venv venv

4. Activate the environment

source venv/bin/activate

5. Install dependencies

pip install -r requirements.txt

6. Run the application

python app.py

Open your browser and visit:

http://127.0.0.1:5000

Application Workflow

1. Upload application log files.
2. Parse timestamps and log events.
3. Correlate events using Request IDs.
4. Reconstruct chronological timelines.
5. Analyze failed and slow requests.
6. Detect anomalies and out-of-order events.
7. View analysis results on the dashboard.

Project Objective

The main objective is to simplify application log analysis and help developers identify errors, investigate incidents, and understand request execution flows.

Author

Aishwarya

License

This project is developed for academic purposes.

## Application Dashboard

![LogFusion Dashboard](screenshots/dashboard.png)

