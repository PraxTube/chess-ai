<p align="center">
    <h1>Milestone I - Dummy AI</h1>
    <h2>Group C - The Plebs</h2>
</p>

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
because it showed me what the chess engine needed to work for the AI
(`make_move`, `undo_move`, `fen` representation, storing castle rights,
etc.). We are also going to compare the two chess backends in the
benchmark later.

There are still quite a lot of problems in the current chess engine

- Always promoting to queen
- Fen loading only works somewhat (not for en passant and the move counter)
- When loading from a fen string there can be issues with the legal move gen
  if the board position has checks or en passant (and possibly other issues)
- The whole backend is using arrays which are very slow in python, possible
  solution could be to use `numpy.array` instead, though this would require
  a lot of refactoring (with many breaking changes)
- Lastly there are some useless bits of code here and there

The reason our group actually decided to use python for the project
was because none of our members have any experience with low-level
programming languages. While this could have been a good opportunity
to learn `C` or `Rust`, the collective decided against it and
wanted to use python instead.

## Benchmarks

\begin{table}[ht!]%
	\caption{Benchmark TEST}
	\label{tab:benchmark}
	\centering %
	\begin{tabular}{cccc}
		\toprule
		1 & 2 & 3 & 4 \\ \toprule
		1 & 2 & 3 & 4 \\
		1 & 2 & 3 & 4 \\
		1 & 2 & 3 & 4 \\ \midrule[0.1mm]
		1 & 2 & 3 & 4 \\
		1 & 2 & 3 & 4 \\
		1 & 2 & 3 & 4 \\ \midrule[0.1mm]
		1 & 2 & 3 & 4 \\
		1 & 2 & 3 & 4 \\
		1 & 2 & 3 & 4 \\ \midrule[0.1mm]
		1 & 2 & 3 & 4 \\
		1 & 2 & 3 & 4 \\
		1 & 2 & 3 & 4 \\ \midrule[0.1mm]
		1 & 2 & 3 & 4 \\
		1 & 2 & 3 & 4 \\
		1 & 2 & 3 & 4 \\ \midrule[0.1mm]
		1 & 2 & 3 & 4 \\ \bottomrule
	\end{tabular}
\end{table}

- Show Benchmarks
- also show python-chess benchmarks, and mention that those are slower
- also note the current bottlenecks and possible explanations

## Dummy AI

- What can the AI do?
- Where are already potential bottlenecks?

## Future Improvements

- state how to address the bottlenecks
- how the benchmarks will most likely change with the development of the AI
- What worked well and what did not (for instance benchmarks useful, unit tests too)
