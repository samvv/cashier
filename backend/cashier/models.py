from datetime import datetime
from decimal import Decimal
from enum import StrEnum, auto
import uuid

import sqlalchemy
from sqlmodel import Relationship, SQLModel, Field, PrimaryKeyConstraint
from pydantic import UUID4

class PricingGroup(SQLModel, table=True):

    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    name: str
    """
    The name of the group as it should be displayed in the interface.
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


class ProductPricingGroup(SQLModel, table=True):

    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    pricing_group: PricingGroup = Field(foreign_key='pricing_group.id')
    """
    The group that may get the discounted price.
    """

    price: Decimal
    """
    The new price of one unit of the product.
    """


class Product(SQLModel, table=True):

    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    name: str
    """
    The name of the item as it will be displayed in the interface.
    """

    base_price: Decimal
    """
    The price of an item when no specific price was found in one of the pricing groups.
    """

    stock: int
    """
    Count of items that can be bought.
    """

    image_path: str | None = None
    """
    A relative path name to the image that represents the product.
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

    order_lines: 'list[OrderLine]' = Relationship(back_populates='product')


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


class WalletType(StrEnum):
    balance = auto()
    external = auto()


class PaymentStatus(StrEnum):
    pending = auto()
    completed = auto()
    confirmed = auto()
    cancelled = auto()


class Payment(SQLModel, table=True):

    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    order_id: UUID4 = Field(foreign_key='order.id')
    """
    Which order was paid with this payment.
    """

    amount: Decimal
    """
    How much needs to pay.
    """

    wallet_type: WalletType
    """
    Did the user pay with their internal balance or something else?
    """

    structured_reference: str | None = None
    """
    An optional string that the user may attach to their payment.
    """

    status: PaymentStatus = Field(default=PaymentStatus.pending)
    """
    The current location in the payment flowchart this payment is in.
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

