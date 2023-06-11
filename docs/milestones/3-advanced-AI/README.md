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
- Replace `class CastlingRights` with a `list`
- Add guard clauses to reduce indentation and increase readability
- Turn `debug_info` from `dict` to a `class` (in `log.py`)
- Use `list` of `int` for board instead of `str`

For a more detailed description see the
commit history in #37.

The way I restructured the backend was actually
very teaching. At first I wanted to simply write
the whole backend from scratch with the new changes.
However, I quickly realized that this wouldn't really
work. So instead I opted to apply the changes in layers,
where after each change the whole backend should still
be working.

This was extremely effective. It not only allowed me to
assert that the changes I made didn't introduce new bugs,
but also made commiting very clean, and also made sure
that I would be able to track down bugs if they did occur.
So in future projects I will use the same way to restructure
bigger files.

## AI

There were quite a lot of changes regarding the AI.
I mainly tried to implement transposition tables,
however that went horribly wrong.
I wrote a seperate article in which I documented what went wrong,
[see here](./transposition-tables.md).
Apart from that set back, I implemented the following changes:

- Check if given node is terminal node (checkmate/stalemate)
  as opposed to only checking `depth == 0`
- Add a proper king of the hill victory condition (and properly test it)
- Improve time management to be more dynamic (allocate time depending
  on the current stage, early, mid late)
- Refactor move ordering to be much more performant

TODO

## Benchmarks

- show plots of the different AI stages

## Issues and Bugs



## Lessons learned

A collection of lessons that I learned during this milestone

1. Benchmarks are extremely useful to not only see improvements
   over different versions of your code, but also to compare
   incremental changes to the code. I realized this when I tried
   to refactor the evaluation function to use numpy. When I had
   many small `np.ndarray` it was actually slower then the python
   `list` implementation. I noticed that this was because we always
   have overhead when calling numpy, so I should reduce the number
   of times I make a numpy call, i.e. use as big as arrays as possible.
   That I did, and the evaluation function went from `200μs` to `50μs`.
1. On the note of benchmarks, I also observed that background tasks
   can significantly influence the result of benchmarks. One should
   try to run them in same environment (or use a server for that if possible).
1. Sticking to atomic commits when restructuring something big is vital.
   It allows to keep a running system which can be checked to make sure
   no bugs went into the restructure.
1. When I refactored the backend, the unit tests really came in handy.
   After every commit I could just run the tests and see if there
   were any issues.
1. It's important to now if something will be worthwile before commiting
   to it if it will take a long time to complete. I learned this with
   the attempt at implementing transposition tables and when trying to refactor
   the evaluation with numpy arrays. If I would have known
   that the potential performance increase was about `~10%`, I would have
   probably not even tried it in the first place, given how much effort
   went into it. The numpy refactor was luckily successful.
1. Debug hash tables is actually not as straightfoward as it initally
   seemed like.

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

