import sqlite3
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, Float, String
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# db = sqlite3.connect('books_collection.db')
# cursor = db.cursor()
# # cursor.execute(
# # "CREATE TABLE books(id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)"
# # )
# cursor.execute(
#     "INSERT INTO books VALUES(1, 'Harry Potter', 'J.K. Rowling', '2.1')"
# )
# db.commit()

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


# Create the database:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'

# Now create the extension
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Create table:


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(
        String(250), unique=False, nullable=False)
    rating: Mapped[float] = mapped_column(Float, unique=False, nullable=False)

    # Allow book to be printed by title:

    def __repr__(self) -> str:
        return f'<Book{self.title}>'


# Create the database:
# with app.app_context():
#     db.create_all()

# # Create a record:
# with app.app_context():
#     new_book = Book(id=1, title="Harry Potter",
#                     author='J.K. Rowling', rating=0.25)
#     db.session.add(new_book)
#     db.session.commit()
book_id = 1
with app.app_context():
    update_book = db.session.execute(
        db.select(Book).where(Book.id == book_id)).scalar()
    update_book.title = "Harry Potter and the Goblet of Fire"
    db.session.commit()
