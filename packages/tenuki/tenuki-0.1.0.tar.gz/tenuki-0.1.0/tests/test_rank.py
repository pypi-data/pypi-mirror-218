import pytest

from tenuki.rank import Rank, RankLevel


def test_rank_parse_for_kyu():
    assert Rank.parse("1k") == Rank(value=1, level=RankLevel.KYU)


def test_rank_parse_for_dan():
    assert Rank.parse("1d") == Rank(value=1, level=RankLevel.DAN)


def test_rank_parse_for_pro():
    assert Rank.parse("1p") == Rank(value=1, level=RankLevel.PRO)


def test_rank_parse_when_wrong_input():
    with pytest.raises(ValueError) as e:
        Rank.parse("xyz")

    assert str(e.value) == "Invalid rank: xyz"


def test_rank_parse_when_wrong_value():
    with pytest.raises(ValueError) as e:
        Rank.parse("10d")

    assert str(e.value) == "Invalid rank: 10d"


def test_rank_parse_when_wrong_level():
    with pytest.raises(ValueError) as e:
        Rank.parse("1x")

    assert str(e.value) == "Invalid rank: 1x"


@pytest.mark.parametrize(
    "first_rank, second_rank, expected",
    [
        ("1k", "2k", False),
        ("2k", "1k", True),
        ("1d", "1k", False),
        ("1k", "1d", True),
        ("2d", "1d", False),
        ("1d", "2d", True),
        ("1p", "9d", False),
        ("9d", "1p", True),
        ("2p", "1p", False),
        ("1p", "2p", True),
    ],
)
def test_rank_lower(first_rank: str, second_rank: str, expected: bool):
    assert (Rank.parse(first_rank) < Rank.parse(second_rank)) is expected


def test_rank_str():
    assert str(Rank.parse("1k")) == "1k"
    assert str(Rank.parse("1d")) == "1d"
    assert str(Rank.parse("1p")) == "1p"


@pytest.mark.parametrize(
    "first_rank, second_rank, expected",
    [
        ("9k", "5k", -4),
        ("5k", "9k", 4),
        ("2k", "2d", -3),
        ("2d", "2k", 3),
        ("5d", "9d", -4),
        ("9d", "5d", 4),
        ("8d", "2p", -3),
        ("2p", "8d", 3),
        ("5p", "9p", -4),
        ("9p", "5p", 4),
        ("1k", "1p", -10),
        ("1p", "1k", 10),
    ],
)
def test_rank_diff(first_rank: str, second_rank: str, expected: int):
    assert Rank.parse(first_rank).diff(Rank.parse(second_rank)) == expected


@pytest.mark.parametrize(
    "first_rank, value, expected",
    [
        ("2k", 1, "1k"),
        ("2k", 2, "1d"),
        ("1k", 1, "1d"),
        ("1d", 1, "2d"),
        ("9d", 1, "1p"),
        ("1p", 1, "2p"),
        ("1k", 10, "1p"),
    ],
)
def test_rank_add_int(first_rank: str, value: int, expected: str):
    assert Rank.parse(first_rank) + value == Rank.parse(expected)


@pytest.mark.parametrize(
    "first_rank, value, expected",
    [
        ("2k", 1, "3k"),
        ("1d", 1, "1k"),
        ("2d", 1, "1d"),
        ("1p", 1, "9d"),
        ("2p", 1, "1p"),
        ("1p", 10, "1k"),
    ],
)
def test_rank_subtract_int(first_rank: str, value: int, expected: str):
    assert Rank.parse(first_rank) - value == Rank.parse(expected)
