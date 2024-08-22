import os
import unittest
from unittest.mock import patch
from src.utils.helper.is_osx import is_osx


class TestIsOsx(unittest.TestCase):
    @patch("os.uname")
    def test_is_osx_returns_true_for_darwin(self, mock_uname):
        mock_uname.return_value = os.uname_result(("Darwin", "", "", "", ""))
        self.assertTrue(is_osx())

    @patch("os.uname")
    def test_is_osx_returns_false_for_non_darwin(self, mock_uname):
        mock_uname.return_value = os.uname_result(("Linux", "", "", "", ""))
        self.assertFalse(is_osx())


if __name__ == "main":
    unittest.main()
