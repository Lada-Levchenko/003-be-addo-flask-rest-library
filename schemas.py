from marshmallow import ValidationError
from marshmallow import fields, validate, validates
from marshmallow_peewee import ModelSchema
from models import Student, Group
from marshmallow_peewee import Related


class GroupSchema(ModelSchema):
    name = fields.Str(validate=[validate.Length(min=3, max=10)])

    class Meta:
        model = Group


class StudentSchema(ModelSchema):
    name = fields.Str(validate=[validate.Length(min=3, max=10)])

    group = Related(nested=GroupSchema)

    class Meta:
        model = Student

    @validates('group')
    def validate_group(self, value):
        if not Group.filter(Group.id == value).exists():
            raise ValidationError("Can't find group")


group_schema = GroupSchema()
student_schema = StudentSchema()
