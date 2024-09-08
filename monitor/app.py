# from . import create_app
from __init__ import create_app
from flask_restful import Resource, Api
from flask import request, Flask
import requests

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)
active_nodes = {}


class VistaReportStatusNode(Resource):
    def post(self):
        body = request.get_json()
        node_id = body.get('node')
        status = body.get('status')
        if node_id not in active_nodes:
            active_nodes[node_id] = status

        if status != active_nodes[node_id]:
            active_nodes[node_id] = status

        check_active_nodes()
        print(active_nodes)
        return '', 204


def check_active_nodes():
    all_false = all(status == False for status in active_nodes.values())
    if all_false:
        print("All nodes are inactive.")
    else:
        print("Some nodes are still active.")

api.add_resource(VistaReportStatusNode, '/report-status')

if __name__ == '__main__':
    app.run(debug=False, port=5001)
