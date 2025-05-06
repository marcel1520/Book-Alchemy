from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.String)
    death_date = db.Column(db.String)

    # meant for users
    def __str__(self):
        return f"Author {self.author_id} with the name {self.name}, born on {self.birth_date}"


    # meant for developers
    def __repr__(self):
        return f"Author_id = {self.author_id} holds (name={self.name}, birth={self.birth_date}, death={self.death_date})"


class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
    publication_year = db.Column(db.Integer)
    isbn = db.Column(db.String)

    author = db.relationship('Author', backref='books')

    # meant for users
    def __str__(self):
        return f"Book {self.book_id} with the title {self.title}, published on {self.publication_year} has isbn: {self.isbn}"

    # meant for developers
    def __repr__(self):
        return f"Book_id = {self.book_id} holds (title={self.title}, isbn={self.isbn}, publication_year={self.publication_year}, foreign_key={self.author_id})"


