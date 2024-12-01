import numpy as np
import pandas as pd
from itertools import permutations, combinations
from collections import Counter


class Die:
    """
    A class to simulate a die with customizable faces and weights.

    Attributes:
        _faces (numpy array): The faces of the die.
        _weights (pandas DataFrame): A private data frame storing faces and their weights.
    """

    def __init__(self, faces):
        """
        Initialize the die with given faces.

        Args:
            faces (numpy array): A NumPy array of distinct face values (strings or numbers).

        Raises:
            TypeError: If `faces` is not a NumPy array.
            ValueError: If `faces` contains duplicate values.
        """
        if not isinstance(faces, np.ndarray):
            raise TypeError("Faces must be a NumPy array.")
        if len(faces) != len(set(faces)):
            raise ValueError("Faces must be distinct.")
        self._weights = pd.DataFrame({'face': faces, 'weight': 1.0}).set_index('face')

    def change_weight(self, face, weight):
        """
        Change the weight of a specific face.

        Args:
            face: The face value whose weight is to be changed.
            weight (float): The new weight to assign to the face.

        Raises:
            IndexError: If the face is not a valid die face.
            TypeError: If weight is not numeric.
        """
        if face not in self._weights.index:
            raise IndexError("Face not found in die.")
        try:
            weight = float(weight)
        except ValueError:
            raise TypeError("Weight must be numeric.")
        self._weights.at[face, 'weight'] = weight

    def roll(self, times=1):
        """
        Roll the die one or more times.

        Args:
            times (int): The number of times to roll the die. Defaults to 1.

        Returns:
            list: A list of rolled face values.
        """
        return list(self._weights.sample(n=times, weights='weight', replace=True).index)

    def show(self):
        """
        Show the current state of the die.

        Returns:
            pandas DataFrame: A copy of the data frame with faces and weights.
        """
        return self._weights.copy()


class Game:
    """
    A class to simulate a game involving one or more similar dice.

    Attributes:
        _dice (list): A list of Die objects.
        _results (pandas DataFrame): A private data frame storing the results of the most recent play.
    """

    def __init__(self, dice):
        """
        Initialize the game with a list of dice.

        Args:
            dice (list): A list of Die objects.
        """
        self._dice = dice
        self._results = pd.DataFrame()

    def play(self, rolls):
        """
        Play the game by rolling all dice a specified number of times.

        Args:
            rolls (int): The number of times to roll the dice.
        """
        results = {f"Die_{i}": die.roll(rolls) for i, die in enumerate(self._dice)}
        self._results = pd.DataFrame(results)

    def show(self, form="wide"):
        """
        Show the results of the most recent play.

        Args:
            form (str): The format of the results ('wide' or 'narrow'). Defaults to 'wide'.

        Returns:
            pandas DataFrame: The results in the specified format.

        Raises:
            ValueError: If the form is not 'wide' or 'narrow'.
        """
        if form == "wide":
            return self._results.copy()
        elif form == "narrow":
            return self._results.stack().to_frame("face").reset_index(names=["roll", "die"])
        else:
            raise ValueError("Form must be 'wide' or 'narrow'.")


class Analyzer:
    """
    A class to analyze the results of a game.

    Attributes:
        _game (Game): The game object to analyze.
        _results (pandas DataFrame): The results of the most recent game play.
    """

    def __init__(self, game):
        """
        Initialize the analyzer with a game object.

        Args:
            game (Game): The game object.

        Raises:
            ValueError: If the input is not a Game object.
        """
        if not isinstance(game, Game):
            raise ValueError("Input must be a Game object.")
        self._game = game
        self._results = game.show()

    def jackpot(self):
        """
        Compute the number of jackpots (all faces the same) in the game results.

        Returns:
            int: The number of jackpots.
        """
        return int(self._results.apply(lambda row: len(set(row)) == 1, axis=1).sum())

    def face_counts_per_roll(self):
        """
        Compute the face counts for each roll.

        Returns:
            pandas DataFrame: A data frame with face counts for each roll.
        """
        return self._results.apply(lambda row: row.value_counts(), axis=1).fillna(0).astype(int)

    def combo_counts(self):
        """
        Compute the counts of distinct combinations of faces rolled.

        Returns:
            pandas DataFrame: A data frame of combinations and their counts.
        """
        combos = self._results.apply(lambda row: tuple(sorted(row)), axis=1)
        return pd.DataFrame.from_dict(Counter(combos), orient='index', columns=['count'])

    def permutation_counts(self):
        """
        Compute the counts of distinct permutations of faces rolled.

        Returns:
            pandas DataFrame: A data frame of permutations and their counts.
        """
        perms = self._results.apply(lambda row: tuple(row), axis=1)
        return pd.DataFrame.from_dict(Counter(perms), orient='index', columns=['count'])
