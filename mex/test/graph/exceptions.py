from collections.abc import Sequence
from typing import Any

from pydantic_core import ErrorDetails

from mex.test.exceptions import testError


class NoResultFoundError(testError):
    """A database result was required but none was found."""


class MultipleResultsFoundError(testError):
    """A single database result was required but more than one were found."""


class InconsistentGraphError(testError):
    """Exception raised for inconsistencies found in the graph database."""


class IngestionError(testError):
    """Error for ingestion failures with underlying details."""

    def __init__(
        self,
        *args: Any,  # noqa: ANN401
        errors: Sequence[ErrorDetails] = (),
        retryable: bool = False,
    ) -> None:
        """Construct a new ingestion failure with underlying details."""
        super().__init__(*args)
        self._errors = list(errors)
        self._retryable = retryable

    def errors(self) -> list[ErrorDetails]:
        """Details about underlying errors."""
        return self._errors

    def is_retryable(self) -> bool:
        """Whether the error is retryable."""
        return self._retryable
