# Log Monitoring Application

This log_monitoring_application script processes a log file ('logs.log') and produces a report that logs a warning if a job took longer than 5 minutes and an error if a job took longer than 10 minutes. It will also create a csv file containing all the data following the format:
    - PID, Job description, Start time, End time, Duration and the log if there is the case

Example: 
    "PID: 57672, Job: scheduled task 796, Start: 11:36:11, End: 11:36:18, Duration: 0.12 minutes"
    "PID: 87228, Job: scheduled task 268, Start: 11:44:25, End: 11:53:53, Duration: 9.47 minutes, Warning: Job exceeded 5 minutes"
    "PID: 81258, Job: background job wmy, Start: 11:36:58, End: 11:51:44, Duration: 14.77 minutes, Error: Job exceeded 10 minutes"

## How to run:
1. Ensure that you have Python 3 installed.
2. Place your 'logs.log' file in the same directory as the script.
3. Run the script using the command:
    python log_monitoring_application.py

## Code Structure:
- **parse_log_line**: Parses a singe log line and returns the individual components (PID, Job, Start time, End time)
- **process_log_lines**: Processes a list of log lines into job entries.
- **process_logs**: Reads the logs file and convets it into a dictionary.
- **generate_report**: Finding out the job duration and logs warnings/errors based on the defined logic.