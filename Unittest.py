import unittest
import numpy as np
import pandas as pd
from MCPackage.MCProgram import Die, Game, Analyzer


class TestDie(unittest.TestCase):
    def test_die_initializer_valid(self):
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        self.assertEqual(list(die.show().index), [1, 2, 3, 4, 5, 6])
        self.assertTrue((die.show()['weight'] == 1.0).all())
    
    def setUp(self):
        self.die = Die(np.array(['A', 'B', 'C']))

    def test_change_weight(self):
        self.die.change_weight('A', 2.0)
        self.assertEqual(self.die.show().at['A', 'weight'], 2.0)

    def test_roll(self):
        result = self.die.roll(5)
        self.assertEqual(len(result), 5)

    def test_show(self):
        self.assertEqual(len(self.die.show()), 3)


class TestGame(unittest.TestCase):
    def test_game_initializer_valid(self):
        dice = [Die(np.array([1, 2, 3])), Die(np.array(['a', 'b', 'c']))]
        game = Game(dice)
        self.assertEqual(len(game._dice), 2)
        self.assertIsInstance(game._dice[0], Die)
        self.assertIsInstance(game._dice[1], Die)
        
    def setUp(self):
        self.dice = [Die(np.array(['A', 'B', 'C'])) for _ in range(3)]
        self.game = Game(self.dice)

    def test_play(self):
        self.game.play(5)
        self.assertEqual(self.game.show().shape[0], 5)

    def test_show(self):
        self.game.play(5)
        self.assertEqual(self.game.show("wide").shape[0], 5)


class TestAnalyzer(unittest.TestCase):
    def test_analyzer_initializer_valid(self):
        dice = [Die(np.array([1, 2, 3])), Die(np.array(['a', 'b', 'c']))]
        game = Game(dice)
        game.play(5)
        analyzer = Analyzer(game)
        self.assertTrue(isinstance(analyzer._results, pd.DataFrame))
        self.assertEqual(analyzer._results.shape[0], 5)
    
    def setUp(self):
        dice = [Die(np.array(['A', 'B', 'C'])) for _ in range(2)]
        game = Game(dice)
        game.play(10)
        self.analyzer = Analyzer(game)

    def test_jackpot(self):
        self.assertIsInstance(self.analyzer.jackpot(), int)

    def test_face_counts_per_roll(self):
        result = self.analyzer.face_counts_per_roll()
        self.assertTrue(isinstance(result, pd.DataFrame))

    def test_combo_counts(self):
        result = self.analyzer.combo_counts()
        self.assertTrue(isinstance(result, pd.DataFrame))

    def test_permutation_counts(self):
        result = self.analyzer.permutation_counts()
        self.assertTrue(isinstance(result, pd.DataFrame))


if __name__ == "__main__":
    with open("test_results.txt", "w") as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(testRunner=runner, exit=False)
