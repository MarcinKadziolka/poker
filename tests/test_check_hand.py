from poker.classes import Card
from poker.poker_func import check_hand_7_cards
import itertools

# 2, 3, 6, 8, 9, 10, 14 -> [6, 8, 9, 10, 14]
high_card_14 = [
    Card(14, 2),
    Card(10, 3),
    Card(9, 4),
    Card(8, 1),
    Card(2, 2),
    Card(6, 3),
    Card(3, 4),
]

# 2, 2, 6, 8, 9, 10, 14 -> [9, 10, 14, 2, 2]
pair_2 = [
    Card(14, 2),
    Card(10, 3),
    Card(9, 4),
    Card(8, 1),
    Card(2, 2),
    Card(6, 3),
    Card(2, 4),
]

# 2, 3, 3, 6, 6, 8, 10 -> [10, 3, 3, 6, 6]
two_pair_6_3 = [
    Card(3, 2),
    Card(10, 3),
    Card(3, 4),
    Card(8, 1),
    Card(2, 2),
    Card(6, 3),
    Card(6, 4),
]
# 5, 5, 8, 8, 12, 14, 14 -> [12, 8, 8, 14, 14]
two_pair_with_3_pairs = [
    Card(14, 1),
    Card(14, 4),
    Card(12, 3),
    Card(8, 4),
    Card(8, 1),
    Card(5, 3),
    Card(5, 2),
]

# 2, 3, 4, 6, 9, 9, 9 -> [4, 6, 9, 9, 9]
toak_9 = [
    Card(3, 2),
    Card(9, 3),
    Card(4, 4),
    Card(9, 1),
    Card(2, 2),
    Card(6, 3),
    Card(9, 4),
]

# 2, 3, 4, 5, 6, 9, 10 -> [2, 3, 4, 5, 6]
straight = [
    Card(2, 2),
    Card(9, 3),
    Card(4, 4),
    Card(3, 1),
    Card(10, 2),
    Card(6, 3),
    Card(5, 4),
]

# 2, 3, 4, 5, 10, 14, 14 -> [14, 2, 3, 4, 5]
straight_double_ace = [
    Card(2, 2),
    Card(3, 1),
    Card(5, 2),
    Card(4, 2),
    Card(14, 3),
    Card(10, 1),
    Card(14, 1),
]

# 2, 3, 6, 8, 9, 10, 14 -> [2, 3, 8, 10, 14]
flush = [
    Card(14, 2),
    Card(10, 2),
    Card(9, 4),
    Card(8, 2),
    Card(2, 2),
    Card(6, 3),
    Card(3, 2),
]

# 2, 2, 6, 8, 10, 10, 10 -> [2, 2, 10, 10, 10]
full_house_10_2 = [
    Card(10, 2),
    Card(10, 1),
    Card(9, 4),
    Card(10, 2),
    Card(2, 2),
    Card(6, 3),
    Card(2, 1),
]
# 2, 2, 2, 7, 7, 7, 13 -> [2, 2, 7, 7, 7]
full_house_two_threes = [
    Card(13, 3),
    Card(2, 3),
    Card(7, 3),
    Card(2, 4),
    Card(2, 1),
    Card(7, 4),
    Card(7, 1),
]

# 2, 2, 5, 5, 7, 7, 7-> [5, 5, 7, 7, 7]
full_house_two_pairs = [
    Card(7, 3),
    Card(2, 3),
    Card(7, 3),
    Card(5, 4),
    Card(2, 1),
    Card(7, 4),
    Card(5, 1),
]
# 7605000
# 6, 10, 10, 13, 13, 13, 13 -> [10, 13, 13, 13, 13]
foak_13 = [
    Card(13, 2),
    Card(10, 1),
    Card(13, 4),
    Card(10, 2),
    Card(13, 2),
    Card(6, 3),
    Card(13, 1),
]

# 5, 6, 7, 8, 9, 13, 14 -> [5, 6, 7, 8, 9]
straight_flush = [
    Card(5, 2),
    Card(7, 2),
    Card(8, 2),
    Card(6, 2),
    Card(13, 2),
    Card(9, 2),
    Card(14, 1),
]


class TestCheckHandStraightFlush:
    min_score = 9700000
    max_score = 10600000

    def test_high_card(self):
        score = check_hand_7_cards(high_card_14)
        assert not self.min_score <= score <= self.max_score

    def test_pair(self):
        score = check_hand_7_cards(pair_2)
        assert not self.min_score <= score <= self.max_score

    def test_two_pair(self):
        score = check_hand_7_cards(two_pair_6_3)
        assert not self.min_score <= score <= self.max_score

    def test_toak(self):
        score = check_hand_7_cards(toak_9)
        assert not self.min_score <= score <= self.max_score

    def test_straight(self):
        score = check_hand_7_cards(straight)
        assert not self.min_score <= score <= self.max_score

    def test_flush(self):
        score = check_hand_7_cards(flush)
        assert not self.min_score <= score <= self.max_score

    def test_full_house(self):
        score = check_hand_7_cards(full_house_10_2)
        assert not self.min_score <= score <= self.max_score

    def test_foak(self):
        score = check_hand_7_cards(foak_13)
        assert not self.min_score <= score <= self.max_score

    def test_straight_flush(self):
        permutations = list(itertools.permutations(straight_flush))
        for perm in permutations:
            assert 10100000 == check_hand_7_cards(perm)


class TestCheckHandFourOfAKind:
    min_score = 8400000
    max_score = 9613000

    def test_high_card(self):
        score = check_hand_7_cards(high_card_14)
        assert not (self.min_score <= score <= self.max_score)

    def test_pair(self):
        score = check_hand_7_cards(pair_2)
        assert not (self.min_score <= score <= self.max_score)

    def test_two_pair(self):
        score = check_hand_7_cards(two_pair_6_3)
        assert not (self.min_score <= score <= self.max_score)

    def test_toak(self):
        score = check_hand_7_cards(toak_9)
        assert not (self.min_score <= score <= self.max_score)

    def test_straight(self):
        score = check_hand_7_cards(straight)
        assert not (self.min_score <= score <= self.max_score)

    def test_flush(self):
        score = check_hand_7_cards(flush)
        assert not (self.min_score <= score <= self.max_score)

    def test_full_house(self):
        score = check_hand_7_cards(full_house_10_2)
        assert not (self.min_score <= score <= self.max_score)

    def test_foak(self):
        permutations = list(itertools.permutations(foak_13))
        for perm in permutations:
            assert 9510000 == check_hand_7_cards(perm)

    def test_straight_flush(self):
        score = check_hand_7_cards(straight_flush)
        assert not (self.min_score <= score <= self.max_score)


class TestCheckHandFullHouse:
    min_score = 7103000
    max_score = 8313000

    def test_high_card(self):
        score = check_hand_7_cards(high_card_14)
        assert not (self.min_score <= score <= self.max_score)

    def test_pair(self):
        score = check_hand_7_cards(pair_2)
        assert not (self.min_score <= score <= self.max_score)

    def test_two_pair(self):
        score = check_hand_7_cards(two_pair_6_3)
        assert not (self.min_score <= score <= self.max_score)

    def test_toak(self):
        score = check_hand_7_cards(toak_9)
        assert not (self.min_score <= score <= self.max_score)

    def test_straight(self):
        score = check_hand_7_cards(straight)
        assert not (self.min_score <= score <= self.max_score)

    def test_flush(self):
        score = check_hand_7_cards(flush)
        assert not (self.min_score <= score <= self.max_score)

    def test_full_house(self):
        permutations = list(itertools.permutations(full_house_10_2))
        for perm in permutations:
            assert 7902000 == check_hand_7_cards(perm)

    def test_full_house_two_threes(self):
        permutations = list(itertools.permutations(full_house_two_threes))
        for perm in permutations:
            assert 7602000 == check_hand_7_cards(perm)

    def test_full_house_two_pairs(self):
        permutations = list(itertools.permutations(full_house_two_pairs))
        for perm in permutations:
            assert 7605000 == check_hand_7_cards(perm)

    def test_foak(self):
        score = check_hand_7_cards(foak_13)
        assert not (self.min_score <= score <= self.max_score)

    def test_straight_flush(self):
        score = check_hand_7_cards(straight_flush)
        assert not (self.min_score <= score <= self.max_score)


class TestCheckFlush:
    min_score = 6305432
    max_score = 7014319

    def test_high_card(self):
        score = check_hand_7_cards(high_card_14)
        assert not (self.min_score <= score <= self.max_score)

    def test_pair(self):
        score = check_hand_7_cards(pair_2)
        assert not (self.min_score <= score <= self.max_score)

    def test_two_pair(self):
        score = check_hand_7_cards(two_pair_6_3)
        assert not (self.min_score <= score <= self.max_score)

    def test_toak(self):
        score = check_hand_7_cards(toak_9)
        assert not (self.min_score <= score <= self.max_score)

    def test_straight(self):
        score = check_hand_7_cards(straight)
        assert not (self.min_score <= score <= self.max_score)

    def test_flush(self):
        permutations = list(itertools.permutations(flush))
        for perm in permutations:
            assert 7010832 == check_hand_7_cards(perm)

    def test_full_house(self):
        score = check_hand_7_cards(full_house_10_2)
        assert not (self.min_score <= score <= self.max_score)

    def test_foak(self):
        score = check_hand_7_cards(foak_13)
        assert not (self.min_score <= score <= self.max_score)

    def test_straight_flush(self):
        score = check_hand_7_cards(straight_flush)
        assert not (self.min_score <= score <= self.max_score)


class TestCheckHandStraight:
    min_score = 5300000
    max_score = 6200000

    def test_high_card(self):
        score = check_hand_7_cards(high_card_14)
        assert not (self.min_score <= score <= self.max_score)

    def test_pair(self):
        score = check_hand_7_cards(pair_2)
        assert not (self.min_score <= score <= self.max_score)

    def test_two_pair(self):
        score = check_hand_7_cards(two_pair_6_3)
        assert not (self.min_score <= score <= self.max_score)

    def test_toak(self):
        score = check_hand_7_cards(toak_9)
        assert not (self.min_score <= score <= self.max_score)

    def test_straight(self):
        permutations = list(itertools.permutations(straight))
        for perm in permutations:
            assert 5400000 == check_hand_7_cards(perm)

    def test_straight_Ace(self):
        permutations = list(itertools.permutations(straight_double_ace))
        for perm in permutations:
            assert 5300000 == check_hand_7_cards(perm)

    def test_flush(self):
        score = check_hand_7_cards(flush)
        assert not (self.min_score <= score <= self.max_score)

    def test_full_house(self):
        score = check_hand_7_cards(full_house_10_2)
        assert not (self.min_score <= score <= self.max_score)

    def test_foak(self):
        score = check_hand_7_cards(foak_13)
        assert not (self.min_score <= score <= self.max_score)

    def test_straight_flush(self):
        score = check_hand_7_cards(straight_flush)
        assert not (self.min_score <= score <= self.max_score)


class TestCheckHandThreeOfAKind:
    min_score = 4004300
    max_score = 5214200

    def test_high_card(self):
        score = check_hand_7_cards(high_card_14)
        assert not (self.min_score <= score <= self.max_score)

    def test_pair(self):
        score = check_hand_7_cards(pair_2)
        assert not (self.min_score <= score <= self.max_score)

    def test_two_pair(self):
        score = check_hand_7_cards(two_pair_6_3)
        assert not (self.min_score <= score <= self.max_score)

    def test_toak(self):
        permutations = list(itertools.permutations(toak_9))
        for perm in permutations:
            assert 4706400 == check_hand_7_cards(perm)

    def test_straight(self):
        score = check_hand_7_cards(straight)
        assert not (self.min_score <= score <= self.max_score)

    def test_flush(self):
        score = check_hand_7_cards(flush)
        assert not (self.min_score <= score <= self.max_score)

    def test_full_house(self):
        score = check_hand_7_cards(full_house_10_2)
        assert not (self.min_score <= score <= self.max_score)

    def test_foak(self):
        score = check_hand_7_cards(foak_13)
        assert not (self.min_score <= score <= self.max_score)

    def test_straight_flush(self):
        score = check_hand_7_cards(straight_flush)
        assert not (self.min_score <= score <= self.max_score)


class TestCheckHandTwoPairs:
    min_score = 2802040
    max_score = 3912100

    def test_high_card(self):
        score = check_hand_7_cards(high_card_14)
        assert not (self.min_score <= score <= self.max_score)

    def test_pair(self):
        score = check_hand_7_cards(pair_2)
        assert not (self.min_score <= score <= self.max_score)

    def test_two_pair(self):
        permutations = list(itertools.permutations(two_pair_6_3))
        for perm in permutations:
            assert 3103100 == check_hand_7_cards(perm)

    def test_three_pairs(self):
        permutations = list(itertools.permutations(two_pair_with_3_pairs))
        for perm in permutations:
            assert 3908120 == check_hand_7_cards(perm)

    def test_toak(self):
        score = check_hand_7_cards(toak_9)
        assert not (self.min_score <= score <= self.max_score)

    def test_straight(self):
        score = check_hand_7_cards(straight)
        assert not (self.min_score <= score <= self.max_score)

    def test_flush(self):
        score = check_hand_7_cards(flush)
        assert not (self.min_score <= score <= self.max_score)

    def test_full_house(self):
        score = check_hand_7_cards(full_house_10_2)
        assert not (self.min_score <= score <= self.max_score)

    def test_foak(self):
        score = check_hand_7_cards(foak_13)
        assert not (self.min_score <= score <= self.max_score)

    def test_straight_flush(self):
        score = check_hand_7_cards(straight_flush)
        assert not (self.min_score <= score <= self.max_score)


class TestCheckPair:
    min_score = 1505430
    max_score = 2713200

    def test_high_card(self):
        score = check_hand_7_cards(high_card_14)
        assert not (self.min_score <= score <= self.max_score)

    def test_pair(self):
        permutations = list(itertools.permutations(pair_2))
        for perm in permutations:
            assert 1515090 == check_hand_7_cards(perm)

    def test_two_pair(self):
        score = check_hand_7_cards(two_pair_6_3)
        assert not (self.min_score <= score <= self.max_score)

    def test_toak(self):
        score = check_hand_7_cards(toak_9)
        assert not (self.min_score <= score <= self.max_score)

    def test_straight(self):
        score = check_hand_7_cards(straight)
        assert not (self.min_score <= score <= self.max_score)

    def test_flush(self):
        score = check_hand_7_cards(flush)
        assert not (self.min_score <= score <= self.max_score)

    def test_full_house(self):
        score = check_hand_7_cards(full_house_10_2)
        assert not (self.min_score <= score <= self.max_score)

    def test_foak(self):
        score = check_hand_7_cards(foak_13)
        assert not (self.min_score <= score <= self.max_score)

    def test_straight_flush(self):
        score = check_hand_7_cards(straight_flush)
        assert not (self.min_score <= score <= self.max_score)


class TestCheckHighCard:
    min_score = 705432
    max_score = 1414319

    def test_high_card(self):
        permutations = list(itertools.permutations(high_card_14))
        for perm in permutations:
            assert 1410986 == check_hand_7_cards(perm)

    def test_pair(self):
        score = check_hand_7_cards(pair_2)
        assert not (self.min_score <= score <= self.max_score)

    def test_two_pair(self):
        score = check_hand_7_cards(two_pair_6_3)
        assert not (self.min_score <= score <= self.max_score)

    def test_toak(self):
        score = check_hand_7_cards(toak_9)
        assert not (self.min_score <= score <= self.max_score)

    def test_straight(self):
        score = check_hand_7_cards(straight)
        assert not (self.min_score <= score <= self.max_score)

    def test_flush(self):
        score = check_hand_7_cards(flush)
        assert not (self.min_score <= score <= self.max_score)

    def test_full_house(self):
        score = check_hand_7_cards(full_house_10_2)
        assert not (self.min_score <= score <= self.max_score)

    def test_foak(self):
        score = check_hand_7_cards(foak_13)
        assert not (self.min_score <= score <= self.max_score)

    def test_straight_flush(self):
        score = check_hand_7_cards(straight_flush)
        assert not (self.min_score <= score <= self.max_score)
