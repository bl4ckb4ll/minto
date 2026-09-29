import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "minto_email_check.py"
RUBRIC = ROOT / "rubrics" / "email-v1.md"
FAKE = ROOT / "tests" / "fake_email_reviewer.py"


class EmailGateTest(unittest.TestCase):
    def run_cmd(self, *args):
        return subprocess.run(
            [sys.executable, str(CHECKER), *map(str, args)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def test_receipt_binds_exact_draft(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            draft = td / "draft.txt"
            receipt = td / "receipt.json"
            draft.write_text(
                "Hi Stella and Hailey,\n\n"
                "Thank you so much for developing Pythia. "
                "The README says to contact you if I want additional checkpoints.\n",
                encoding="utf-8",
            )

            check = self.run_cmd(
                "check",
                "--draft", draft,
                "--rubric", RUBRIC,
                "--receipt", receipt,
                "--model-id", "fake",
                "--model-revision", "test",
                "--reviewer", sys.executable, FAKE,
            )
            self.assertEqual(check.returncode, 0, check.stderr + check.stdout)
            self.assertTrue(receipt.exists())

            verify = self.run_cmd(
                "verify",
                "--draft", draft,
                "--rubric", RUBRIC,
                "--receipt", receipt,
                "--model-id", "fake",
                "--model-revision", "test",
            )
            self.assertEqual(verify.returncode, 0, verify.stderr + verify.stdout)
            self.assertIn("verified=true", verify.stdout)
            self.assertIn("passed=true", verify.stdout)

            draft.write_text(draft.read_text(encoding="utf-8") + "changed\n", encoding="utf-8")
            stale = self.run_cmd(
                "verify",
                "--draft", draft,
                "--rubric", RUBRIC,
                "--receipt", receipt,
            )
            self.assertNotEqual(stale.returncode, 0)
            self.assertIn("draft_hash", stale.stdout)

    def test_bad_opening_fails(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            draft = td / "draft.txt"
            receipt = td / "receipt.json"
            draft.write_text(
                "Hi Stella and Hailey,\n\n"
                "Thank you so much for developing Pythia. "
                "Anybody who doesn't use it, I don't understand why. "
                "It's like not using GDB to step through code.\n\n"
                "I would like some more checkpoints.\n",
                encoding="utf-8",
            )

            check = self.run_cmd(
                "check",
                "--draft", draft,
                "--rubric", RUBRIC,
                "--receipt", receipt,
                "--model-id", "fake",
                "--model-revision", "test",
                "--reviewer", sys.executable, FAKE,
            )
            self.assertNotEqual(check.returncode, 0)
            data = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertFalse(data["policy"]["passed"])
            self.assertIn("purpose_not_in_opening", data["policy"]["failures"])


if __name__ == "__main__":
    unittest.main()
