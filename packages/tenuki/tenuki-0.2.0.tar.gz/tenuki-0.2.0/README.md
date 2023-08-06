# tenuki

A set of development tools for go/baduk/wéiqí projects.

## Installation

Use `pip` or your favorite package manager to install `tenuki`:

```bash
pip install tenuki
```

## Rank

`Rank` class is a representation of a player's rank.

```python
from tenuki.rank import Rank

rank_1 = Rank.parse("1d")
rank_2 = Rank.parse("1k")

assert rank_1 > rank_2
assert rank_1.diff(rank_2) == 1
assert rank_1 + 8 == Rank.parse("9d")
```

### EGF

#### GoR <-> Rank

Convert between GoR and Rank:

```python
from tenuki.rank import Rank
from tenuki.egf import gor_to_rank, rank_to_gor

assert gor_to_rank(2100) == Rank.parse("1d")
assert rank_to_gor(Rank.parse("1d")) == 2100
```
