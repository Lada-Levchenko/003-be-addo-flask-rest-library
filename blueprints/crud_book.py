from flask import Blueprint, request, jsonify
from schemas import book_schema, author_book_schema
from models import Book, AuthorBook, Author

crud_book = Blueprint('crud_book', __name__)


@crud_book.route('', methods=["POST"])
def create():
    book, errors = book_schema.load(request.json)
    if errors:
        return jsonify(errors), 400

    book.save()

    for author in request.json["authors"]:
        if not author_book_schema.validate({
            "book": book.get_id(),
            "author": author
        }):
            AuthorBook.create(book=book, author=Author.get(id=author))
    return jsonify(book_schema.dump(book).data), 201


@crud_book.route('', methods=["GET"])
def read():
    return jsonify(book_schema.dump(list(Book.select()), many=True).data)


@crud_book.route('/<int:id>', methods=["GET"])
def read_one(id):
    try:
        book = Book.get(id=id)
        return jsonify(book_schema.dump(book).data)
    except Book.DoesNotExist:
        return jsonify({"message": "Can't find book with id - `{id}`".format(id=id)}), 404


@crud_book.route('/<int:id>', methods=["PUT"])
def update(id):
    try:
        book = Book.get(id=id)
    except Book.DoesNotExist:
        return jsonify({"message": "Can't find book with id - `{id}`".format(id=id)}), 404

    book, errors = book_schema.load(request.json, instance=book)

    if errors:
        return jsonify(errors), 400

    book.save()

    return jsonify(book_schema.dumps(book).data), 200


@crud_book.route('/<int:id>', methods=["DELETE"])
def delete(id):
    is_book_exists = Book.select().filter(id=id).exists()

    if not is_book_exists:
        return jsonify({"message": "Can't find book with id - `{id}`".format(id=id)}), 404

    AuthorBook.delete().where(AuthorBook.book == id).execute()
    Book.delete().where(Book.id == id).execute()
    return jsonify({}), 204
