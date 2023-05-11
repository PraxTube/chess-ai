# <center>Milestone I - Dummy AI</center>

## <center>Group C - The Plebs</center>

A chess AI written in Python.

## Chess Backend

The backend consists of mainly two classes, `GameState` and `Move`.
The first handles the whole board logic, what is the state of the board,
which moves were made, what are the current legal moves and so on.
The second class is used as a way to store moves, this is useful for
internal representation of the moves but also for debugging
(for instance one can simply overwrite the `__str__` to format the
move when printing it).
The current chess engine was mainly inspired by
[this repo](https://github.com/Jabezng2/Star-Wars-Chess-AI-Game)
which was in turn inspired by
[this YouTube series](https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_).

Before I started writing the current backend, I first used the
[python-chess](https://github.com/niklasf/python-chess) library
as the chess backend. Even though we aren't supposed to use it and I
had to write the backend in a short span of time, it was still very useful
because it showed me what the chess engine needed in order to make the AI work
(`make_move`, `undo_move`, `fen` representation, storing castle rights,
etc.). We are also going to compare the two chess backends in the
benchmark later.

There are still quite a lot of problems in the current chess engine

- Doesn't look for best promotion, always promotes to queen
- Fen loading only works somewhat (not for en passant and the move counter)
- When loading from a fen string there can be issues with the legal move gen
  if the board position has checks or en passant (and possibly other issues)
- The whole backend is using arrays which are very slow in python, possible
  solution could be to use `numpy.array` instead, though this would require
  a lot of refactoring (with many breaking changes)
- Quite many useless or redundant bits of code here and there

The reason our group actually decided to use python for the project
was because none of our members have any experience with low-level
programming languages. While this could have been a good opportunity
to learn `C` or `Rust`, the collective decided against it and
wanted to use python instead.

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
  <img src="benchmark-table.svg" alt="Table SVG Image">
</p>

Interesting to note is that the evaluation function
should be the same for both. The only reason they could be
different, is that the fen string of the python-chess is
very slow.

Also interesting to note is the fact that the current
engine, which is mainly written by people who did this
for the first time, is somehow faster then the python-chess
engine, which is written by many people and maintained since
a long time. It could be that python-chess is rather bloated
and as a result very slow. However I would doubt that bloat
would cause such a significance in performance.

The bottlenecks of the current engine seem to be the legal
move generation. That seems to be very fast in the python-chess
engine. If we can somehow get the speed from the python-chess
engine while maintaining the speed in the other categories
then we could potentially increase the performance by a huge
amount. However given that python-chess uses `0x88` as a backend
and the current engine uses arrays, this will most likely not be
possible.

The chess engine also doesn't yet implement
king of the hill win conditions.

## Dummy AI

The AI in it's current state can do the following

1. Communicate with the chess engine
1. Use the engine and minimax to find the best move
1. Basic evaluation using board material
1. Debug certain info about the game (current state and history)

There is a lot of room for improvement, mainly in the
best move search and the evaluation.

## Future Improvements

The main goal of improving this project is to increase performance
of the AI to allow for faster search of the best move.
The second goal is to keep maintainability as high as possible.
The following changes are going to address both of these goals.

### Engine Improvements

The engine in it's current state is very shaky and hard to read.
Docstring's would greatly help to understand the code, but are
to early as the engine is still going to be greatly refactored.
Another problem are huge `if-else` blocks. This can be
somewhat fixed through Guard Clauses. Another problem is that
there are many redundant or inefficient parts in the engine.
In order to address these issues, the following changes will
be implemented in the near future (hopefully till the next
milestone, but it's questionable if the time will be enough)

- Remove redundant classes
- Use more efficient data structures (`numpy.array`)
- Be consistent in the naming (`snake_casing`)
- Implement more Guard Clauses
- Split functions into smaller functions in order to try to reduce state
- ...

There are still many more improvements that can be made,
however for the time being the ones listed are already going to be
quite the time investment.

### AI Improvements

The AI doesn't have as many problems as the engine.
For the AI there are however still many changes that can be made

- Use `numpy.array` in the evaluation function
- Implement alpha-beta search
- Use better time management (move specific)
- Create a better evaluation function
    - Use piece to board aware array masks
    - Use check as a meassure
    - Use capture as a meassure
- Better move ordering
- Possibly cache the last found best move

## Final remarks

Many things went rather roughly, such as

- Team coordination (mainly due to the fact that only really
  one person can work on the engine)
- Writing the chess engine and debugging it
- Writing unit tests this early wasn't very useful
- Getting started was the hardest part, as we didn't quite
  know what to do (where to begin)

However there were also things that proofed to be very useful

- Benchmarking is extremely valuable
- Writing debugging tools early can pay of (same with logging tools)
- Failing fast (using python-chess to code up a simple AI) created
  a good base knowledge about what needs to be done
- Writing good git commits is extremely useful for both
  documentation (like this one) and overall work flow

An overall very teaching experience.
