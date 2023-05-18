# <center>Milestone II - Basic AI</center>

## <center>Group C - The Plebs</center>

A chess AI written in Python.

## Changes to the Chess Backend

There weren't that many changes to the backend in this
version. Mainly some quality of life improvements and
a few helper functions to debug and log chess games
better. Nothing of the actual logic changed.

Potential improvements for the the future are

- Use numpy array's for the board representation
- Reduce OOP and instead lean more towards FP
- Split logic into smaller functions

Overall, the improvements range from performance
to maintainability.

## Benchmarks

The benchmarks in the table below have the following categories

- **Fen Conversion** Convert internal board to a fen string
- **Legal Move Gen** Generate all legal moves for a given board
- **Making Move** Make a move on the current board and undo it
- **Evaluate Board** Evaluate the board, here a simple material calculation
- **Best Move Search** Find the best move of a given board, with depth 1

The boards that were used

- **Early-Game** 
  `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`
- **Mid-Game**
  `r3k2r/ppp1bppp/b1n2n2/1N2B3/2B1q3/2Q1PN2/PPP2PPP/R3K2R b KQkq - 0 1`
- **Late-Game**
  `4k3/8/8/3PP3/3pp3/8/8/3K4 w - - 0 1`.

<p align="center">
  <img src="benchmark-tables.svg" alt="Tables SVG Image">
</p>

The tests were run on a PC with the following specs

- CPU: Intel i5-4590, Threads: 4, Cores: 4, 3.7GHz

- RAM: 24GB DDR3

CONTENT

## Basic AI

The previous AI was able to do the following

1. Communicate with the chess engine
1. Use the engine and minimax to find the best move
1. Basic evaluation using board material
1. Debug certain info about the game (current state and history)

The new AI can also do these

1. Alpha-beta search
1. Better evaluation function, started to use PeSTO
1. Slightly better time management

The current biggest problem is the chess backend and it's
incompatability with the evaluation function.
We are using numpy arrays to calculate the value for the
board, however the chess engine uses python lists to store
the board information.

The reason we didn't directly implement the board with numpy
was because we wanted to get a finished engine instead of
plan too much ahead. This comes to bite us in the ass now,
as refactoring the engine to use numpy instead of lists
will require a massive amount of time and effort.

## Future Improvements

For the next milestone we would like to focus
heavily on the chess engine.
If we don't clean up our foundation,
which is our engine, we will only run into more and
more bugs. On that note, the following points are a
collection of possible improvements for the engine
noted in the previous
[milestone documentation]("../one/README.md")

- Remove redundant classes
- Use more efficient data structures (`numpy.array`)
- Be consistent in the naming (`snake_casing`)
- Implement more Guard Clauses
- Split functions into smaller functions in order to try to reduce state
- ...

These improvements should increase both
maintainability as well as performance of the AI.

## Final remarks

Given that the time frame was much shorter compared to the
first milestone there is much less to say. We did improve our
team work though, mainly because we have much more clear
tasks now (in the form of issues) which are easier to
complete.

Overall the development seems to be heading in a good direction.
