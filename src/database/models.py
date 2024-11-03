from sqlalchemy import Column, Integer, String, BigInteger
from .base import Base


class Request(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True, index=True)
    telegram_username = Column(String, nullable=False)
    telegram_id = Column(BigInteger, nullable=False)
    username = Column(String, nullable=False)
    description = Column(String, nullable=True)
    subdomain = Column(String, nullable=False)

    def __repr__(self):
        return f"<Request(id={self.id}, username='{self.username}', description='{self.description}', subdomain='{self.subdomain}')>"
