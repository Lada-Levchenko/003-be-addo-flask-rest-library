import peewee as pw

db = pw.SqliteDatabase('database.db')


def initialize():
    Author.create_table(fail_silently=True)
    Book.create_table(fail_silently=True)
    AuthorBook.create_table(fail_silently=True)


class BaseModel(pw.Model):

    class Meta:
        database = db


class Author(BaseModel):
    first_name = pw.CharField(max_length=100)
    last_name = pw.CharField(max_length=100)

    def get_id(self):
        return self.id


class Book(BaseModel):
    name = pw.CharField(max_length=100)

    def get_id(self):
        return self.id


class AuthorBook(BaseModel):
    author = pw.ForeignKeyField(Author)
    book = pw.ForeignKeyField(Book)






