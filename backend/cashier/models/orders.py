
from datetime import datetime
from decimal import Decimal
from enum import StrEnum, auto
import uuid
from pydantic import UUID4
import sqlalchemy
from sqlmodel import Field, PrimaryKeyConstraint, Relationship, SQLModel

from .products import Product


class OrderLine(SQLModel, table=True):
    __table_args__ = (
        PrimaryKeyConstraint("order_id", "product_id"),
    )
    order_id: UUID4 = Field(foreign_key='order.id')
    product_id: UUID4 = Field(foreign_key='product.id')

    quantity: int
    """
    How many items of the product are being bought.
    """

    unit_price: Decimal
    """
    The calculated price of the product at this particular date and time.
    """

    created_at: datetime | None = Field(
        default=None,
        sa_type=sqlalchemy.DateTime,
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
    )
    """
    Date and time when this order line was registered into the system.
    """

    updated_at: datetime | None = Field(
        default=None,
        sa_type=sqlalchemy.DateTime,
        sa_column_kwargs={"onupdate": sqlalchemy.func.now(), "server_default": sqlalchemy.func.now()},
    )
    """
    Date and time of the most recent change to any of the fields of this order.
    """

    orders: 'list[Order]' = Relationship(back_populates="order_lines")

    product: Product = Relationship(back_populates='order_lines')


class OrderStatus(StrEnum):
    pending_submission = auto()
    pending_payment = auto()
    paid = auto()
    cancelled = auto()


class Order(SQLModel, table=True):

    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    status: OrderStatus = Field(default=OrderStatus.pending_submission)
    """
    What state in the ordering flow the end-user is in now.
    """

    created_at: datetime | None = Field(
        default=None,
        sa_type=sqlalchemy.DateTime,
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
    )
    """
    Date and time when this order was registered into the system.
    """

    updated_at: datetime | None = Field(
        default=None,
        sa_type=sqlalchemy.DateTime,
        sa_column_kwargs={"onupdate": sqlalchemy.func.now(), "server_default": sqlalchemy.func.now()},
    )
    """
    Date and time of the most recent change to any of the fields of this order.
    """

    order_lines: list[OrderLine] = Relationship(back_populates="orders")


