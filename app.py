import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book


app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'library.sqlite')


app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.secret_key = 'my_key_123'


db.init_app(app)


@app.route("/")
def home():
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort_by', 'title')
    valid_columns = {
        'title': Book.title,
        'publication_year': Book.publication_year,
        'author': Author.name
    }
    if sort_by not in valid_columns:
        sort_by = 'title'

    query = db.session.query(Book).join(Author)

    if search_query:
        query = query.filter(Book.title.ilike(f'%{search_query}%'))

    books = query.order_by(valid_columns[sort_by]).all()

    return render_template("home.html", books=books, sort_by=sort_by)


@app.route("/add_author", methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form.get('name')
        birth_date = request.form.get('birth_date')
        death_date = request.form.get('death_date') or None

        new_author = Author(name=name, birth_date=birth_date, death_date=death_date)
        db.session.add(new_author)
        db.session.commit()

        flash(f"Author '{name}' added successfully!", "success")
        return redirect(url_for('add_author'))

    return render_template("add_author.html")


@app.route("/add_book", methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author_id = request.form.get('author_id')
        publication_year = request.form.get('publication_year')
        isbn = request.form.get('isbn')

        new_book = Book(title=title, author_id=author_id, publication_year=publication_year, isbn=isbn)
        db.session.add(new_book)
        db.session.commit()

        flash(f"title {title} added successfully", 'success')
        return redirect(url_for('add_book'))

    authors = Author.query.all()
    return render_template("add_book.html", authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        flash(f"Book '{book.title}' deleted successfully", 'success')
    else:
        flash("Book not found.", 'error')
    return redirect(url_for('home'))

if __name__ == "__main__":

    """with app.app_context():
        db.create_all()"""

    app.run(debug=True)