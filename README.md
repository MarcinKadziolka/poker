# Poker Texas Hold'em No Limit

This project is a comprehensive implementation of a Poker Texas Hold'em No Limit game from scratch, including:
- all necessary classes
- a custom hand evaluation system
- hand recognition system
- algorithm that calculates win probabilities using Monte Carlo simulation
- algorithm to evaluate decision effectiveness
- bot that makes optimal mathematical decisions using these algorithms

<img src="https://github.com/MarcinKadziolka/poker/assets/30349386/63ecabde-cf92-49c0-b388-36ef93043e86" width="600" alt="win_gui">

<img src="https://github.com/MarcinKadziolka/poker/assets/30349386/d2ae2c12-7849-431a-af06-98f0c55b7c46" width="600" alt="win_gui">

<img src="https://github.com/MarcinKadziolka/poker/assets/30349386/c0d97b3a-c852-463f-84b5-7078cccf9f47" width="600" alt="against_unknown">


## Implementation
Game is implemented using object-oriented programming with the following classes:
- Player: stores information about chip stack, betting amounts and has methods for acting during the game: fold, check or raise. 
- Bot: inherits Player class extending it by new method: decision. This method makes a decision based on mathematical probabilities.
- Deck: stores cards
- Card: represents card
- Pot: stores information about amount of chips and tracks minimum bet allowed.
- Game: controls flow of the game.

## Custom Scoring System
To evaluate and compare hand strength, an authorial scoring system was developed. This system uses a combination of addition and specifically chosen multipliers to uniquely evaluate each poker hand. Below are the precise formulas for each possible hand in poker:

Let kickers be represented by $k$, and highest card of the hand as $n$:
$$\text{High card} = n \cdot 100000 + k_1 \cdot 1000 + k_2 \cdot 100 + k_3 \cdot 10 + k_4 \cdot 1$$
$$\text{Pair} = \text{pair value} \cdot 100000 + 13 \cdot 100000 + k_1 \cdot 1000 + k_2 \cdot 100 + k_3 \cdot 10$$
$$\text{Two Pair} = \text{pair value}_1 \cdot 100000 + 25 \cdot 100000 + \text{pair value}_2 \cdot 1000 + k_1 \cdot 10$$
$$\text{Three of a kind} = \text{value of the three cards} + 38 \cdot 100000 + k_1 \cdot 100 + k_2 \cdot 10$$
$$\text{Straight} = n \cdot 100000 + 48 \cdot 100000$$
$$\text{Flush} = n \cdot 100000 + 56 \cdot 100000 + k_1 \cdot 10000 + k_2 \cdot 1000 + k_3 \cdot 100 + k_4 \cdot 10$$
$$\text{Full house} = \text{value of the full house} + 82 \cdot 100000 + k_1 \cdot 1000$$
$$\text{Poker} = n \cdot 100000 + 92 \cdot 100000$$


## Poker Win Probability Calculator
The calculator utilizes Monte Carlo simulations to estimate probabilities. This method involves running a large number of random simulations to model the possible outcomes of a game. Here's how it works in the context of this poker calculator:

- Random Sampling: The calculator generates random combinations of common cards and opponent hands to simulate different game scenarios.
- Statistical Accuracy: By running thousands or even millions of these simulations, the calculator can approximate the true probability of winning a hand with high accuracy.
- Efficiency: Instead of analyzing every possible combination exhaustively, Monte Carlo simulation allows for quick probability estimation by focusing on a representative sample of possible outcomes.

### Calculation modes
#### Against Known Cards
Function: Calculates the win probability for specific player hands and common cards.
   
Example: For two players with no common cards, the calculator considers 1,712,304 possible combinations. It samples 50,000 combinations for quick results, achieving 2% accuracy within 5 seconds.

#### Against Unknown Cards
Function: Evaluates probabilities by inputting two known cards and assuming two unknown cards for the opponent.

Example: In a one-on-one game, the opponent's hand can form 1,225 possible combinations. The calculator uses sampling to estimate probabilities efficiently.

#### Against Hand Ranges
Function: Assesses hand strength against a range of potential opponent hands using Bill Chen’s scoring method.
   
Example: Calculate the win probability of a pair of Kings against any hands scored 8 or higher.
