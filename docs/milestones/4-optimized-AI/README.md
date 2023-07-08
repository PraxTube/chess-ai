# <center>Milestone IV - Optimized AI</center>

## <center>Group C - The Plebs</center>

A chess AI written in Python.

## Summary

In this milestone we primairly focused on the AI improvements
in both strength and speed.

We managed to make the AI both stronger and faster by implementing
the following changes:

- Various evaluation function improvements
- PVS/negamax
- Nullsearch
- MCTS

## AI

### Evaluation

We improved the evaluation function to include the following features

- Check if it's late game, if so, use different PeSTO table
- Evaluate King danger
- Punish bad pawn structure (isolated, backward, not right aligned)
- Pigs on the 7th rank (rooks on 7th rank)

While the above additions make the evaluation slower overall, we think
that it was a good trade-off for a stronger AI.
Fine tuning a few hyperparameters (through research and
trial and error) also helped to increase the strength without any trade-offs.
We also tried to implement mobility evaluation, however in our case
it was just way too slow so we removed it. Also, checking if two bishops
are present was too slow (compared to the benefit it provided).

The reason some features worked well and others didn't
was mainly a question about can we vectorize it properly with numpy.
Features that required calcuations that could be cleverly put into
one single numpy call worked the best. On the other, features that only required
checks with loops over the board were simply to slow compared to the rest.

### PVS/Negamax

PVS (Principal Variation Search) combined with negamax is an efficient algorithm for searching the game tree and evaluating the best moves. The primary challenge we encountered was understanding the intricacies of the algorithm. Ensuring the correctness and efficiency of our PVS/negamax implementation demanded careful debugging and testing. However, with thorough research and trail and error, we were able to overcome these challenges successfully (although it seems like there might still be some issues, it works fairly decent in most cases).
We also had some problems when implementing this feature in our code base simply because the AI framework was pretty bad.
While we did refactor the chess backend in the previous milestone, we didn't do the same for the AI (though to be fair, the AI is much less complex). So we also restructured the AI framework (partially) with the features we implemented in this milestone.

### Nullsearch

Implementing nullsearch involved modifying our search algorithm to skip certain moves and evaluate the position based on the assumption of no move being made. The main challenge here was determining when and where to apply null moves and ensuring that the search results remained accurate. Tuning the nullmove heuristic and fine-tuning the implementation took some time, but we managed to integrate nullsearch into our AI effectively.
This was probably the easiest feature we implemented in this milestone. It was a decent boost in the performance for fairly little work, so overall probably the best ROI (Return of Investment) in this milestone.

### MCTS

The challenges we faced with the MCTS implementation were mainly related to the design and structure of the search tree. Coding up the algorithm was actually not too hard, especially because some members of the team already covered MCTS both in theary and in practice in a separate course. This actually allowed us to implement it fairly fast without any major hiccups. The main challange here was to balance exploration and exploitation effectively to improve the AI's decision-making. The complexity of MCTS required us to carefully manage the tree's expansion, simulation, and backpropagation phases. Additionally, tuning the exploration parameter and the number of simulations proved to be crucial for achieving good performance. Though given that we were already quite familiar with MCTS we managed to overcome this challange and integrate MCTS successfully into our AI.

## Benchmarks

The plots illustrate how the changes to the AI effect the performance.
We can see that only the evaluation and the best move generation are influenced by the changes
(which makes sense of course, given that we didn't change anything in the backend).

The increase in evaluation is fairly high, however we do get a lot of value out of that trade-off.
We also exeprimented with worse evaluation and faster speed and also the reverse and ultimately landed
somewhere inbetween. The best move generation went down overall because of all the different AI
features we implemented, which is actually a very good sign because the evaluation time increase.

In figure 2 we can see that the amount of nodes we search has decreased and that the overall time
has also decreased compared to the previous AI version.

The tests were run on a PC with the following specs

- CPU: Intel i5-4590, Threads: 4, Cores: 4, 3.7GHz

- RAM: 24GB DDR3

- OS: Zorin 16.2 (Ubuntu based)

<p align="center">
    <img src="plot.svg" alt="Plot SVG Image">
    <br>
    Figure 1: Benchmarks of the different categories across the AI versions.
</p>

<p align="center">
    <img src="plot-depths.svg" alt="Plot Depths SVG Image">
    <br>
    Figure 2: Benchmarks of different AI versions in respect to search depth.
    <br>
    Note that the number of nodes searched is in thousands (kilo).
</p>

## Lessons learned

We were able to implement most of the things we planned to do without any major issues.
Primairly because we leveraged the knowledge and learned from previous mistakes.
For instance we didn't commit to anything before we knew it would yield results.
We tested very regularly the performance to see if we are going in the right direction.
Atomic commits kept the history clean and allowed for better and easier teamwork.

## Final remarks

This was the final milestone in which we managed to wrap up the project
fairly nicely. That being said, there are still a number of possible
improvements that can be made. Perhaps we will continue this project
as a hobby at some point, though not in the near future.

At times this project was a lot. Bugs kept creeping up everywhere.
The teamwork didn't work out to well in the beginning.
However we managed to overcome these issues and learn from them.
Overall it has been a very teaching and most importantly a fun project.
