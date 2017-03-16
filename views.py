from flask import Flask, request, jsonify, redirect, url_for
from models import Author, Book, AuthorBook, initialize
from schemas import author_schema, book_schema, author_book_schema
from blueprints.crud_author import crud_author
from blueprints.crud_book import crud_book

from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(crud_author, url_prefix="/api/authors")
app.register_blueprint(crud_book, url_prefix="/api/books")
CORS(app=app)
initialize()


@app.route('/api/authors/<int:id>/books', methods=["GET"])
def get_books_of_author(id):
    books = list(Book.select().join(AuthorBook).join(Author).where(Author.id == id))
    return jsonify(book_schema.dump(books, many=True)), 200


@app.route('/api/books/<int:id>/authors', methods=["GET"])
def get_authors_of_book(id):
    authors = list(Author.select().join(AuthorBook).join(Book).where(Book.id == id))
    return jsonify(author_schema.dump(authors, many=True)), 200

if __name__ == '__main__':
    initialize()
    app.run(use_reloader=True)
