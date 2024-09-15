import uuid
from typing import Any, cast

from faker.utils.text import slugify
from sqlalchemy import DECIMAL


def make_slug(oid: uuid.UUID, title: str) -> str:
    return slugify(f"{str(oid)[:13]}-{title}")


def cast_any(obj: Any) -> Any:
    return cast(Any, obj)


Money = DECIMAL(precision=10, scale=2)
