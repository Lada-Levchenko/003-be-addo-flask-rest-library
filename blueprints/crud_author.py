from flask import Blueprint, request, jsonify
from schemas import author_schema
from models import Author

crud_author = Blueprint('crud_author', __name__)


@crud_author.route('', methods=["POST"])
def create():
    author, errors = author_schema.load(request.json)

    if errors:
        return jsonify(errors), 400

    author.save()

    return jsonify(author_schema.dump(author).data), 201


@crud_author.route('', methods=["GET"])
def read():
    authors = list(Author.select())
    return jsonify(author_schema.dump(authors, many=True).data)


@crud_author.route('/<int:id>', methods=["GET"])
def read_one(id):
    try:
        author = Author.get(id=id)
        return jsonify(author_schema.dump(author).data)
    except Author.DoesNotExist:
        return jsonify({"message": "Can't find author with id - `{id}`".format(id=id)}), 404


@crud_author.route('/<int:id>', methods=["PUT"])
def update(id):
    try:
        author = Author.get(id=id)
    except Author.DoesNotExist:
        return jsonify({"message": "Can't find author with id - `{id}`".format(id=id)}), 404

    author, errors = author_schema.load(request.json, instance=author)

    if errors:
        return jsonify(errors), 400

    author.save()

    return jsonify(author_schema.dumps(author).data), 200


@crud_author.route('/<int:id>', methods=["DELETE"])
def delete(id):
    is_author_exists = Author.select().filter(id=id).exists()

    if not is_author_exists:
        return jsonify({"message": "Can't find author with id - `{id}`".format(id=id)}), 404

    Author.delete().where(Author.id == id).execute()
    return jsonify({}), 204
