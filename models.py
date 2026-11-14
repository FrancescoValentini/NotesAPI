import uuid

from sqlalchemy import String, Text, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class User(Base):
    """Represents a user account and its associated notes."""
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True
    )

    hashed_password: Mapped[str] = mapped_column(String(255))

    notes: Mapped[list["Note"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan"
    )


class Note(Base):
    """Represents a note belonging to a user."""
    __tablename__ = "notes"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id"),
        index=True
    )

    owner: Mapped["User"] = relationship(
        back_populates="notes"
    )