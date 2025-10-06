import unittest
import pygame

class TestGame(unittest.TestCase):
    def test_game_import(self):
        """
        Tests if the main game module can be imported without errors.
        This is a basic smoke test to catch syntax errors or issues
        with initial asset loading that happens at the module level.
        """
        try:
            import main
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Failed to import main.py: {e}")

if __name__ == '__main__':
    unittest.main()
