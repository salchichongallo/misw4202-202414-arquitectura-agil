import os
from requests import post
from flask import Flask, request, abort, jsonify


class CallNode:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.calls = 0

    def url(self):
        return f'http://localhost:{self.port}/call'

    def toJSON(self):
        return { 'name': self.name, 'url': self.url() }


class NodeFactory:
    def __init__(self):
        self.initial_port = 5050

    def create(self, name):
        self.initial_port += 1
        return CallNode(name, self.initial_port)


class NodesRepostiory:
    def __init__(self):
        self.nodes = {}

    def add(self, node):
        if node.name in self.nodes:
            raise ValueError('Node already exists')
        self.nodes[node.name] = node

    def list(self):
        return list(self.nodes.values())


app = Flask(__name__)
nodes_factory = NodeFactory()
nodes_repository = NodesRepostiory()

def bad_request(**kwargs):
    response = jsonify(**kwargs)
    response.status_code = 400
    return abort(response)

@app.get('/nodes')
def list_nodes():
    return { 'nodes': [node.toJSON() for node in nodes_repository.list()] }

@app.post('/forward-call')
def forward_call():
    # TODO: Forward call to the next available microservice
    response = post('http://localhost:5002/call', json=request.json)
    return { 'data': response.json(), 'forwarded': True }

@app.post('/nodes')
def register_node():
    name = request.json.get('name')
    if not name:
        return bad_request(message='Name is required')

    try:
        node = nodes_factory.create(name)
        nodes_repository.add(node)
    except ValueError as error:
        return bad_request(message=str(error))

    return node.toJSON()

if __name__ == '__main__':
    app.run(debug=True, port=os.environ.get('PORT', 5001))
