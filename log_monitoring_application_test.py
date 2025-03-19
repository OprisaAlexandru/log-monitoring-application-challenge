import unittest
from io import StringIO
import logging
from log_monitoring_application import parse_log_lines, process_log_lines, generate_report

class Test(unittest.TestCase):
    def setUp(self):
        self.sample_logs = [
            "11:35:23,scheduled task 032, START,37980",
            "11:35:56,scheduled task 032, END,37980",
            "11:36:11,scheduled task 796, START,57672",
            "11:39:26,background job dej, START,90812",
            "11:41:55,background job ulp, END,60134",
            "11:47:18,scheduled task 796, END,57672", 
            "11:36:58,background job wmy, START,81258",
            "11:42:58,background job wmy, END,81258",
            "Invalid LOG Line"
        ]
    
    def test_parse_log_line(self):
        line = self.sample_logs[0]
        timestamp, description, event, pid = parse_log_lines(line)
        self.assertEqual(timestamp.hour, 11)
        self.assertEqual(description, "scheduled task 032")
        self.assertEqual(event, "START")
        self.assertEqual(pid, "37980")

    def test_process_log_lines(self):
        jobs = process_log_lines(self.sample_logs)
        self.assertIn("37980", jobs)
        self.assertIn("57672", jobs)
        self.assertIn("81258", jobs)

    def test_generate_report(self):
        jobs = process_log_lines(self.sample_logs)
        report = generate_report(jobs)
        self.assertEqual(len(report), 3)

    def test_logging(self):
        log_stream = StringIO()
        handler = logging.StreamHandler(log_stream)
        logger = logging.getLogger()
        logger.addHandler(handler)

        jobs = process_log_lines(self.sample_logs)
        generate_report(jobs)

        logger.removeHandler(handler)
        log_contents = log_stream.getvalue()

        self.assertIn("Job 57672 took longer than 10 minutes: 11.12 minutes", log_contents)
        self.assertNotIn("Job 37980 took longer than 5 minutes: 5 minutes", log_contents)
        self.assertIn("Incomplete log for job 90812", log_contents)
        self.assertIn("Error parsing line", log_contents)

if __name__ == "__main__":
    unittest.main()