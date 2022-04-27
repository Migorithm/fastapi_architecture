from sqlalchemy import Boolean, Column, Integer, String

from config.database import db

Base = db.get("dev")._base


class FooItem(Base):
    __tablename__ = "foo_items"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    public = Column(Boolean, default=False)