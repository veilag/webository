from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Request(Base):
    __tablename__ = 'requests'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    telegram_username: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    subdomain: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<Request(id={self.id}, username='{self.username}', description='{self.description}', subdomain='{self.subdomain}')>"
