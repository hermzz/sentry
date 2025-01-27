from abc import abstractmethod
from typing import Iterable, NewType

#: Rule to replace high-cardinality patterns in a transaction name.
#: For now, format these rules as simple strings
ReplacementRule = NewType("ReplacementRule", str)


class Clusterer:
    """Strategy for clustering transaction names

    Derives replacement rules from a given set of transaction names.

    """

    @abstractmethod
    def add_input(self, strings: Iterable[str]) -> None:
        """Add a batch of transaction names to the clusterer's state"""
        ...

    @abstractmethod
    def get_rules(self) -> list[ReplacementRule]:
        """Compute and retrieve rules"""
        ...
