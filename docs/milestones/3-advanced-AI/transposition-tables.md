When I tried to implement the transposition tables
I stumbled across many issues. Mainly having way
too many collisions in the hash table.

## The Problem

There are far too many collisions in the hash table to
reasonably implement this into the AI.
Roughly, for 10k boards that were hashed there were
around 20 collisions. If you didn't wipe the table
after each ply, then the number of collisions would
skyrocket after that, to the point were searching
50k boards resulted in 25k collisions, so 50%.
Any type of collision handling would be more then
futile here.

I was also able to observe that the AI was playing
extremely bad (basically random moves) when the
number of collisions was high, which means that
it's unlikely that there was an issue with the
debugging of the collisions.

## Theory and Birthday Paradox

It goes without saying that something must be
going wrong here, though if we consider the
[birthday paradox](https://en.wikipedia.org/wiki/Birthday_problem),
then it doesn't seem so bizarre actually.
Using the rule of thumb of `p ~= n^2 / 2 * m` with
the probability of collisions `p`,
the number of boards hashed `n` and the amount
of entries in the board `m`, we get the following:

```
m = 2^24
p = 1 / 2
n = sqrt(2^24) = 2^12
```

so if we hash `2^12 = 4096` boards we should expect
that there will be at least one collision with
a chance of 50%.
So collisions with the number of boards we hashed are
actually extremely likely, and given that they grow
exponentially, it's not too surprising to find
these huge numbers of collisions. Though there is
still likely a bug in my implementation.

## Trying to Solve the Problem

I tried these things to solve the problem,
however none of them fixed it:

- Generate zobrist keys through a random seed and
  test different seeds
- Write unit tests to see how many collisions appear
  on depth 3 alone (roughly 3k)
- Differentiate between index collisions and hash
  collisions, were index collisions mean different
  hashes map to the same index because of `%`,
  and hash collisions simple mean different boards
  hash to the same value. Hash collisions are by
  far the more common collision type
- Make sure that the castling rights also get hashed
- Use 64 bit zobrist hashkeys instead of 32 bit

I was very confused when I first saw that the hash
collisions are the much more common type of collision.
It seems like the hash function isn't all that great,
but I don't really know how to make that any better,
or why it would be bad in the first place.

## Lessons learned

To begin with, given that I am using python,
transposition tables wouldn't be that great anyways.
We can't get much deeper then depth 4, so the effect
they would have would be pretty small anyways.
Despite that, I still wanted to implement them
because I didn't use hash tables before.
My big take away is to avoid using hash tables
if at all possible. Designing a good hash
function is not at all trivial and managing
collisions, either through channing or open addressing
is also something that has to be carefully choosen.

I did try to implement them in C so that was a good
learning experience. It's also quite fascinating that
you can call into C from Python in less then
3 microseconds (using the
[cffi package](https://pypi.org/project/cffi/)).
The whole evaluation function could actually be rewritten
in C. That could boost the performance by perhaps 25%.

I also discovered a bug that is pretty sever.
The current move ordering is actually evaluating
every single board. This is obviously extremely dumb,
especially when you try to compare minimax and alpha-beta
and don't really see much of a difference (this is
the reason why the cutoff effect didn't seem that
effective in [milestone II](../2-basic-AI/README.md)
the amount of cutoffs in depth 3 is actually a perfect
cutoff and it also explains why the total time for
the best move generation is so high).

Overall I learned a lot, however I did cost me a lot
of time as well, with little to nothing to show for now.
Perhaps I will come back to the transposistion tables
in a later stage, but I doubt it.
