from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering


class RankLevel(Enum):
    KYU = "k"
    DAN = "d"
    PRO = "p"

    def __lt__(self, other: RankLevel) -> bool:
        order = [RankLevel.KYU, RankLevel.DAN, RankLevel.PRO]
        return order.index(self) < order.index(other)


@total_ordering
@dataclass(frozen=True)
class Rank:
    value: int
    level: RankLevel

    def __str__(self):
        return f"{self.value}{self.level.value}"

    def __post_init__(self):
        if self.value < 1 or (self.level in [RankLevel.DAN, RankLevel.PRO] and self.value > 9):
            raise ValueError(f"Invalid rank: {self.value}{self.level.value}")

    def __lt__(self, other: Rank) -> bool:
        if self.level == other.level:
            if self.level == RankLevel.KYU:
                return self.value > other.value
            else:
                return self.value < other.value
        return self.level < other.level

    def __sub__(self, value: int) -> Rank:
        return Rank._from_int(self._to_int() - value)

    def __add__(self, value: int) -> Rank:
        return Rank._from_int(self._to_int() + value)

    def diff(self, other: Rank) -> int:
        """Returns the difference between two ranks - aka 'stones' difference"""
        return self._to_int() - other._to_int()

    def _to_int(self) -> int:
        match self.level:
            case RankLevel.KYU:
                return -self.value
            case RankLevel.DAN:
                return self.value - 1
            case RankLevel.PRO:
                return self.value + 8

    @staticmethod
    def _from_int(value: int) -> Rank:
        if value < 0:
            return Rank(value=-value, level=RankLevel.KYU)
        elif value < 9:
            return Rank(value=value + 1, level=RankLevel.DAN)
        else:
            return Rank(value=value - 8, level=RankLevel.PRO)

    @staticmethod
    def parse(raw: str) -> Rank:
        """Parses a rank from a string."""
        m = re.match(r"(\d+)\s?([a-z]+)", raw.lower())
        if not m:
            raise ValueError(f"Invalid rank: {raw}")
        value, level = m.groups()
        value = int(value)
        match level:
            case "d" | "dan":
                level = RankLevel.DAN
            case "k" | "kyu":
                level = RankLevel.KYU
            case "p" | "pro":
                level = RankLevel.PRO
            case _:
                raise ValueError(f"Invalid rank: {raw}")
        if (level in [RankLevel.DAN, RankLevel.PRO] and value > 9) or value < 1:
            raise ValueError(f"Invalid rank: {raw}")
        return Rank(value=value, level=level)
