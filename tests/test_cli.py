import contextlib
import io
import os
import unittest
from unittest.mock import patch

import run


class CliTests(unittest.TestCase):
    def test_bad_flag_is_rejected_before_key_check(self):
        with patch.dict(os.environ, {}, clear=True), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as e:
                run.main(["--definitely-not-real"])
        self.assertEqual(e.exception.code, 2)

    def test_unknown_demo_is_rejected_before_key_check(self):
        with patch.dict(os.environ, {}, clear=True), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as e:
                run.main(["not_a_demo"])
        self.assertEqual(e.exception.code, 2)

    def test_missing_key_still_fails_fast_for_valid_demo(self):
        with patch.dict(os.environ, {"PYTHON_DOTENV_DISABLED": "1"}, clear=True):
            self.assertEqual(run.main(["citations"]), 1)


if __name__ == "__main__":
    unittest.main()
