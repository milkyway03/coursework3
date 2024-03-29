from cw.dao.models.base import BaseMixin
from cw.setup_db import db


class Movie(BaseMixin, db.Model):
    __tablename__ = "movies"
    __table_args__ = {'extend_existing': True}

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    trailer = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"), nullable=False)
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("directors.id"), nullable=False)
    director = db.relationship("Director")

    def __repr__(self):
        return f"<Movie '{self.title.title()}'>"
