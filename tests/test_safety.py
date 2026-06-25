import unittest

from zai_coder.core.safety import SafetyPolicy


class SafetyPolicyTest(unittest.TestCase):
    def test_blocks_git_add_dot(self):
        self.assertFalse(SafetyPolicy().check_command("git add .").allowed)

    def test_blocks_no_verify(self):
        self.assertFalse(SafetyPolicy().check_command("git commit --no-verify -m x").allowed)

    def test_allows_git_status(self):
        self.assertTrue(SafetyPolicy().check_command("git status --short").allowed)

    def test_blocks_zlms(self):
        self.assertFalse(SafetyPolicy().check_path("apps/zlms/file.ts").allowed)


if __name__ == "__main__":
    unittest.main()
