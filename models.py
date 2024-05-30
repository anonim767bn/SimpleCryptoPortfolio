from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint, Text, DateTime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class Base(DeclarativeBase):
    pass


class UUIDmixin:
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)


class Portfolio(Base, UUIDmixin):
    __tablename__ = 'portfolio'

    name: Mapped[str] = mapped_column(
        Text, nullable=False, unique=True, index=True)
    assets: Mapped['Asset'] = relationship('Asset', back_populates='portfolio')

    __table_args__ = (
        CheckConstraint('LENGTH(name) < 50'),
    )


class Asset(Base, UUIDmixin):
    __tablename__ = 'asset'

    amount: Mapped[float]
    currency_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey('crypto_currency.id'), index=True, nullable=False)
    crypto_currency: Mapped['CryptoCurrency'] = relationship(
        'CryptoCurrency', back_populates='assets')

    portfolio_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey('portfolio.id'), index=True, nullable=False)
    portfolio: Mapped['Portfolio'] = relationship(
        'Portfolio', back_populates='assets')
    __table_args__ = (
        UniqueConstraint('portfolio_id', 'currency_id'),
        CheckConstraint('amount >= 0')
    )


class CryptoCurrency(Base, UUIDmixin):
    __tablename__ = 'crypto_currency'

    name: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    symbol: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    assets: Mapped['Asset'] = relationship(
        'Asset', back_populates='crypto_currency')
    price_histories: Mapped['PriceHistory'] = relationship(
        'PriceHistory', back_populates='crypto_currency')

    __table_args__ = (
        UniqueConstraint('name', 'symbol'),
        CheckConstraint('symbol = upper(symbol)'),
        CheckConstraint('LENGTH(name) < 50'),
    )


class PriceHistory(Base, UUIDmixin):
    __tablename__ = 'price_history'

    crypto_currency_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey('crypto_currency.id'), index=True)
    crypto_currency: Mapped['CryptoCurrency'] = relationship(
        'CryptoCurrency', back_populates='price_histories')
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True, nullable=False)
    price: Mapped[float]

    __table_args__ = (
        UniqueConstraint('crypto_currency_id', 'timestamp'),
        CheckConstraint('price >= 0')
    )
