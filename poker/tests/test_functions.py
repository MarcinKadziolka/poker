from poker.poker_func import Card
from poker import poker_func
import pytest


@pytest.mark.parametrize(
    "hole_cards, score",
    [
        ((Card(14, 1), Card(14, 2)), 20),
        ((Card(14, 1), Card(13, 1)), 12),
        ((Card(10, 3), Card(10, 4)), 10),
        ((Card(5, 2), Card(7, 2)), 6),
        ((Card(2, 2), Card(2, 3)), 5),
        ((Card(8, 2), Card(10, 2)), 7),
        ((Card(8, 2), Card(10, 3)), 5),
        ((Card(8, 2), Card(8, 3)), 8),
        ((Card(13, 2), Card(2, 3)), 3),
        ((Card(13, 2), Card(12, 3)), 8),
        ((Card(13, 2), Card(11, 3)), 7),
        ((Card(13, 2), Card(11, 2)), 9),
    ],
)
def test_chen_formula(hole_cards, score):
    assert poker_func.chen_formula(hole_cards) == score


@pytest.mark.parametrize(
    "string, expected",
    [
        ("As Ks", [Card(14, 4), Card(13, 4)]),
        (
            "As Ks Qs Js Ts",
            [Card(14, 4), Card(13, 4), Card(12, 4), Card(11, 4), Card(10, 4)],
        ),
        ("2h, Qs, 7d, 6c", [Card(2, 3), Card(12, 4), Card(7, 2), Card(6, 1)]),
        (
            "2h, Qs, 7d, 6c, 5c",
            [Card(2, 3), Card(12, 4), Card(7, 2), Card(6, 1), Card(5, 1)],
        ),
    ],
)
def test_parse_cards(string, expected):
    assert poker_func.parse_cards(string) == expected
