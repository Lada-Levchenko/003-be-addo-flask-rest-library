import peewee as pw

db = pw.SqliteDatabase('database.db')


def initialize():
    Group.create_table(fail_silently=True)
    Student.create_table(fail_silently=True)


class BaseModel(pw.Model):
    class Meta:
        database = db


class Group(BaseModel):
    name = pw.CharField(max_length=100)


class Student(BaseModel):
    first_name = pw.CharField(max_length=100)
    last_name = pw.CharField(max_length=100)
    group = pw.ForeignKeyField(Group)
