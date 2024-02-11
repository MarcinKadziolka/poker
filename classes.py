import random


class Card:
    values = {
        2: "Two",
        3: "Three",
        4: "Four",
        5: "Five",
        6: "Six",
        7: "Seven",
        8: "Eight",
        9: "Nine",
        10: "Ten",
        11: "Jack",
        12: "Queen",
        13: "King",
        14: "Ace",
    }
    suits = {
        1: ["Clubs", "♣"],
        2: ["Diamonds", "♦"],
        3: ["Hearts", "♥"],
        4: ["Spades", "♠"],
    }

    def __init__(self, value, suit_val):
        self.value = value
        self.name = self.values[value]
        self.suit_val = suit_val
        self.suit_name = self.suits[suit_val][0]

        if value <= 10:
            self.symbol = str(self.value) + self.suits[suit_val][1]
        else:
            self.symbol = self.name[0] + self.suits[suit_val][1]

    def __repr__(self):
        return self.show()

    def show(self):
        return self.symbol

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.value == other.value and self.suit_val == other.suit_val
        return False

    def __hash__(self):
        return hash((self.value, self.suit_val))

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit_val


class Deck:
    def __init__(self):
        self.available_cards = []
        self.dealt_cards = []
        self.burned_cards = []
        self.build()

    def build(self):
        for i in range(1, 5):
            for j in range(2, 15):
                self.available_cards.append(Card(j, i))

    def shuffle(self):
        return random.shuffle(self.available_cards)

    def deal(self, index=-1):
        card = self.available_cards.pop(index)
        self.dealt_cards.append(card)
        return card

    def burn_card(self):
        self.burned_cards.append(self.available_cards.pop())

    def recollect(self):
        for _ in range(len(self.dealt_cards)):
            self.available_cards.append(self.dealt_cards.pop())
        for _ in range(len(self.burned_cards)):
            self.available_cards.append(self.burned_cards.pop())


class CardHolder:
    def __init__(self):
        self.cards = []

    def draw_card(self, card):
        self.cards.append(card)

    def get_cards(self):
        return self.cards

    def clear_cards(self):
        self.cards = []


class Player(CardHolder):
    def __init__(self, name="Name"):
        super().__init__()
        self.balance = 0
        self.name = name
        self.folded = False
        self.current_round_bet = 0
        self.total_bet = 0
        self.type = "Human"

    def get_name(self):
        return self.name

    def __repr__(self):
        return self.get_name()

    def fold(self):
        self.folded = True
        return True

    # Serves as call and check (check is a call for 0)
    def call(self, pot):
        to_call = pot.get_highest_bet() - self.current_round_bet
        if self.balance <= to_call:
            self.current_round_bet += self.balance
            self.total_bet += self.balance
            pot.balance += self.balance
            self.balance = 0
            print("ALL IN!")
        elif (self.balance - to_call) > 0:
            self.balance -= to_call
            self.current_round_bet += to_call
            self.total_bet += to_call
            pot.balance += to_call
        else:
            print("Not enough credits")
            return False
        return True

    def bet_raise(self, x, pot):
        if self.balance == x:
            if (
                x + self.current_round_bet - pot.get_highest_bet()
                >= pot.get_last_raise()
            ):
                pot.last_raise = (
                    x + self.get_current_round_bet() - pot.get_highest_bet()
                )
            pot.balance += x
            self.balance -= x
            self.current_round_bet += x
            self.total_bet += x
            print("ALL IN!")
        elif (self.balance - x) > 0:
            # Checks if a raise is same or bigger than last raise,
            # i.e. A bets x, B has to bet 2x (call for x and raise for x), C has to bet 4x (call for 2x, raise for 2x)
            # print(f"{x=}, {self.current_round_bet=}, {pot.highest_bet=}, {pot.last_raise=}")
            # print(f"{x + self.current_round_bet - pot.get_highest_bet() >= pot.get_last_raise()=}")
            if (
                x + self.current_round_bet - pot.get_highest_bet()
                >= pot.get_last_raise()
            ):
                pot.last_raise = (
                    x + self.get_current_round_bet() - pot.get_highest_bet()
                )
                pot.balance += x
                self.balance -= x
                self.current_round_bet += x
                self.total_bet += x
            else:
                # print(f"{x=}, {pot.last_raise=}")
                print("Raise must at least the size of the last raise")
                return False
        else:
            print("Not enough credits")
            return False
        return True

    def chips_inflow(self, x):
        self.balance += x

    def get_balance(self):
        return self.balance

    def get_current_round_bet(self):
        return self.current_round_bet

    def get_total_bet(self):
        return self.total_bet

    def has_folded(self):
        return self.folded


class Bot(Player):
    def __init__(self, name="Bot"):
        super().__init__()
        self.name = name
        self.type = "Bot"

    def decision(self, win_prob_prc, break_even_prc, pot, folded_count):
        if win_prob_prc > break_even_prc + 0.1:
            min_raise = pot.last_raise - self.current_round_bet + pot.highest_bet
            if min_raise > self.balance:
                to_raise = self.balance
            elif pot.balance / 4 > min_raise:
                quarter_raise = round(pot.balance / 4)
                third_raise = round(pot.balance / 3)
                half_raise = round(pot.balance / 2)
                three_quarters = round(pot.balance * 0.75)
                pot_raise = pot.balance
                to_raise = random.choices(
                    [
                        min_raise,
                        quarter_raise,
                        third_raise,
                        half_raise,
                        three_quarters,
                        pot_raise,
                    ],
                    weights=(10, 40, 20, 10, 10, 10),
                    k=1,
                )[0]
            else:
                to_raise = min_raise
            if to_raise > self.balance:
                to_raise = self.balance
            self.bet_raise(to_raise, pot)
            print(f"Bot RAISES by {to_raise}, to {self.current_round_bet}")
        elif win_prob_prc >= break_even_prc:
            self.call(pot)
            print(f"Bot CALLS {pot.get_highest_bet() - self.current_round_bet}")
        else:
            print("Bot FOLDS")
            self.fold()
            folded_count += 1

        print()
        input("Press enter to continue")
        print()

        return folded_count


class Pot:
    def __init__(self):
        self.balance = 0
        self.highest_bet = 0
        self.last_raise = 0

    def __repr__(self):
        return "Main pot"

    def set_highest_bet(self, players):
        maximum = 0
        for p in players:
            bet = p.get_current_round_bet()
            if bet > maximum:
                maximum = bet
        self.highest_bet = maximum

    def get_highest_bet(self):
        return self.highest_bet

    def get_balance(self):
        return self.balance

    def get_last_raise(self):
        return self.last_raise
