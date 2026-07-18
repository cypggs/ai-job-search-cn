"""Tests for the /html-report command and its gitignore rule."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COMMAND_FILE = REPO_ROOT / ".claude" / "commands" / "html-report.md"
GITIGNORE = REPO_ROOT / ".gitignore"


class HtmlReportCommandFileTests(unittest.TestCase):
    def test_command_file_exists(self):
        self.assertTrue(COMMAND_FILE.exists(), f"{COMMAND_FILE} not found")

    def test_command_file_starts_with_correct_header(self):
        text = COMMAND_FILE.read_text(encoding="utf-8")
        first_line = text.lstrip().splitlines()[0]
        self.assertTrue(
            first_line.startswith("# /html-report"),
            f"Command file must start with '# /html-report', got: {first_line!r}",
        )

    def test_command_file_is_non_empty(self):
        text = COMMAND_FILE.read_text(encoding="utf-8").strip()
        self.assertGreater(len(text), 100, "Command file appears suspiciously short")


class HtmlReportGitignoreTests(unittest.TestCase):
    def test_reports_folder_is_gitignored(self):
        rules = {line.strip() for line in GITIGNORE.read_text(encoding="utf-8").splitlines()}
        self.assertIn(
            "reports/",
            rules,
            "reports/ must be listed in .gitignore — generated dashboards are personal output",
        )


if __name__ == "__main__":
    unittest.main()
