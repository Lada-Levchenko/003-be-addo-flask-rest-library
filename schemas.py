from marshmallow import ValidationError
from marshmallow import fields, validate, validates
from marshmallow_peewee import ModelSchema
from models import Author, Book, AuthorBook
from marshmallow_peewee import Related


class AuthorSchema(ModelSchema):
    first_name = fields.Str(validate=[validate.Length(min=3, max=100)])
    last_name = fields.Str(validate=[validate.Length(min=3, max=100)])

    class Meta:
        model = Author


class BookSchema(ModelSchema):
    name = fields.Str(validate=[validate.Length(min=3, max=100)])
    authors = fields.List(fields.Int)

    class Meta:
        model = Book


class AuthorBookSchema(BookSchema):
    book = Related(nested=BookSchema)
    author = Related(nested=AuthorSchema)

    class Meta:
        model = AuthorBook

    @validates('book')
    def validate_book(self, book):
        if not Book.filter(Book.id == book).exists():
            raise ValidationError("Can't find book")

    @validates('author')
    def validate_author(self, author):
        if not Author.filter(Author.id == author).exists():
            raise ValidationError("Can't find author")


author_schema = AuthorSchema()
book_schema = BookSchema()
author_book_schema = AuthorBookSchema()
