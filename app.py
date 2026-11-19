from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import tempfile

from log_engine import (
    read_log_files,
    reconstruct_timeline,
    correlate_events,
    detect_event_issues,
    detect_failed_requests,
    calculate_request_durations,
    detect_slow_requests,
    detect_anomalies,
    analyze_incident_impact,
    calculate_severity_statistics
)

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        uploaded_files = request.files.getlist("logs")

        if not uploaded_files or not any(f.filename for f in uploaded_files):

            return render_template(
                "index.html",
                error="Please select at least one log file."
            )

        try:

            with tempfile.TemporaryDirectory() as temp_folder:

                for file in uploaded_files:

                    if file.filename:

                        filename = secure_filename(file.filename)

                        if filename:
                            file.save(
                                os.path.join(temp_folder, filename)
                            )

                events = read_log_files(temp_folder)

                timeline = reconstruct_timeline(events)

                correlated = correlate_events(events)

                issues = detect_event_issues(correlated)

                failed_requests = detect_failed_requests(correlated)

                durations = calculate_request_durations(correlated)

                slow_requests = detect_slow_requests(
                    durations,
                    threshold=30
                )

                anomalies = detect_anomalies(
                    durations,
                    failed_requests,
                    slow_requests
                )

                incident_impact = analyze_incident_impact(
                    failed_requests,
                    slow_requests,
                    anomalies
                )

                severity_statistics = calculate_severity_statistics(
                    events
                )

                return render_template(
                    "index.html",

                    timeline=timeline,
                    correlated=correlated,
                    issues=issues,

                    total_events=len(events),
                    total_requests=len(correlated),

                    failed_requests=failed_requests,
                    durations=durations,
                    slow_requests=slow_requests,
                    anomalies=anomalies,
                    incident_impact=incident_impact,
                    severity_statistics=severity_statistics
                )

        except Exception as error:

            return render_template(
                "index.html",
                error=f"Error processing logs: {error}"
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)