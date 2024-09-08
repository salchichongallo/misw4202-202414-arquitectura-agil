import os
from flask import Flask, jsonify
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


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
