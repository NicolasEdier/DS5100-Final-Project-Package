# DS5100-Final-Project-Package
This repo contains the "Final" package, which is a Die game Monte Carlo Simulation program. Using this package, you can create a specified Die, run a variation of games on it, then analyze the results. Thanks for checking it out!

## Metadata
- **Author:** Nicolas Edier
- **Project:** Monte Carlo Simulation
- **License:** MIT
- **Version:** 1.0.0
- **Description:** This project simulates a dice game involving one or more dice. The game can be played by rolling dice, and the results can be analyzed in various ways, including counting jackpots, face combinations, and permutations.

## Installation

### Importing
- To import, begin by cloning this repo in your preferred terminal of choice
- Then pip install within the repo
```bash
pip install .
```
- Navigate to python, import the package "Final", and you are ready to go
```python
import Final
```

## Synopsis

### Die Class
To create a die object, you pass an array of faces (distinct values) to the constructor:

```python
faces = np.array([1, 2, 3, 4, 5, 6])
die = Die(faces)
die.roll(5)  # Roll the die 5 times
die.change_weight(1, 2.5)  # Change the weight of face '1' to 2.5
die.show()  # Show the current state of the die 
```

### Game Class
To create a game, pass a list of Die objects to the Game constructor:

```python
die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
game = Game([die1, die2])
game.play(3)  # Roll the dice 3 times
game.show()  # Show the results in the 'wide' format
```

### Analyzer Class
To analyze the game results, pass a Game object to the Analyzer constructor:

```python
analyzer = Analyzer(game)
analyzer.jackpot()  # Count the number of jackpots (all faces the same)
analyzer.face_counts_per_roll()  # Get the face counts per roll
analyzer.combo_counts() # Get the count of distint combinations of faces rolled
analyzer.permutation_counts() # Get the count of distinct permutations of faces rolled
```

## API

### Die
The Die class simulates a die with customizable faces and weights.

Methods:
- __init__(faces): Initializes the die with the given faces (NumPy array). Raises TypeError if faces are not a NumPy array, and ValueError if faces are not distinct.
- change_weight(face, weight): Changes the weight of a specific face.
- roll(times=1): Rolls the die the specified number of times, returning the rolled face values.
- show(): Returns the current state of the die as a DataFrame.


### Game
The Game class simulates a game involving one or more dice.

Methods:
- __init__(dice): Initializes the game with a list of Die objects.
- play(rolls): Plays the game by rolling all dice the specified number of times.
- show(form="wide"): Shows the results of the most recent play. Accepts 'wide' or 'narrow' formats. Raises ValueError if the form is invalid.


### Analyzer
The Analyzer class analyzes the results of a game.

Methods:
- __init__(game): Initializes the analyzer with a Game object. Raises ValueError if the input is not a Game object.
- jackpot(): Computes the number of jackpots (all faces the same) in the game results.
- face_counts_per_roll(): Computes the face counts for each roll.
- combo_counts(): Computes the counts of distinct combinations of faces rolled.
- permutation_counts(): Computes the counts of distinct permutations of faces rolled.