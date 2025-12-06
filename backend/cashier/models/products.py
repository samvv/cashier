from datetime import datetime
from decimal import Decimal
from pydantic import UUID4
import uuid
import sqlalchemy
from sqlmodel import Field, SQLModel

__all__ = [
    'Product',
]

class Product(SQLModel, table=True):

    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    name: str
    """
    The name of the item as it will be displayed in the interface.
    """

    price: Decimal
    """
    The fixed price of the product.
    """

    stock: int
    """
    Count of items that can be bought.
    """

    image_path: str | None = None
    """
    A relative path name to the image that represents the product.
    """

    ean: str = Field(nullable=False, index=True)
    """
    The offcial EAN code of the product.

    Useful for scanning barcodes.
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

