from typing import Any
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, Result, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///film_collection.db"
db_film = SQLAlchemy(model_class=Base)
db_film.init_app(app)

# CREATE TABLE


class Film(db_film.Model):
    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    title: Mapped[str] = mapped_column(
        String(250), nullable=False, unique=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[Float] = mapped_column(Float, nullable=True)
    review: Mapped[str] = mapped_column(
        String(500), nullable=True, unique=True)
    img_url: Mapped[str] = mapped_column(
        String(500), nullable=True, unique=True)

    def __repr__(self) -> str:
        return f'<Film {self.title}>'


with app.app_context():
    db_film.create_all()

# Run twice with different film dets to add a couple of films to the database:

# with app.app_context():
#     new_movie = Film(
#         title='Test Constraints',
#         year='2024',
#         description="Test if problem with constraints been resolved.",
#         rating=7.3,
#         ranking=9,
#         review='Test.',
#         img_url='Test'
#     )
#     db_film.session.add(new_movie)
#     db_film.session.commit()

all_films = []


@app.route("/")
def home():
    Result = db_film.session.execute(db_film.select(Film))
    all_films = Result.scalars().all()
    return render_template("index.html", films=all_films)


if __name__ == '__main__':
    app.run(debug=True)
