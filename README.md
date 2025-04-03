# Todo List API

This is a simple RESTful API built with Flask to manage todo lists and their corresponding tasks. It provides basic operations such as creating, reading, updating, and deleting todo lists and tasks (items).

## Functions

- Create, Read, Update, Delete (CRUD) operations for todo lists
- Create, Read, Update, Delete (CRUD) operations for todo items (tasks)
- CORS enabled for cross-origin requests
- Uses UUID to uniquely identify lists and items

## Endpoints

### Todo Lists

- `GET /todo-lists`

Retrieves all todo lists.
- `GET /todo-list/<list_id>`

Retrieves a specific todo list by its ID.
- `POST /todo-list`

Creates a new todo list.

Request body:

```json
{ "name": "Your list name" }
```

- `DELETE /todo-list/<list_id>`

Deletes a to-do list based on its ID.

### Todo entries

- `GET /todo-list/<list_id>/entries`

Retrieves all entries (tasks) in a specific to-do list.
- `POST /todo-list/<list_id>/entry`

Creates a new to-do entry for a specific list.

Request body:

```json
{
"name": "Task name",
"description": "Task description"
}
```

- `PUT /todo-list/<list_id>/entry/<entry_id>`

Updates an existing to-do entry based on its ID.
- `DELETE /todo-list/<list_id>/entry/<entry_id>`

Deletes a specific todo entry based on its ID.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/CuteeKim/FlaskPyProject.git
```

2. Navigate to the project folder:

```bash
cd FlaskPyProject
```

3. Install the required dependencies:

```bash
pip install -r util/requirements.txt
```

4. Run the Flask application:

```bash
python index.py
```

The server will be started at `http://127.0.0.1:5000`.

## Example Requests (BASH)

### Creating a New To-Do List

```bash
curl -X POST http://localhost:5000/todo-list -H "Content-Type: application/json" -d '{"name": "Einkaufsliste"}'
```

### Adding a To-Do Item to a List

```bash
curl -X POST http://localhost:5000/todo-list/<list_id>/entry -H "Content-Type: application/json" -d '{"name": "Buy Milk", "description": "Buy 2 Liters of Milk"}'
```

### Updating a To-Do Item

```bash
curl -X PUT http://localhost:5000/todo-list/<list_id>/entry/<entry_id> -H "Content-Type: application/json" -d '{"name": "Buy Milk", "description": "Buy 3 liters of milk"}'
```

### Deleting a To-Do Item

```Bash
curl -X DELETE http://localhost:5000/todo-list/<list_id>/entry/<entry_id>
```

### Deleting a To-Do Iist
```Bash
curl -X DELETE http://localhost:5000/todo-list/<list_id>
```

### License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/CuteeKim/FlaskPyProject/blob/main/LICENSE) file for additional details.
