import uuid
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

todo_lists = [
    {'id': '1318d3d1-d979-47e1-a225-dab1751dbe75', 'name': 'Einkaufsliste'},
    {'id': '3062dc25-6b80-4315-bb1d-a7c86b014c65', 'name': 'Arbeit'},
    {'id': '44b02e00-03bc-451d-8d01-0c67ea866fee', 'name': 'Privat'},
]

todos = []

@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PUT'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method Not Allowed'}), 405

@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists), 200

@app.route('/todo-list/<list_id>', methods=['GET'])
def get_list(list_id):
    list_item = next((l for l in todo_lists if l['id'] == list_id), None)
    if not list_item:
        abort(404)
    return jsonify(list_item), 200

@app.route('/todo-list', methods=['POST'])
def add_new_list():
    data = request.get_json()
    if 'name' not in data:
        abort(400)
    new_list = {'id': str(uuid.uuid4()), 'name': data['name']}
    todo_lists.append(new_list)
    return jsonify(new_list), 200

@app.route('/todo-list/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    global todo_lists, todos
    list_item = next((l for l in todo_lists if l['id'] == list_id), None)
    if not list_item:
        abort(404)
    todo_lists = [l for l in todo_lists if l['id'] != list_id]
    todos = [t for t in todos if t['list'] != list_id]
    return jsonify({'msg': 'success'}), 200

@app.route('/todo-list/<list_id>/entries', methods=['GET'])
def get_entries(list_id):
    if not any(l['id'] == list_id for l in todo_lists):
        abort(404)
    return jsonify([t for t in todos if t['list'] == list_id]), 200

@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_entry(list_id):
    if not any(l['id'] == list_id for l in todo_lists):
        abort(404)
    data = request.get_json()
    if 'name' not in data or 'description' not in data:
        abort(400)
    new_entry = {'id': str(uuid.uuid4()), 'name': data['name'], 'description': data['description'], 'list': list_id}
    todos.append(new_entry)
    return jsonify(new_entry), 200

@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT'])
def update_entry(list_id, entry_id):
    entry = next((t for t in todos if t['id'] == entry_id and t['list'] == list_id), None)
    if not entry:
        abort(404)
    data = request.get_json()
    if 'name' not in data or 'description' not in data:
        abort(400)
    entry.update({'name': data['name'], 'description': data['description']})
    return jsonify(entry), 200

