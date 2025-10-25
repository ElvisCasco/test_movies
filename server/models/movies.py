from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from server.database import Base

class MovieModel(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genres = relationship("GenreModel", back_populates="movie")

class GenreModel(Base):
    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True, index=True)
    genre_name = Column(String, index=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id"))
    movie = relationship("MovieModel", back_populates="genres")