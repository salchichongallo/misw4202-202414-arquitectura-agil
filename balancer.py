import os
import subprocess
import requests as http
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

port = 5051
nodes = []
current_node = 0

def next_node():
    global current_node, nodes
    node = nodes[current_node]
    current_node = (current_node + 1) % len(nodes)
    return node if node.available else next_node()

class CallNode:
    def __init__(self, name=None, port=None, available=True):
        self.name = name
        self.port = port
        self.available = available

    def url(self):
        return f'http://localhost:{self.port}/process-call'

def create_node():
    global port
    name = f'node-{port}'
    node = CallNode(name, port, True)
    port += 1
    return node

def start_node(node: CallNode):
    subprocess.Popen(['python', 'management_call.py', str(node.port)])
    next_node()

def release_node(node: CallNode):
    node.available = True

def lock_node(node: CallNode):
    node.available = False

def get_node_by(name):
    global nodes
    for node in nodes:
        if node.name == name:
            return node
    raise Exception(f'Node "{name}" not found')


class CallResource(Resource):
    def post(self):
        node = next_node()
        response = http.post(node.url(), json=request.json)
        return jsonify({ 'node': node.name, 'result': response.json() })


class NodesResource(Resource):
    def post(self):
        node = create_node()
        nodes.append(node)
        start_node(node)
        release_node(node)
        return jsonify({ 'node': node.name })


class SingleNodeResource(Resource):
    def patch(self, nodeName):
        should_release = request.json.get('status')
        node = get_node_by(nodeName)
        if should_release:
            release_node(node)
        else:
            lock_node(node)
        return '', 204


app = Flask(__name__)
api = Api(app)

api.add_resource(CallResource, '/assign-call')
api.add_resource(NodesResource, '/nodes')
api.add_resource(SingleNodeResource, '/nodes/<string:nodeName>')

if __name__ == '__main__':
    app.run(debug=False, port=os.environ.get('PORT', 5001))
