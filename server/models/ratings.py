from datetime import datetime
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    CheckConstraint,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from server.models.get_db import BaseSQLModel
from server.database import Base

if TYPE_CHECKING:
    from server.models.movies import MovieModel
    from server.models.user import UserModel

else:
    MovieModel = "MovieModel"
    UserModel = "UserModel"


#class RatingModel(BaseSQLModel):
#    __tablename__ = "ratings"
#    __table_args__ = (
#        CheckConstraint("rating >= 0.5 AND rating <= 5.0"),
#        UniqueConstraint("user_id", "movie_id"),
#    )

#    rating_id: Mapped[int] = mapped_column(
#        Integer, primary_key=True, autoincrement=True
#    )
#    user_id: Mapped[int] = mapped_column(
#        Integer, ForeignKey("users.user_id"), nullable=False, index=True
#    )
#    movie_id: Mapped[int] = mapped_column(
#        Integer, ForeignKey("movies.movie_id"), nullable=False, index=True
#    )
#    rating: Mapped[float] = mapped_column(Numeric(2, 1), nullable=False)
#    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

#    # Relationships
#    user: Mapped[UserModel] = relationship(back_populates="ratings")
#    movie: Mapped[MovieModel] = relationship(back_populates="ratings")


class RatingModel(Base):
    __tablename__ = "ratings"
    __table_args__ = (
        CheckConstraint("rating >= 0.5 AND rating <= 5.0"),
        UniqueConstraint("user_id", "movie_id"),
    )

    rating_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # keep user_id as plain Integer (no FK to users table to avoid missing users table)
    user_id = Column(Integer, index=True, nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.movie_id"), index=True, nullable=False)
    rating = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relationship to MovieModel (MovieModel should define back_populates="ratings")
    movie = relationship("MovieModel", back_populates="ratings", passive_deletes=True, lazy="joined")