from sqlalchemy import Column, Integer, String

from shared.db import Base


class Pizza(Base):
    __tablename__ = "pizza"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)

    def update(self, title: str) -> None:
        self.title = title
