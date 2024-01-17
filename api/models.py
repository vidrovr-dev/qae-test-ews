import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=lambda: uuid.uuid4())
    url: Mapped[str]
    title: Mapped[str]
    filestore_key: Mapped[str] = mapped_column(index=True)


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=lambda: uuid.uuid4())
    video_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("videos.id"), index=True)
    text: Mapped[str]
