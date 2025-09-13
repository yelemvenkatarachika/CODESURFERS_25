from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, DateTime, func

class BaseMixin:
    """
    Base mixin to add common columns like id, created_at, updated_at,
    and automatically generate table names from class names.
    """
    @declared_attr
    def __tablename__(cls):
        # Use the class name in lowercase as table name by default
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Create the declarative base with the mixin class
Base = declarative_base(cls=BaseMixin)
