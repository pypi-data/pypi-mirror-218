# tenuki

A set of development tools for go/baduk/wéiqí projects.


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
