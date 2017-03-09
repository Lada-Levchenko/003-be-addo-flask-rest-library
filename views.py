from flask import Flask, request, jsonify
from models import Student, Group, initialize
from schemas import group_schema, student_schema

from flask_cors import CORS

app = Flask(__name__)
CORS(app=app)


@app.route('/api/groups', methods=["POST"])
def create_group():
    group, errors = group_schema.load(request.json)

    if errors:
        return jsonify(errors), 400

    group.save()

    return jsonify(group_schema.dump(group).data), 201


@app.route('/api/groups', methods=["GET"])
def get_groups():
    groups = list(Group.select())
    return jsonify(group_schema.dump(groups, many=True).data)


@app.route('/api/students', methods=["POST"])
def create_student():
    student, errors = student_schema.load(request.json)

    if errors:
        return jsonify(errors), 400

    student.save()

    return jsonify(student_schema.dump(student).data), 201


@app.route('/api/students', methods=["GET"])
def get_students():
    return jsonify(student_schema.dump(list(Student.select()), many=True).data)


@app.route('/api/students/<int:id>', methods=["GET"])
def get_one_student(id):
    try:
        student = Student.get(id=id)
        return jsonify(student_schema.dump(student).data)
    except Student.DoesNotExist:
        return jsonify({"message": "Can't find student with id - `{id}`".format(id=id)}), 404


@app.route('/api/students/<int:id>', methods=["PUT"])
def update_student(id):
    try:
        student = Student.get(id=id)
    except Student.DoesNotExist:
        return jsonify({"message": "Can't find student with id - `{id}`".format(id=id)}), 404

    student, errors = student_schema.load(request.json, instance=student)

    if errors:
        return jsonify(errors), 400

    student.save()

    return jsonify(student_schema.dumps(student).data), 200


@app.route('/api/students/<int:id>', methods=["DELETE"])
def delete_student(id):
    is_user_exists = Student.select().filter(id=id).exists()

    if not is_user_exists:
        return jsonify({"message": "Can't find student with id - `{id}`".format(id=id)}), 404

    Student.delete().where(Student.id == id).execute()
    return jsonify({}), 204


if __name__ == '__main__':
    initialize()
    app.run(use_reloader=True)
