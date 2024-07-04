from itertools import combinations
from collections import Counter
import _pickle as cPickle
import random
import copy
from operator import itemgetter
import math


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

    def __len__(self):
        return len(self.available_cards)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Deck):
            return self.available_cards == other.available_cards
        return False

    def __iter__(self):
        for card in self.available_cards:
            yield card


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
    def __init__(self, chip_stack=1000, name="Name"):
        super().__init__()
        self.chip_stack = chip_stack
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

    def call_amount(self, pot):
        return pot.get_highest_bet() - self.current_round_bet

    # Serves as call and check (check is a call for 0)
    def call(self, pot):
        to_call = self.call_amount(pot)
        if self.chip_stack <= to_call:
            self.current_round_bet += self.chip_stack
            self.total_bet += self.chip_stack
            pot.chip_stack += self.chip_stack
            self.chip_stack = 0
            print("ALL IN!")
        elif (self.chip_stack - to_call) > 0:
            self.chip_stack -= to_call
            self.current_round_bet += to_call
            self.total_bet += to_call
            pot.chip_stack += to_call
        else:
            print("Not enough credits")
            return False
        return True

    def bet_raise(self, x, pot):
        if self.chip_stack == x:
            if (
                x + self.current_round_bet - pot.get_highest_bet()
                >= pot.get_last_raise()
            ):
                pot.last_raise = (
                    x + self.get_current_round_bet() - pot.get_highest_bet()
                )
            pot.chip_stack += x
            self.chip_stack -= x
            self.current_round_bet += x
            self.total_bet += x
            print("ALL IN!")
        elif (self.chip_stack - x) > 0:
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
                pot.chip_stack += x
                self.chip_stack -= x
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

    def add_chips(self, x):
        self.chip_stack += x

    def get_chip_stack(self):
        return self.chip_stack

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
            if min_raise > self.chip_stack:
                to_raise = self.chip_stack
            elif pot.chip_stack / 4 > min_raise:
                quarter_raise = round(pot.chip_stack / 4)
                third_raise = round(pot.chip_stack / 3)
                half_raise = round(pot.chip_stack / 2)
                three_quarters = round(pot.chip_stack * 0.75)
                pot_raise = pot.chip_stack
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
            if to_raise > self.chip_stack:
                to_raise = self.chip_stack
            self.bet_raise(to_raise, pot)
            print(f"Bot RAISES by {to_raise}")
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
    def __init__(self, min_bet=20):
        self.min_bet = min_bet
        self.chip_stack = 0
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

    def get_chip_stack(self):
        return self.chip_stack

    def get_last_raise(self):
        return self.last_raise


# Zwraca listę posortowaną według siły ręki przekazanych graczy
def compare_7_card_hands_showdown(players_list):
    hands_and_scores = []
    for p in players_list:
        #                           0               1               2
        #                       (Michael, [A♣, 7♢, 9♡, K♠, Q♠], 1414297)
        hands_and_scores.append((p, p.cards, check_hand_7_cards(p.cards)))

    sorted_by_score = sorted(
        hands_and_scores, key=lambda tup: tup[2]
    )  # returning list sorted by third item

    return sorted_by_score


# Ocenia siłę ręki zawierającej straight flush
def score_straight_flush(values):
    # A straight flush is a hand that contains five cards of sequential value, all the same suit.
    sorted_values = sorted(values)  # getting sorted values in to the list

    if sorted_values == [
        2,
        3,
        4,
        5,
        14,
    ]:  # because Ace value is 14, we need to check this case (A, 2, 3, 4, 5)
        score = 5 * 100000 + 92 * 100000
    else:
        score = sorted_values[-1] * 100000 + 92 * 100000
    return score


# Ocenia siłę ręki zawierającej flush
def score_flush_7_cards(sorted_values):
    # cdef int
    score = (
        sorted_values[-1] * 100000
        + 56 * 100000
        + sorted_values[-2] * 1000
        + sorted_values[-3] * 100
        + sorted_values[-4] * 10
        + sorted_values[-5] * 1
    )

    return score


def check_straight(sorted_values):
    """
    Znajduje strit:param sorted_values:
    :return: Lista wartości tworzących najwyższy strit uporządkowana malejąco
    """

    """
    Sortuje wartości w porządku malejącym

    Jeśli w wartościach jest As (14), to na koniec listy dodawane jest 1,
    aby wykryć strita [A, 2, 3, 4, 5] == [..., 5, 4, 3, 2, 1]

    Iteruje po wartościach posortowanych malejąco   

    Jeśli indeks + 1 jest równy liczbie wartości w liście, cała lista została przeszukana i nie występuje rosnący ciąg


    Przy każdej iteracji sprawdza, czy liczba o kolejnym indeksie jest o 1 mniejsza, 
    jeśli tak, dodaje jeden do licznika, a daną wartość zapisuje do listy  
    [..., 10, 9, ...] -> if 10 - 1 == 9? -> True -> append(10)

    Jeżeli licznik wynosi 4, oznacza to, że został znaleziony ciąg 5 liczb.
    Do listy dodawana jest ostatnia liczba
    Jeśli w liście znajduje się 1 (As), to jest ona usuwana, a dodawana jest liczba 14
    Zwracana jest lista wartości uporządkowanych rosnąco

    Jeśli liczba o kolejnym indeksie nie jest o 1 mniejsza, sprawdza, czy jest równa obecnej
    (zapobieganie sytuacji, gdy [10, 9, 8, 8, 7, 6, 2])
                                              ^
                                 -4  -3 -2 -1 0

    Gdy jest równa obecnej, przechodzi do następnej iteracji                      

    Jeśli liczba o kolejnym indeksie nie jest większa lub równa obecnej, licznik jest zerowany, a lista czyszczona
    """

    sequence = 0

    straight_sequence = my_deep_copy(sorted_values)

    straight_sequence.reverse()

    to_enumerate_sequence = my_deep_copy(straight_sequence)

    if 14 in straight_sequence:
        to_enumerate_sequence.append(1)

    for i, value in enumerate(to_enumerate_sequence):
        if i + 1 == len(to_enumerate_sequence):
            return None

        if value - 1 == to_enumerate_sequence[i + 1]:
            sequence += 1
            straight_sequence.append(value)

            if sequence == 4:
                straight_sequence.append(value - 1)
                if 1 in straight_sequence:
                    straight_sequence.remove(1)
                    straight_sequence.append(14)
                straight_sequence.sort()
                return straight_sequence
        elif value == to_enumerate_sequence[i + 1]:
            continue
        else:
            sequence = 0
            straight_sequence.clear()


# Ocenia siłę ręki zawierającej strita
def score_straight(sorted_values):
    # cdef int

    if sorted_values == [2, 3, 4, 5, 14]:
        return 5 * 100000 + 48 * 100000

    return sorted_values[-1] * 100000 + 48 * 100000


# Ocenia siłę ręki zawierającej karetę
def score_four_of_a_kind_7_cards(value_count):
    """
    Four of a kind, also known as quads, is a hand that contains four cards of one value and one card of another value
    """
    # cdef int
    quad_value = value_count.most_common(1)[0][0]

    # cdef int

    del value_count[quad_value]
    score = quad_value * 100000 + 82 * 100000 + list(value_count)[-1] * 1000
    return score


# Ocenia siłę ręki zawierającej full house
def score_full_house_7_cards(value_count):
    """
    A full house is a hand that contains three cards of one value and two cards of another value.
    """
    trips_val = 0
    pair_val = 0
    found_pair = 0
    for item in value_count.items():
        if item[1] == 3:
            if item[0] > trips_val:
                if not found_pair:
                    pair_val = trips_val
                trips_val = item[0]
        elif item[1] == 2:
            found_pair = 1
            pair_val = item[0]

    value_count.most_common(2)

    score = trips_val * 100000 + 69 * 100000 + pair_val * 1000

    return score


def check_flush_7_cards(cards):
    """
    :param cards:
    :return: Lista 5 lub więcej kart w danym kolorze w rosnącym porządku / 0
    """
    # A flush is a hand that contains five cards all the same suit, not all of sequential value.
    suits = [card.suit_val for card in cards]
    # Check flush
    suits_counted = Counter(suits)
    # (suit_value, repetitions)
    most_common_suit_tuple = suits_counted.most_common(1)
    if most_common_suit_tuple[0][1] >= 5:
        most_common_suit_value = most_common_suit_tuple[0][0]

        sorted_values = [
            card.value for card in cards if card.suit_val == most_common_suit_value
        ]
        sorted_values.sort()

        return sorted_values
    return 0


# Ocenia siłę ręki zawierającej trójkę
def score_three_of_a_kind_7_cards(value_count):
    """
    Three of a kind is a hand that contains three cards of one value and two cards of another value.
    """

    # cdef int
    trip_value = value_count.most_common(1)[0][0]

    del value_count[trip_value]

    sorted_kickers = list(value_count)

    # cdef int
    score = (
        trip_value * 100000
        + 38 * 100000
        + sorted_kickers[-1] * 1000
        + sorted_kickers[-2] * 100
    )
    return score


# Ocenia siłę ręki zawierającą dwie pary
def score_two_pair_7_cards(value_count):
    #  Two pair is a hand that contains two cards of one value,
    #  two cards of another value and one card of a third value.

    sorted_pairs = []

    items = value_count.items()

    for item in items:
        if item[1] == 2:
            sorted_pairs.append(item[0])

    del value_count[sorted_pairs[-1]]
    del value_count[sorted_pairs[-2]]

    if len(sorted_pairs) == 3:
        del value_count[sorted_pairs[-3]]

    # cdef int
    score = (
        sorted_pairs[-1] * 100000
        + 25 * 100000
        + sorted_pairs[-2] * 1000
        + list(value_count)[-1] * 10
    )

    return score


# Ocenia siłę ręki zawierającą parę
def score_pair_7_cards(sorted_values, value_count):
    # Pair is a hand that contains two cards of one value and three cards of three other values.

    # cdef int
    r = value_count.most_common(1)[0][0]
    # cdef int
    score = r * 100000 + 13 * 100000
    sorted_values.remove(r)
    sorted_values.remove(r)
    score += sorted_values[-1] * 1000 + sorted_values[-2] * 100 + sorted_values[-3] * 10

    return score


# Ocenia siłę ręki, która nie posiada żadnego układu
def score_high_card_7_cards(sorted_values):
    # High card, also known as no pair or simply nothing, is a hand that does not fall into any other category

    # cdef int
    score = (
        sorted_values[-1] * 100000
        + sorted_values[-2] * 1000
        + sorted_values[-3] * 100
        + sorted_values[-4] * 10
        + sorted_values[-5] * 1
    )

    return score


def check_hand_7_cards(cards):
    #  Function checking for all possible rankings in poker, if it finds none, returns ranking for highest card

    sorted_values = [card.value for card in cards]

    sorted_values.sort()

    values_same_suit = check_flush_7_cards(cards)

    # Jeśli minimum 5 kart jest tego samego koloru
    if values_same_suit:
        flush_straight_sequence = check_straight(values_same_suit)

        # Jeśli wśród kart tego samego koloru jest strit
        if flush_straight_sequence:
            # Oceń strit w kolorze
            return score_straight_flush(flush_straight_sequence)
        else:
            # Oceń kolor
            return score_flush_7_cards(values_same_suit)

    straight_sequence = check_straight(sorted_values)

    # Jeśli jest strit
    if straight_sequence:
        # Oceń strit
        return score_straight(straight_sequence)

    # Podliczenie wystąpień danych wartości
    value_count = Counter(sorted_values)

    # Posortowanie rosnąco według liczby powtórzeń
    value_count_values = sorted(value_count.values())

    # Możliwe kombinacje value_count dla high_card = [1, 1, 1, 1, 1, 1, 1]
    if value_count_values == [1, 1, 1, 1, 1, 1, 1]:
        return score_high_card_7_cards(sorted_values)

    # Możliwe kombinacje value_count dla pair: [1, 1, 1, 1, 1, 2]
    if value_count_values == [1, 1, 1, 1, 1, 2]:
        return score_pair_7_cards(sorted_values, value_count)

    # Możliwe kombinacje value_count dla two pair: [1, 1, 1, 2, 2], [1, 2, 2, 2]
    if value_count_values[-1] == 2 and value_count_values[-2] == 2:
        return score_two_pair_7_cards(value_count)

    # Możliwe kombinacje value_count dla toak: [1, 1, 1, 1, 3]
    if value_count_values == [1, 1, 1, 1, 3]:
        return score_three_of_a_kind_7_cards(value_count)

    # Możliwe kombinacje value_count dla full house: [1, 1, 2, 3], [2, 2, 3], [1, 3, 3]
    if value_count_values[-1] == 3 and (
        value_count_values[-2] == 2 or value_count_values[-2] == 3
    ):
        return score_full_house_7_cards(value_count)

    # Możliwe kombinacje value_count dla foak: [1, 1, 1, 4], [1, 2, 4], [3, 4]
    if value_count_values[-1] == 4:
        return score_four_of_a_kind_7_cards(value_count)


def my_deep_copy(obj):
    try:
        return cPickle.loads(cPickle.dumps(obj, -1))
    except cPickle.PicklingError:
        return copy.deepcopy(obj)


# Zwraca listę siły rąk przekazanych graczy
def compare_7_card_hands(hands_7_cards):
    hands_and_scores = []
    for hand in hands_7_cards:
        hands_and_scores.append((hand, check_hand_7_cards(hand)))

    return hands_and_scores


def generate_all_possible_tables(passed_available_cards, num_of_table_cards):
    tuples = combinations(passed_available_cards, 5 - num_of_table_cards)
    generated_tables = [list(x) for x in tuples]
    return generated_tables


def generate_random_num_tables(
    passed_available_cards, num_of_table_cards, number_of_tables
):
    generated_tuples = set()
    for _ in range(number_of_tables):
        generated_tuples.add(
            tuple(random.sample(passed_available_cards, 5 - num_of_table_cards))
        )

    while len(generated_tuples) < number_of_tables:
        generated_tuples.add(
            tuple(random.sample(passed_available_cards, 5 - num_of_table_cards))
        )

    generated_tables = [list(x) for x in generated_tuples]

    return generated_tables


def generate_tables(
    passed_available_cards,
    num_of_table_cards,
    max_number_of_tables=20000,
    choice="automatic",
):
    if choice == "simulation":
        return generate_random_num_tables(
            passed_available_cards, num_of_table_cards, max_number_of_tables
        )
    elif choice == "real":
        return generate_all_possible_tables(passed_available_cards, num_of_table_cards)
    elif choice == "automatic":
        # With 2 players real num of tables is 1 712 304
        if num_of_table_cards == 0:
            return generate_random_num_tables(
                passed_available_cards, num_of_table_cards, max_number_of_tables
            )

        # With 2 players real num of tables is 178 365
        if num_of_table_cards == 1:
            return generate_random_num_tables(
                passed_available_cards, num_of_table_cards, max_number_of_tables
            )

        # With 2 players real num of tables is 15 180
        if num_of_table_cards == 2:
            return generate_all_possible_tables(
                passed_available_cards, num_of_table_cards
            )

        # With 2 players real num of tables is 990
        if num_of_table_cards == 3:
            return generate_all_possible_tables(
                passed_available_cards, num_of_table_cards
            )

        # With 2 players real num of tables is 44
        if num_of_table_cards == 4:
            return generate_all_possible_tables(
                passed_available_cards, num_of_table_cards
            )

        if num_of_table_cards == 5:
            return None


def parse_cards(cards_string):
    # String must be formatted using comas or spaces as such:
    # Ah Ts 8c 8h Kd or Ah, Ts, 8c, 8h, Kd

    # Splitting the string between the spaces
    splitted_cards = cards_string.split()

    # Order is important, as we will use it to find value by index
    names = "23456789TJQKA"
    suits = "cdhs"

    cards = []

    # string.find('some_letter') returns index of passed letter

    for string_card in splitted_cards:
        value = names.find(string_card[0]) + 2
        suit_value = suits.find(string_card[1]) + 1
        cards.append(Card(value, suit_value))

    return cards


def win_probability(
    passed_hands,
    table_cards,
    available_cards,
    max_num_of_simulations=20000,
    choice="automatic",
):
    # start = timeit.default_timer()
    generated_tables = generate_tables(
        available_cards, len(table_cards), max_num_of_simulations, choice
    )

    win_tie_count = [[0.0, 0.0] for _ in range(len(passed_hands))]

    if not generated_tables:
        dc_passed_hands = my_deep_copy(passed_hands)

        for hand in dc_passed_hands:
            hand += table_cards

        hands_and_scores = compare_7_card_hands(dc_passed_hands)

        best_score = max(hands_and_scores, key=itemgetter(1))[1]

        winners = []
        for has in hands_and_scores:
            if has[1] == best_score:
                winners.append(has[1])

        if len(winners) > 1:
            for i, has in enumerate(hands_and_scores):
                if has[1] in winners:
                    win_tie_count[i][1] += 1
        else:
            for i, has in enumerate(hands_and_scores):
                if has[1] in winners:
                    win_tie_count[i][0] += 1

        return win_tie_count, 1

    else:
        amount_of_tables = len(generated_tables)

        for table_c in generated_tables:
            table_c += table_cards
            dc_passed_hands = my_deep_copy(passed_hands)

            for hand in dc_passed_hands:
                hand += table_c

            hands_and_scores = compare_7_card_hands(dc_passed_hands)

            best_score = max(hands_and_scores, key=itemgetter(1))[1]

            winners = []
            for has in hands_and_scores:
                if has[1] == best_score:
                    winners.append(has[1])

            if len(winners) > 1:
                for i, has in enumerate(hands_and_scores):
                    if has[1] in winners:
                        win_tie_count[i][1] += 1
            else:
                for i, has in enumerate(hands_and_scores):
                    if has[1] in winners:
                        win_tie_count[i][0] += 1

        # print(timeit.default_timer() - start)

        return win_tie_count, amount_of_tables


def expected_value(win_prc, to_win, lose_prc, to_lose):
    return (win_prc * to_win) - (lose_prc * to_lose)


def pot_odds_break_even(to_call, pot_chip_stack):
    to_win = to_call + pot_chip_stack
    to_lose = to_call
    if to_lose == 0:
        return 0, 0
    pot_odds = to_win / to_lose
    break_even = 1 / (pot_odds + 1)
    return pot_odds, break_even


def implied_odds(to_call, pot_chip_stack, improve_prc):
    improve_prc /= 100
    # ((1 / Eq) * C) – (P + C)
    return round((1 / improve_prc * to_call) - (pot_chip_stack + to_call))


def generate_all_possible_hole_cards(passed_available_cards):
    combi = combinations(passed_available_cards, 2)
    generated_hole_cards = [list(x) for x in combi]
    return generated_hole_cards


def generate_sample_hol_cards(passed_available_cards, num_of_hands):
    generated_tuples = set()
    for _ in range(num_of_hands):
        generated_tuples.add(tuple(random.sample(passed_available_cards, 2)))

    while len(generated_tuples) < num_of_hands:
        generated_tuples.add(tuple(random.sample(passed_available_cards, 2)))

    generated_hands = [list(x) for x in generated_tuples]

    return generated_hands


def generate_av_cards(hands, table_cards):
    new_deck = []
    not_available_cards = set()

    for i in range(1, 5):
        for j in range(2, 15):
            new_deck.append(Card(j, i))
    for hand in hands:
        for card in hand:
            not_available_cards.add(card)

    if len(table_cards) > 0:
        not_available_cards.update(table_cards)

    for card in not_available_cards:
        new_deck.remove(card)

    return new_deck


def win_probability_against_unknown_cards(
    hero_hand,
    table_cards,
    available_cards,
    num_of_cards_to_generate=100,
    num_of_tables=500,
    choice="automatic",
):
    # Possible hole cards against one player preflop: 1225
    # Possible hole cards against one player one card at the table: 1176
    # Possible hole cards against one player two cards at the table: 1128
    # Possible hole cards against one player three cards: 1081
    # Possible hole cards against one player four: 1035
    # Possible hole cards against one player five: 990
    table_len = len(table_cards)

    sum_of_hero_wins = 0
    sum_of_villain_wins = 0
    sum_of_tables = 0
    sum_of_ties = 0

    if choice == "real":
        villain_hands = generate_all_possible_hole_cards(available_cards)

        for hand in villain_hands:
            av_cards = generate_av_cards([hero_hand + hand], table_cards)

            win_tie_count, amount_of_tables = win_probability(
                [hero_hand] + [hand], table_cards, av_cards, choice="real"
            )

            sum_of_hero_wins += win_tie_count[0][0]
            sum_of_villain_wins += win_tie_count[1][0]
            sum_of_ties += win_tie_count[0][1]
            sum_of_tables += amount_of_tables

    elif choice == "simulation":
        villain_hands = generate_sample_hol_cards(
            available_cards, num_of_cards_to_generate
        )

        for hand in villain_hands:
            av_cards = generate_av_cards([hero_hand + hand], table_cards)

            win_tie_count, amount_of_tables = win_probability(
                [hero_hand] + [hand],
                table_cards,
                av_cards,
                num_of_tables,
                choice="simulation",
            )

            sum_of_hero_wins += win_tie_count[0][0]
            sum_of_villain_wins += win_tie_count[1][0]
            sum_of_ties += win_tie_count[0][1]
            sum_of_tables += amount_of_tables

    elif choice == "automatic":
        if table_len == 0 or table_len == 1 or table_len == 2 or table_len == 3:

            villain_hands = generate_sample_hol_cards(
                available_cards, num_of_cards_to_generate
            )

            for hand in villain_hands:
                av_cards = generate_av_cards([hero_hand + hand], table_cards)

                win_tie_count, amount_of_tables = win_probability(
                    [hero_hand] + [hand],
                    table_cards,
                    av_cards,
                    num_of_tables,
                    "simulation",
                )

                sum_of_hero_wins += win_tie_count[0][0]
                sum_of_villain_wins += win_tie_count[1][0]
                sum_of_ties += win_tie_count[0][1]
                sum_of_tables += amount_of_tables
        else:

            villain_hands = generate_all_possible_hole_cards(available_cards)

            for hand in villain_hands:
                av_cards = generate_av_cards([hero_hand + hand], table_cards)

                win_tie_count, amount_of_tables = win_probability(
                    [hero_hand] + [hand], table_cards, av_cards, choice="real"
                )

                sum_of_hero_wins += win_tie_count[0][0]
                sum_of_villain_wins += win_tie_count[1][0]
                sum_of_ties += win_tie_count[0][1]
                sum_of_tables += amount_of_tables

    return [sum_of_hero_wins, sum_of_villain_wins, sum_of_ties, sum_of_tables]


def chen_formula(hole_cards):
    """
    1. Score your highest card only. Do not add any points for your lower card.
        A = 10 points.
        K = 8 points.
        Q = 7 points.
        J = 6 points.
        10 to 2 = 1/2 of card value. (e.g. a 6 would be worth 3 points)

    2. Multiply pairs by 2 of one card’s value. However, minimum score for a pair is 5.
        (e.g. KK = 16 points, 77 = 7 points, 22 = 5 points)

    3. Add 2 points if cards are suited.

    4. Subtract points if there is a gap between the two cards.
        No gap = -0 points.
        1 card gap = -1 points.
        2 card gap = -2 points.
        3 card gap = -4 points.
        4 card gap or more = -5 points. (Aces are high this step, so hands like A2, A3 etc. have a 4+ gap.)
    5. Add 1 point if there is a 0 or 1 card gap and both cards are lower than a Q. (e.g. JT, 75, 32 etc, this bonus point does not apply to pocket pairs)

    6. Round half point scores up. (e.g. 7.5 rounds up to 8)
    """
    score = 0

    suits = set()
    values = []

    for card in hole_cards:
        suits.add(card.suit_val)
        values.append(card.value)

    max_val = max(values)

    match max_val:
        case 14:
            score += 10
        case 13:
            score += 8
        case 12:
            score += 7
        case 11:
            score += 6
        case _:
            score += max_val / 2

    pair = False
    if values[0] == values[1]:
        score *= 2
        if score < 5:
            score = 5
        pair = True

    if len(suits) == 1:
        score += 2

    gap = abs(values[0] - values[1])
    match gap:
        case 0:
            pass
        case 1:
            pass
        case 2:
            score -= 1
        case 3:
            score -= 2
        case 4:
            score -= 4
        case _:
            score -= 5

    if gap <= 2 and values[0] < 12 and values[1] < 12 and not pair:
        score += 1

    return math.ceil(score)


def win_probability_against_range(
    hero_hand,
    villain_hands,
    table_cards,
    num_of_cards_to_generate=100,
    num_of_tables=500,
    choice="automatic",
):
    table_len = len(table_cards)

    sum_of_hero_wins = 0
    sum_of_villain_wins = 0
    sum_of_tables = 0
    sum_of_ties = 0

    first_hero_card = hero_hand[0]
    second_hero_card = hero_hand[1]

    if choice == "real":
        for hand in villain_hands:
            print(first_hero_card, second_hero_card, hand)
            if first_hero_card in hand:
                continue
            if second_hero_card in hand:
                continue
            if hand[0] in table_cards:
                continue
            if hand[1] in table_cards:
                continue

            av_cards = generate_av_cards([hero_hand + hand], table_cards)

            win_tie_count, amount_of_tables = win_probability(
                [hero_hand] + [hand], table_cards, av_cards, choice="real"
            )

            sum_of_hero_wins += win_tie_count[0][0]
            sum_of_villain_wins += win_tie_count[1][0]
            sum_of_ties += win_tie_count[0][1]
            sum_of_tables += amount_of_tables

    elif choice == "simulation":

        villain_hands_sample = []
        while len(villain_hands_sample) < num_of_cards_to_generate and len(
            villain_hands_sample
        ) < len(villain_hands):
            hand_to_add = random.sample(villain_hands, 1)[0]
            # print(f"{hero_hand[0]=}, {hero_hand[1]=}, {hand_to_add=}")

            if first_hero_card in hand_to_add:
                continue
            if second_hero_card in hand_to_add:
                continue
            if hand_to_add[0] in table_cards:
                continue
            if hand_to_add[1] in table_cards:
                continue

            villain_hands_sample.append(hand_to_add)

        for hand in villain_hands_sample:
            av_cards = generate_av_cards([hero_hand + hand], table_cards)

            win_tie_count, amount_of_tables = win_probability(
                [hero_hand] + [hand],
                table_cards,
                av_cards,
                num_of_tables,
                choice="simulation",
            )

            sum_of_hero_wins += win_tie_count[0][0]
            sum_of_villain_wins += win_tie_count[1][0]
            sum_of_ties += win_tie_count[0][1]
            sum_of_tables += amount_of_tables

    elif choice == "automatic":
        if table_len == 0 or table_len == 1 or table_len == 2 or table_len == 3:

            villain_hands_sample = []
            while len(villain_hands_sample) < 100 and len(villain_hands_sample) < len(
                villain_hands
            ):
                hand_to_add = random.sample(villain_hands, 1)[0]
                # print(f"{hero_hand[0]=}, {hero_hand[1]=}, {hand_to_add=}")

                if first_hero_card in hand_to_add:
                    continue
                if second_hero_card in hand_to_add:
                    continue
                if hand_to_add[0] in table_cards:
                    continue
                if hand_to_add[1] in table_cards:
                    continue

                villain_hands_sample.append(hand_to_add)

            for hand in villain_hands_sample:
                av_cards = generate_av_cards([hero_hand + hand], table_cards)

                win_tie_count, amount_of_tables = win_probability(
                    [hero_hand] + [hand], table_cards, av_cards, 500, "simulation"
                )

                sum_of_hero_wins += win_tie_count[0][0]
                sum_of_villain_wins += win_tie_count[1][0]
                sum_of_ties += win_tie_count[0][1]
                sum_of_tables += amount_of_tables
        else:

            for hand in villain_hands:
                if hand[0] in table_cards:
                    continue
                if hand[1] in table_cards:
                    continue
                av_cards = generate_av_cards([hero_hand + hand], table_cards)

                win_tie_count, amount_of_tables = win_probability(
                    [hero_hand] + [hand], table_cards, av_cards, choice="real"
                )

                sum_of_hero_wins += win_tie_count[0][0]
                sum_of_villain_wins += win_tie_count[1][0]
                sum_of_ties += win_tie_count[0][1]
                sum_of_tables += amount_of_tables

    return [sum_of_hero_wins, sum_of_villain_wins, sum_of_ties, sum_of_tables]


def create_ranges():
    # -1 -> 72o
    # 0  -> 29o, 5To, gap > 4
    # 1  -> 72s, J6o
    # 2  -> Q7o, 46o
    # 3  -> 24s, K7o
    # 4  -> Q2s, 53s, T8o
    # 5  -> K2s, 32s, A2o, A9o
    # 6  -> 55, 56s, 98o, ATo, KTo
    # 7  -> A2s, A3s, A4s, A5s, KJo, QJo, A9s
    # 8  -> 77, 98s, QTs, KTs, AJo, KQo, QTs
    # 9  -> 88, QJs, JTs, KJs, AQo
    # 10 -> 99, AJs, KQs, AKo,
    # 11 -> TT, AQs
    # 12 -> AKs
    # 13 -> JJ
    # 14 -> QQ
    # 16 -> KK
    # 20 -> AA

    av = generate_av_cards([[]], [])

    all_hole_cards = generate_all_possible_hole_cards(av)

    scored_hole_cards = []

    for i, hole_cards in enumerate(all_hole_cards):
        scored_hole_cards.append([])
        scored_hole_cards[i].append(hole_cards)
        scored_hole_cards[i].append(chen_formula(hole_cards))

    ranges = {
        -1: [],
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
        10: [],
        11: [],
        12: [],
        13: [],
        14: [],
        16: [],
        20: [],
    }

    for hole_cards in scored_hole_cards:
        ranges[hole_cards[1]].extend([hole_cards[0]])

    return ranges


all_ranges = create_ranges()

strong_range = (
    all_ranges[8]
    + all_ranges[9]
    + all_ranges[10]
    + all_ranges[11]
    + all_ranges[12]
    + all_ranges[13]
    + all_ranges[14]
    + all_ranges[16]
    + all_ranges[20]
)


""" 
hero = parse_cards("Kh Kd")
table = []


av = generate_av_cards([hero], table)
r = win_probability_against_unknown_cards(hero, table, av)
print()
print("Probability against random cards")
print(f"{hero}, Wins: {r[0]/r[3]*100:.2f}, ties: {r[1]/r[3]*100:.2f}")
print(f"[? ?], Wins: {r[1]/r[3]*100:.2f}, ties: {r[1]/r[3]*100:.2f}")


r = win_probability_against_range(hero, strong_range, table)
print()
print("Probability against range")
print(f"{hero}, Wins: {r[0]/r[3]*100:.2f}, ties: {r[1]/r[3]*100:.2f}")
print(f"Range 8+, Wins: {r[1]/r[3]*100:.2f}, ties: {r[1]/r[3]*100:.2f}")
"""


"""
Możliwe stoły:
0 graczy:
52 karty dostępne, 5 kartowe - 2598960 0 graczy

2 graczy:
48 karty dostępne, 5 kartowe - 1712304
Po flopie, 45 kart, 2 kartowe - 990
Po turnie, 44 karty, 1 kartowe - 44

"""
