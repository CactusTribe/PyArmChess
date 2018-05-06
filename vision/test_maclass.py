import unittest

from vision.maclass import MaClass


class MaClassTest(unittest.TestCase):
    """Test MaClass."""

    def setUp(self):
        """Initialise des tests."""
        self.liste = list(range(10))

    def test_affichemoi(self):
        """Test le fonctionnement de la fonction affichemoi."""
        result = MaClass().afficheMoi()
        self.assertEqual(result, "Salut ça va?")

    def test_affiche2(self):
        """Test le fonctionnement de la fonction affiche2."""
        result = MaClass().affiche2()
        self.assertEqual(result, 2)
