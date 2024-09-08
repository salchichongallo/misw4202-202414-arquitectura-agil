import os
import subprocess
import requests as http
from flask import Flask, jsonify, request
from flask_restful import Api, Resource


class CallNode:
    def __init__(self, name=None, port=None, available=True):
        self.name = name
        self.port = port
        self.available = available

    def url(self):
        return f'http://localhost:{self.port}/process-call'

    def toJSON(self):
        return {
            'name': self.name,
            'port': self.port,
            'available': self.available,
            'url': self.url(),
        }


class NodesIterator:
    def __init__(self, nodes):
        self.nodes = nodes
        self.current = 0

    def next(self):
        node = self.nodes[self.current]
        self.current = (self.current + 1) % len(self.nodes)
        return node if node.available else self.next()


class NodesFactory:
    def __init__(self):
        self.port = 5051

    def create_node(self):
        name = f'node-{self.port}'
        node = CallNode(name, self.port, available=True)
        self.port += 1
        return node


class NodeService:
    def release(self, node: CallNode):
        script = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'management-call', 'app.py'))
        subprocess.Popen(['python', script, str(node.port)])
        node.available = True

    def lock(self, node: CallNode):
        node.available = False


class Balancer:
    def __init__(self):
        self.nodes = []
        self.iterator = NodesIterator(self.nodes)

    def add(self, node):
        self.nodes.append(node)

    def assign_call(self):
        return self.iterator.next()

    def get_by(self, name):
        for node in self.nodes:
            if node.name == name:
                return node


balancer = Balancer()
factory = NodesFactory()
service = NodeService()


class CallResource(Resource):
    def post(self):
        node = balancer.assign_call()
        response = http.post(node.url(), json=request.json)
        return jsonify({ 'node': node.name, 'result': response.json() })


class NodesResource(Resource):
    def post(self):
        node = factory.create_node()
        service.release(node)
        balancer.add(node)
        return jsonify({ 'node': node.name })

    def get(self):
        return jsonify([node.toJSON() for node in balancer.nodes])


class SingleNodeResource(Resource):
    def patch(self, nodeName):
        should_release = request.json.get('status')
        node = balancer.get_by(nodeName)
        if should_release:
            service.release(node)
        else:
            service.lock(node)
        return '', 204


app = Flask(__name__)
api = Api(app)

api.add_resource(CallResource, '/assign-call')
api.add_resource(NodesResource, '/nodes')
api.add_resource(SingleNodeResource, '/nodes/<string:nodeName>')

if __name__ == '__main__':
    # Start first node
    node = factory.create_node()
    service.release(node)
    balancer.add(node)

    app.run(debug=False, port=5001)
