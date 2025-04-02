import uuid
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

todo_lists = [
    {'id': '1318d3d1-d979-47e1-a225-dab1751dbe75', 'name': 'Einkaufsliste'},
    {'id': '3062dc25-6b80-4315-bb1d-a7c86b014c65', 'name': 'Arbeit'},
    {'id': '44b02e00-03bc-451d-8d01-0c67ea866fee', 'name': 'Privat'},
]

todos = []