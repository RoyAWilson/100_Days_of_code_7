"""Build front end to display/edit data in webpage HTML format

    Returns:
        HTML5: Front end for database of favourite films.
    """
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
    """Set up database as Declarative

    Args:
        DeclarativeBase (_type_): _description_
    """
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///film_collection.db"
db_film = SQLAlchemy(model_class=Base)
db_film.init_app(app)

# CREATE TABLE


class Film(db_film.Model):
    """_summary_

    Args:
        db_film (SQL Database): Set up SQL database to hold film details.

    Returns:
        SQL: Build table
    """
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


class Rate_film_form(FlaskForm):
    """Build form to grab rating and review update/new film

    Args:
        FlaskForm (form)
    """
    rating = StringField("Your Rating out of 10 e.g. 6.5")
    review = StringField("Your Review")
    submit = SubmitField("Submit")


class Add_film(FlaskForm):
    """Build form to obtain new film details

    Args:
        FlaskForm (_type_): Build form
    """
    film_title = StringField("Enter Movie Title:", validators=[DataRequired()])
    submit_butt = SubmitField("Add Movie")


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
    """Render home page of the movie database

    Returns:
        String: HTML Page
    """
    Result = db_film.session.execute(db_film.select(Film))
    all_films = Result.scalars().all()
    return render_template("index.html", films=all_films)


@app.route("/edit", methods=["POST", "GET"])
def edit():
    """Edit rating and review

    Returns:
        _type_: Response | str Update database with new details.
    """
    form = Rate_film_form()
    film_id = request.args.get("id")
    film = db_film.get_or_404(Film, film_id)
    if form.validate_on_submit():
        film.rating = float(form.rating.data)
        film.review = form.review.data
        db_film.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", film=film, form=form)


@app.route("/add", methods=["GET", "POST"])
def add_film():
    """_summary_ Add film to database

    Returns:
        _type_: Film _description_ Film to add to the database
    """
    form = Add_film()
    # TODO: Get film title
    # TODO: Get movie API Key etc.
    # TODO: Pass movie title to API
    # TODO: Get feedback from the movie API and pass to select page get the correct movie details.
    return render_template("add.html", form=form)

# TODO: Add env file for API key import load_env and run it.
#       Add the Secret key to env file even though it was open on
#       the pro-forma download, don't want it showing in the end code.
# TODO: Code the select page to show results of API call
# TODO: Grab details of correct film
# TODO: Write the details to the database
# TODO: Ensure once added redirect to edit page to add further details.


@app.route("/delete")
def delete_film():
    """_summary_ Delete a film from the database

    Returns:
        _type_: None _description_ None
    """
    film_id = request.args.get("id")
    film = db_film.get_or_404(Film, film_id)
    db_film.session.delete(film)
    db_film.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
