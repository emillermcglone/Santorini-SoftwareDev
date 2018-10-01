# Santorini

Santorini is a two-player board game. The board is a 6 x 6 grid of squares. Each player is allocated two workers. At the beginning of the game, the players place their workers on four distinct squares of the board, one at a time. The "foo-est" player starts, and the players take turns placing their workers.

Once the workers are placed, the players take turns to move their workers and use them to construct buildings. A building consists of up to four floors. Workers can climb buildings (but not to the forth floor) and can jump from buildings. The first player to place a worker on the third floor wins.

## Directory Structure

* Admin: Administrator specific code 
  
* Player: Player specific code

* Common: Common data and knowledge for both administrative and player components
  
* Lib: Library like code

## Running Tests

Run the following shell command:

```
python3 Command/tests/test_suite.py
```