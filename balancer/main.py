import os
from flask import Flask, jsonify
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


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


class CallResource(Resource):
    def post(self):
        return jsonify({ 'foo': 'bar' })


class NodesResource(Resource):
    def post(self):
        return jsonify({ 'node': 'foo' })


class SingleNodeResource(Resource):
    def patch(self, nodeName):
        return '', 204


api.add_resource(CallResource, '/assign-call')
api.add_resource(NodesResource, '/nodes')
api.add_resource(SingleNodeResource, '/nodes/<string:nodeName>')

if __name__ == '__main__':
    app.run(debug=True, port=os.environ.get('PORT', 5001))
