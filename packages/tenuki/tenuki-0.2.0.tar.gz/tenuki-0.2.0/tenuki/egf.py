from tenuki.rank import Rank, RankLevel


def gor_to_rank(gor: int, is_pro: bool = False) -> Rank:
    if is_pro and gor >= 2685:
        result = ((gor - 15) // 30) - 88
        return Rank(value=min(result, 9), level=RankLevel.PRO)
    if gor < 2050:
        result = -((gor - 50) // 100) + 20
        return Rank(value=result, level=RankLevel.KYU)
    else:
        result = ((gor - 50) // 100) - 19
        return Rank(value=min(result, 9), level=RankLevel.DAN)


def rank_to_gor(rank: Rank) -> int:
    match rank.level:
        case RankLevel.KYU:
            return -((rank.value - 21) * 100)
        case RankLevel.DAN:
            return (rank.value + 20) * 100
        case RankLevel.PRO:
            return (rank.value + 89) * 30
