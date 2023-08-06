from abc import ABC, abstractmethod


class EnvironmentConfig(ABC):
    """Interface for environment configuration."""

    @property
    @abstractmethod
    def n_rows(self) -> int:
        """Returns the number of rows in the environment grid."""

    @property
    @abstractmethod
    def n_cols(self) -> int:
        """Returns the number of columns in the environment grid."""

    @property
    @abstractmethod
    def agent_start_location(self) -> tuple[int, int]:
        """Returns the starting location of the agent in the environment grid."""

    @property
    @abstractmethod
    def propositions(self) -> list[chr]:
        """Return a list of all propositions which may be true in the environment."""

    @property
    @abstractmethod
    def max_observation_counts(self) -> dict[chr, int | None]:
        """Return a dictionary mapping propositions to their maximum observation counts.

        If the maximum observation count is None, the proposition can be observed an
        infinite number of times.
        """

    @property
    @abstractmethod
    def replacement_mapping(self) -> dict[chr, chr]:
        """Return a dictionary mapping propositions to their replacements.

        A proposition is replaced once it has been observed the maximum number of times.
        """

    @property
    @abstractmethod
    def locations(self) -> dict[chr, tuple[int, int]]:
        """Return a dictionary mapping propositions to their locations in the environment grid.

        Each returned tuple indicates proposition location as [row, col].
        """

    @abstractmethod
    def get_proposition_location(self, proposition: chr) -> tuple[int, int]:
        """Return the location of a proposition in the environment grid."""

    @abstractmethod
    def get_proposition_max_observation_count(self, proposition: chr) -> int:
        """Return the maximum number of times a proposition can be observed in the environment.

        After a propostion has been observed the maximum number of times, it will be replaced
        by the proposition defined by the method get_next_proposition(proposition).
        """

    @abstractmethod
    def get_next_proposition(self, proposition: chr) -> chr:
        """Return the proposition which replaces the given proposition.

        A proposition is replaced once it has been observed the maximum number of times.
        """

    def __init__(self) -> None:
        self._validate_replace_mapping()
        self._validate_locations()
        self._validate_observation_counts()

    def _validate_replace_mapping(self) -> None:
        """Validated replacement stragegy.

        Ensure replacement strategy defined for all propositions which may only be observed
        a finite number of times.
        """
        for p in self.max_observation_counts:
            if self.max_observation_counts[p] is not None:
                assert (
                    p in self.replacement_mapping
                ), f"Replacement strategy not defined for proposition {p}, which has a finite max_observation_count."

    def _validate_locations(self) -> None:
        """Validate proposition locations.

        Ensure each position has a most one defined proposition. Propositions which share a
        location are managed through the replacement strategy.
        """
        assert len(set(self.locations.values())) == len(
            self.locations.values()
        ), "Duplicate locations found in initial proposition location strategy."

    def _validate_observation_counts(self) -> None:
        """Validate proposition observation counts.

        Ensure each proposition has a defined maximum observation count.
        """

        print(len(self.max_observation_counts), len(self.propositions))

        assert len(self.max_observation_counts) == len(
            self.propositions
        ), "Missing observation count for proposition."


class DefaultConfig(EnvironmentConfig):
    n_rows = 5
    n_cols = 5
    propositions = ["A", "B", "C", "E"]
    locations = {"A": (1, 1), "B": (0, 4), "C": (4, 0)}
    agent_start_location = (4, 4)
    max_observation_counts = {"A": 1, "B": None, "C": None, "E": None}
    replacement_mapping = {"A": "E"}

    def __init__(self) -> None:
        super().__init__()

    def get_proposition_location(self, proposition: chr) -> tuple[int, int]:
        return self.locations[proposition]

    def get_proposition_max_observation_count(self, proposition: chr) -> int:
        return self.max_observation_counts[proposition]

    def get_next_proposition(self, proposition: chr) -> chr:
        return self.replacement_mapping[proposition]


if __name__ == "__main__":
    DefaultConfig()
