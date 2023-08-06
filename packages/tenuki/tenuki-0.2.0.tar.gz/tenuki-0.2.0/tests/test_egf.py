import pytest

from tenuki.egf import gor_to_rank, rank_to_gor
from tenuki.rank import Rank


@pytest.mark.parametrize(
    "gor, is_pro, expected",
    [
        (2151, False, Rank.parse("2d")),
        (2150, False, Rank.parse("2d")),
        (2149, False, Rank.parse("1d")),
        (2100, False, Rank.parse("1d")),
        (2050, False, Rank.parse("1d")),
        (2049, False, Rank.parse("1k")),
        (2000, False, Rank.parse("1k")),
        (1950, False, Rank.parse("1k")),
        (1949, False, Rank.parse("2k")),
        (-900, False, Rank.parse("30k")),
        (2684, True, Rank.parse("7d")),
        (2685, True, Rank.parse("1p")),
        (2700, True, Rank.parse("1p")),
        (2714, True, Rank.parse("1p")),
        (2715, True, Rank.parse("2p")),
        (2730, True, Rank.parse("2p")),
        (3000, True, Rank.parse("9p")),
    ],
)
def test_gor_to_rank(gor: int, is_pro: bool, expected: Rank) -> None:
    assert gor_to_rank(gor=gor, is_pro=is_pro) == expected


@pytest.mark.parametrize(
    "rank, expected",
    [
        (Rank.parse("1p"), 2700),
        (Rank.parse("1d"), 2100),
        (Rank.parse("1k"), 2000),
        (Rank.parse("30k"), -900),
    ],
)
def test_rank_to_gor(rank: Rank, expected: int) -> None:
    assert rank_to_gor(rank=rank) == expected
