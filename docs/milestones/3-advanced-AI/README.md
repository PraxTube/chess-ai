# <center>Milestone III - Advanced AI</center>

## <center>Group C - The Plebs</center>

A chess AI written in Python.

## Summary


## Changes to the Chess Backend

The backend was in dire need of a restructure.
It was created it in a rush to meet the deadline
of the first milestone and was therefore not written
with the most maintainability in mind.
The following things were changed:

- Use `snake_casing` consistently
- Class `CastlingRights` and replace with a `list`
- Add guard clauses to reduce indentation
- Turn `debug_info` from `dict` to a `class` (in `log.py`)
- Use `list` of `int` for board instead of `str`

For a more detailed description see the
commit history in #37.

The way I restructured the backend was actually
very teaching. At first I wanted to simply write
the whole backend from scratch with the new changes.
However I quickly realized that this wouldn't really
work. So instead I opted to apply the changes in layers,
where after each change the whole backend should still
be working.

This was extremely effective. It not only allowed to
assert that the changes I made didn't introduce new bugs,
but it also made commiting very clean, and also made sure
that I would be able to track down bugs if they did occur.
So in future projects I will use the same way to restructure
bigger files.

## AI

There were quite a lot of changes regarding the AI.
I implemented the following changes:

- Check if given node is terminal node (checkmate/stalemate)
  as opposed to only checking `depth == 0`
- Add a proper king of the hill victory condition (and properly test it)
- Try to add [transposition tables but fail miserably](./transposition-tables.md)

TODO

## Benchmarks

- show plots of the different AI stages

## Issues and Bugs



## Lessons learned

- benchmarks are extremely important, see numpy -> list
- unit tests are also vital, especially when restructuring (breaking changes)
- when restructuring, keep atomic commits ALWAYS, don't restructure multiple things at once
- performing tests under same-ish conditions
- before commiting for something huge, try to gauge if it will be worth it
  (evaluation and C scripts as well as numpy refactors)

## Future Improvements

I found that I cannot improve the engine much further then
what I have right now.
While it would be possible to restructure the whole backend to use
something like `0x88` or bitboards, that would require an extreme amount
time and effort. Also, it's doubtful that the those changes would
have a huge effect in the end, given that the main bottleneck
will always be python.

Much more interesting would be the refactoring of
the evaluation function. If the evaluation function
would be written entirely in C, then there would be
no overhead when the evaluation function communicates
with the transposition table. This alone would increase
performance by around 10%. Additionally, the performance
boost from switching to pure C would probably give at
least another 10% - 20% boost.

Apart from that, there is not much that can be really
improved for the performance. That is simply because
the legal move generation is just so insanely slow.
For mid game boards it can take a whole millisecond
and the only way to increase the performance there
would be to completely restructure the backend in C.
That is obviously not going to happen.
So instead I would focus my attention on making the
AI stronger by implementing better and more AI
techniques.

## Final remarks

