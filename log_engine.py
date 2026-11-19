import os
import re
from datetime import datetime
from collections import Counter


# -------------------------------
# READ LOG FILES
# -------------------------------
def read_log_files(folder_path):
    events = []

    timestamp_pattern = re.compile(
        r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}"
    )

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if not os.path.isfile(file_path):
            continue

        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:

            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    continue

                match = timestamp_pattern.search(line)

                if not match:
                    continue

                try:
                    timestamp = datetime.fromisoformat(
                        match.group().replace(" ", "T")
                    )
                except ValueError:
                    continue

                events.append({
                    "timestamp": timestamp,
                    "message": line,
                    "source": filename,
                    "line_number": line_number,
                    "severity": detect_severity(line)
                })

    return events


# -------------------------------
# SEVERITY CLASSIFICATION
# -------------------------------
def detect_severity(message):

    text = message.upper()

    if re.search(r"\bCRITICAL\b|\bFATAL\b", text):
        return "CRITICAL"

    if re.search(r"\bERROR\b|\bFAILED\b|\bFAILURE\b|\bEXCEPTION\b", text):
        return "ERROR"

    if re.search(r"\bWARN(?:ING)?\b", text):
        return "WARNING"

    if re.search(r"\bDEBUG\b|\bTRACE\b", text):
        return "DEBUG"

    if re.search(r"\bINFO\b|\bINFORMATION\b", text):
        return "INFO"

    return "UNKNOWN"


# -------------------------------
# CHRONOLOGICAL TIMELINE
# -------------------------------
def reconstruct_timeline(events):
    return sorted(events, key=lambda event: event["timestamp"])


# -------------------------------
# REQUEST ID EXTRACTION
# -------------------------------
def extract_request_id(message):

    patterns = [
        r"request_id\s*[=:]\s*([A-Za-z0-9_-]+)",
        r"correlation_id\s*[=:]\s*([A-Za-z0-9_-]+)",
        r"request\s*id\s*[=:]\s*([A-Za-z0-9_-]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)

        if match:
            return match.group(1)

    return None


# -------------------------------
# EVENT CORRELATION
# -------------------------------
def correlate_events(events):

    correlated = {}

    for event in events:

        request_id = extract_request_id(event["message"])

        if request_id:

            correlated.setdefault(request_id, []).append(event)

    for request_id in correlated:

        correlated[request_id].sort(
            key=lambda event: event["timestamp"]
        )

    return correlated


# -------------------------------
# FAILED REQUEST DETECTION
# -------------------------------
def detect_failed_requests(correlated_events):

    failed_requests = []

    failure_keywords = [
        "ERROR",
        "FAILED",
        "FAILURE",
        "EXCEPTION",
        "TIMEOUT",
        "DENIED",
        "UNAUTHORIZED",
        "HTTP 4",
        "HTTP 5",
        "STATUS=500",
        "STATUS=404"
    ]

    for request_id, events in correlated_events.items():

        messages = " ".join(
            event["message"].upper()
            for event in events
        )

        if any(keyword in messages for keyword in failure_keywords):

            failed_requests.append({
                "request_id": request_id,
                "events": events,
                "details": "Failure-related message detected",
                "severity": "ERROR"
            })

    return failed_requests


# -------------------------------
# REQUEST DURATION ANALYSIS
# -------------------------------
def calculate_request_durations(correlated_events):

    durations = []

    for request_id, events in correlated_events.items():

        if len(events) < 2:
            continue

        start_time = min(
            event["timestamp"] for event in events
        )

        end_time = max(
            event["timestamp"] for event in events
        )

        duration = (end_time - start_time).total_seconds()

        durations.append({
            "request_id": request_id,
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration
        })

    return durations


# -------------------------------
# SLOW REQUEST DETECTION
# -------------------------------
def detect_slow_requests(durations, threshold=30):

    slow_requests = []

    for request in durations:

        if request["duration"] >= threshold:

            slow_requests.append({
                "request_id": request["request_id"],
                "duration": request["duration"],
                "severity": "WARNING",
                "details": (
                    f"Request took {request['duration']} seconds"
                )
            })

    return slow_requests


# -------------------------------
# ANOMALY DETECTION
# -------------------------------
def detect_anomalies(
    durations,
    failed_requests,
    slow_requests
):

    anomalies = []

    failed_ids = {
        request["request_id"]
        for request in failed_requests
    }

    slow_ids = {
        request["request_id"]
        for request in slow_requests
    }

    for request in durations:

        request_id = request["request_id"]

        if request_id in failed_ids:

            anomalies.append({
                "request_id": request_id,
                "type": "Failed Request",
                "severity": "ERROR",
                "details": "Failure-related events found"
            })

        if request_id in slow_ids:

            anomalies.append({
                "request_id": request_id,
                "type": "Slow Request",
                "severity": "WARNING",
                "details": (
                    f"Request took {request['duration']} seconds"
                )
            })

    return anomalies


# -------------------------------
# INCIDENT IMPACT ANALYSIS
# -------------------------------
def analyze_incident_impact(
    failed_requests,
    slow_requests,
    anomalies
):

    impacted_requests = set()

    for request in failed_requests:
        impacted_requests.add(request["request_id"])

    for request in slow_requests:
        impacted_requests.add(request["request_id"])

    for anomaly in anomalies:
        impacted_requests.add(anomaly["request_id"])

    total_impacted = len(impacted_requests)

    if total_impacted == 0:
        impact_level = "LOW"
        message = "No significant request impact detected."

    elif total_impacted <= 2:
        impact_level = "MEDIUM"
        message = "Limited number of requests affected."

    elif total_impacted <= 5:
        impact_level = "HIGH"
        message = "Multiple requests are affected."

    else:
        impact_level = "CRITICAL"
        message = "Large number of requests are affected."

    return {
        "level": impact_level,
        "total_impacted": total_impacted,
        "message": message,
        "request_ids": sorted(impacted_requests)
    }


# -------------------------------
# SEVERITY STATISTICS
# -------------------------------
def calculate_severity_statistics(events):

    statistics = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0,
        "DEBUG": 0,
        "UNKNOWN": 0
    }

    for event in events:

        severity = event["severity"]

        if severity in statistics:
            statistics[severity] += 1
        else:
            statistics["UNKNOWN"] += 1

    return statistics


# -------------------------------
# DETECT EVENT ISSUES
# -------------------------------
def detect_event_issues(correlated_events):

    issues = []

    for request_id, events in correlated_events.items():

        if len(events) < 2:

            issues.append({
                "request_id": request_id,
                "issue": "Incomplete Request",
                "details": "Only one event found for this request."
            })

    return issues