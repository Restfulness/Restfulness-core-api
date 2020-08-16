from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required
# TodoList
# shows a list of all todos, and lets you POST to add new tasks

parser = reqparse.RequestParser()
parser.add_argument('task')

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

class TodoList(Resource):
    @jwt_required
    def get(self):
        return TODOS

    @jwt_required
    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201
