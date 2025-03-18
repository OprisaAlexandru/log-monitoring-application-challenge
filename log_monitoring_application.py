import logging
from datetime import datetime
import sys
import csv

def parse_log_lines(line: str):
    parts = [part.strip() for part in line.split(",")]
    if len(parts) != 4:
        raise ValueError("Invalid log line format")
    time_str, description, event, pid = parts
    timestamp = datetime.strptime(time_str, "%H:%M:%S")
    return timestamp, description, event, pid

def process_log_lines(lines):
    jobs = {}
    for line in lines:
        if not line.strip():
            continue
        try:
            timestamp, description, event, pid = parse_log_lines(line)
        except Exception as e:
            logging.error("Error parsing line: %s. Exception: %s", line, e)

        if pid not in jobs:
            jobs[pid] = {"description": description, "start": None, "end": None}
        if event.upper() == "START":
            jobs[pid]['start'] = timestamp
        elif event.upper() == "END":
            jobs[pid]['end'] = timestamp
        else:
            logging.error("Unknown event type: %s in line %s", event, line)
    return jobs

def generate_report(jobs):
    report_lines = []

    csv_headers = [ "PID", "Job Description", "Start time", "End time", 'Duration (minutes)', "Potential issues"]

    for pid, info in jobs.items():
        if info['start'] and info['end']:
            duration_minutes = ((info['end'] - info['start']).total_seconds()) / 60
            report_line = (f"PID: {pid}, Job: {info['description']}, Start: {info['start'].time()}, End: {info['end'].time()}, Duration: {duration_minutes:.2f} minutes")
            
            if duration_minutes > 10:
                logging.error("Job %s took longer than 10 minutes: %.2f minutes", pid, duration_minutes)
                report_line += ", Error: Job exceeded 10 minutes"
            elif duration_minutes > 5:
                logging.warning("Job %s took longer than 5 minutes: %.2f minutes", pid, duration_minutes)
                report_line += ", Warning: Job exceeded 5 minutes"
            
            report_lines.append(report_line)
        else:
            logging.error("Incomplete log for job %s", pid)
    return report_lines

def process_logs(filename: str):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        logging.error("Failed to read file %s: %s", filename, e)
        return {}
    return process_log_lines(lines)

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    filename = "logs.log"
    output_file = "job_report.csv"
    jobs = process_logs(filename)
    report = generate_report(jobs)

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for line in report:
            writer.writerow([line])
        

if __name__ == '__main__':
    main()