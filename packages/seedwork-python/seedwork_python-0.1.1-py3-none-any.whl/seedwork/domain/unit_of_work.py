from abc import ABC, abstractmethod
from traceback import TracebackException
from typing import Optional

from typing_extensions import Self

__all__ = ['AbstractUnitOfWork']


class AbstractUnitOfWork(ABC):
    def commit(self) -> None:
        self._commit()

    def rollback(self) -> None:
        self._rollback()

    @abstractmethod
    def _commit(self) -> None:
        ...

    @abstractmethod
    def _rollback(self) -> None:
        ...

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: TracebackException,
    ) -> None:
        self.rollback()
