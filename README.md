# Poker Texas Hold'em No Limit

This project is a comprehensive implementation of a poker card game, including all necessary classes, a custom hand evaluation system, and a hand recognition system. It features an algorithm that calculates win probabilities in three modes: against known cards, unknown cards, and hand ranges. Additionally, it includes an algorithm to evaluate decision effectiveness and an AI that makes optimal mathematical decisions using these algorithms. The game allows for play against the AI, providing a challenging and educational poker experience.



# Game introduction
Poker Texas Hold'em No Limit is the most popular variant of poker, requiring a minimum of two players and typically up to ten. 
It uses a standard deck of 52 cards, featuring ranks 2 through 10, Jack, Queen, King, and Ace in four suits: clubs, hearts, diamonds, and spades. 
The suits have equal value. The Jack, Queen, and King are valued as 11, 12, and 13, respectively, and the Ace can be worth either 1 or 14.

## Gameplay

Players compete to form the best hand while betting against each other over four stages. In no limit, bets are only restricted by players' chip counts. Community cards are dealt face up and can be used by all players. In each betting round, players can:

  - Fold: Forfeit their cards and exit the round.
  - Call: Match the current highest bet.
  - Raise: Increase the current bet.

### Turn Order

A white button marks the dealer's position, moving one spot left each round. This ensures all players experience different positions relative to the dealer. Action moves clockwise, starting from the first player left of the dealer.
#### First Round (Pre-flop)

Before play begins, the two players left of the dealer post blinds: the small blind and the big blind. Each player then receives two private cards, and the first betting round starts.
#### Second Round (Flop)

Three community cards are dealt face up, followed by the second betting round.
#### Third Round (Turn)

A fourth community card is dealt face up, followed by the third betting round.
#### Fourth Round (River)

A fifth community card is dealt face up, followed by the final betting round. If multiple players remain, a showdown occurs, and the player with the best hand wins the pot. If all but one player fold, the remaining player wins without revealing their cards.



Poker Win Probability Calculator

This section describes the implementation of a calculator that computes win probabilities in poker using game simulation. The calculator offers three modes: against known cards, unknown cards, and hand ranges.
Calculation Modes
Against Known Cards

Calculates win probability for up to six known player hands and community cards. Simulates up to 50,000 random tables for accuracy within 2 percentage points and executes in under 5 seconds.

Example:

    Player 1: AA
    Player 2: KK
    Community Cards: None

Simulation results for two players with various community cards are shown in Table 1.

Table 1: Combinations of Missing Cards Based on Game State
Community Cards	Available Cards	Missing Cards	Combinations
0	48	5	1,712,304
1	47	4	178,365
2	46	3	15,180
3	45	2	990
4	44	1	44
5	43	0	1
Against Unknown Cards

Calculates win probability for known player cards against all possible opponent hands. Uses sampling to simulate feasible games based on the number of community cards, ensuring efficient execution.

Example:

    Player: 8♦ 9♦
    Opponent: ??

Results show probabilities similar to a coin toss.
Against Hand Ranges

Evaluates player hand strength against a range of possible opponent hands, typically stronger hands. Uses Bill Chen's method for hand evaluation to create ranges.

Example:

    Player Hand: K♥ K♠
    Opponent Range: Hands ≥ 8 points
    Community Cards: None

Bill Chen's Hand Evaluation Method

    High Card Points:
        A = 10, K = 8, Q = 7, J = 6, 10 or lower = card value.
        Pairs: Score doubled (e.g., AA = 20 points).

    Suited Bonus:
        +2 points if suited.

    Gap Penalty:
        0-1 gap = 0 points
        2 gaps = -1 point
        3 gaps = -2 points
        4 gaps = -4 points
        5+ gaps = -5 points

    Low Card Bonus:
        +1 point if both cards < Q and gap < 3.

Evaluates 1,326 possible hands to determine ranges for the calculator.
