import uuid
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Sample todo lists with unique IDs
todo_lists = [
    {'id': '1318d3d1-d979-47e1-a225-dab1751dbe75', 'name': 'Einkaufsliste'},
    {'id': '3062dc25-6b80-4315-bb1d-a7c86b014c65', 'name': 'Arbeit'},
    {'id': '44b02e00-03bc-451d-8d01-0c67ea866fee', 'name': 'Privat'},
]

# List of todos (tasks) corresponding to the todo lists
todos = []

# Middleware to apply CORS headers for cross-origin requests
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all origins
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PUT'  # Allow these HTTP methods
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Allow the Content-Type header
    return response

# Error handler for Method Not Allowed (405)
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method Not Allowed'}), 405

# Route to get all todo lists
@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists), 200  # Return all todo lists with a 200 OK status

# Route to get a specific todo list by its ID
@app.route('/todo-list/<list_id>', methods=['GET'])
def get_list(list_id):
    # Find the todo list with the given ID
    list_item = next((l for l in todo_lists if l['id'] == list_id), None)
    if not list_item:
        abort(404)  # If the list does not exist, return a 404 Not Found error
    return jsonify(list_item), 200  # Return the todo list with a 200 OK status

# Route to add a new todo list
@app.route('/todo-list', methods=['POST'])
def add_new_list():
    data = request.get_json()  # Get the JSON data from the request
    if 'name' not in data:  # Ensure the name is provided in the request data
        abort(400)  # If not, return a 400 Bad Request error
    new_list = {'id': str(uuid.uuid4()), 'name': data['name']}  # Create a new list with a unique ID
    todo_lists.append(new_list)  # Add the new list to the todo lists
    return jsonify(new_list), 200  # Return the new list with a 200 OK status

# Route to delete a todo list by its ID
@app.route('/todo-list/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    global todo_lists, todos
    # Find the todo list with the given ID
    list_item = next((l for l in todo_lists if l['id'] == list_id), None)
    if not list_item:
        abort(404)  # If the list does not exist, return a 404 Not Found error
    # Remove the list and any associated todos from the todo lists
    todo_lists = [l for l in todo_lists if l['id'] != list_id]
    todos = [t for t in todos if t['list'] != list_id]
    return jsonify({'msg': 'success'}), 200  # Return a success message with a 200 OK status

# Route to get all entries (todos) in a specific todo list
@app.route('/todo-list/<list_id>/entries', methods=['GET'])
def get_entries(list_id):
    # Check if the list exists
    if not any(l['id'] == list_id for l in todo_lists):
        abort(404)  # If not, return a 404 Not Found error
    # Return all todos for the given list ID
    return jsonify([t for t in todos if t['list'] == list_id]), 200

# Route to add a new todo entry to a specific list
@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_entry(list_id):
    # Check if the list exists
    if not any(l['id'] == list_id for l in todo_lists):
        abort(404)  # If not, return a 404 Not Found error
    data = request.get_json()  # Get the JSON data from the request
    if 'name' not in data or 'description' not in data:  # Ensure the name and description are provided
        abort(400)  # If not, return a 400 Bad Request error
    # Create a new todo entry with a unique ID
    new_entry = {'id': str(uuid.uuid4()), 'name': data['name'], 'description': data['description'], 'list': list_id}
    todos.append(new_entry)  # Add the new entry to the todos list
    return jsonify(new_entry), 200  # Return the new entry with a 200 OK status

# Route to update an existing todo entry in a specific list
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT'])
def update_entry(list_id, entry_id):
    # Find the todo entry by its ID and list ID
    entry = next((t for t in todos if t['id'] == entry_id and t['list'] == list_id), None)
    if not entry:
        abort(404)  # If the entry does not exist, return a 404 Not Found error
    data = request.get_json()  # Get the JSON data from the request
    if 'name' not in data or 'description' not in data:  # Ensure the name and description are provided
        abort(400)  # If not, return a 400 Bad Request error
    # Update the entry with the new data
    entry.update({'name': data['name'], 'description': data['description']})
    return jsonify(entry), 200  # Return the updated entry with a 200 OK status

# Route to delete a specific todo entry from a list
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['DELETE'])
def delete_entry(list_id, entry_id):
    global todos
    # Check if the list exists
    if not any(l['id'] == list_id for l in todo_lists):
        abort(404)  # If not, return a 404 Not Found error
    # Find the todo entry by its ID and list ID
    entry = next((t for t in todos if t['id'] == entry_id and t['list'] == list_id), None)
    if not entry:
        abort(404)  # If the entry does not exist, return a 404 Not Found error
    # Remove the entry from the todos list
    todos = [t for t in todos if not (t['id'] == entry_id and t['list'] == list_id)]
    return jsonify({'msg': 'success'}), 200  # Return a success message with a 200 OK status

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
