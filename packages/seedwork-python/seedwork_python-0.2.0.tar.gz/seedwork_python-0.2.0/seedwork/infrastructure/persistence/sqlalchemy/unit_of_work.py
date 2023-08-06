from traceback import TracebackException
from typing import Optional

from sqlalchemy.orm import Session, sessionmaker
from typing_extensions import Self

from seedwork.domain.unit_of_work import AbstractUnitOfWork

__all__ = ['SQLAlchemyUnitOfWork']


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: sessionmaker) -> None:
        self.session_factory: sessionmaker = session_factory

    def _commit(self) -> None:
        self.session.commit()

    def _rollback(self) -> None:
        self.session.rollback()

    def __enter__(self) -> Self:
        self.session: Session = self.session_factory()
        return super().__enter__()

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: TracebackException,
    ) -> None:
        super().__exit__(exc_type, exc_val, exc_tb)
        self.session.close()
