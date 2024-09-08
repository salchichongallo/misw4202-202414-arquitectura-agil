import os
from flask import Flask, jsonify
from flask_restful import Api, Resource


class CallNode:
    def __init__(self, name=None, port=None, available=True):
        self.name = name
        self.port = port
        self.available = available

    def url(self):
        return f'http://localhost:{self.port}/process-call'


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
        # TODO: Start server via CLI on the node's port
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


balancer = Balancer()
factory = NodesFactory()
service = NodeService()


class CallResource(Resource):
    def post(self):
        return jsonify({ 'foo': 'bar' })


class NodesResource(Resource):
    def post(self):
        return jsonify({ 'node': 'foo' })


class SingleNodeResource(Resource):
    def patch(self, nodeName):
        return '', 204


app = Flask(__name__)
api = Api(app)

api.add_resource(CallResource, '/assign-call')
api.add_resource(NodesResource, '/nodes')
api.add_resource(SingleNodeResource, '/nodes/<string:nodeName>')

if __name__ == '__main__':
    app.run(debug=True, port=os.environ.get('PORT', 5001))
