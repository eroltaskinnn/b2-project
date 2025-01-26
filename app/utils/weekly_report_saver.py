import json
from datetime import datetime
from pathlib import Path


class WeeklyReportSaver:
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = Path(reports_dir)

    def save(self, report: dict) -> str:
        """Save report to file"""
        self.reports_dir.mkdir(exist_ok=True)

        report_file = self.reports_dir / f"weekly_report_{datetime.utcnow().strftime('%Y%m%d')}.json"

        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        return str(report_file)