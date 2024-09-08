from __init__ import create_app
from flask_restful import Resource, Api
from flask import request
import requests

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)
balanceador_url = 'http://localhost:5001'
active_nodes = {}


class VistaReportStatusNode(Resource):
    def post(self):
        body = request.get_json()
        node_id = body.get('node')
        status = body.get('status')

        if node_id not in active_nodes or status != active_nodes[node_id]:
            active_nodes[node_id] = status

        check_active_nodes()
        print(active_nodes)
        return '', 202


def check_active_nodes():
    all_false = all(status == False for status in active_nodes.values())
    if all_false:
        print("All nodes are inactive.")
        try:
            content = requests.post(f'{balanceador_url}/nodes').json()
            print(f'The node {content["node"]} has been successfully activated.')
        except requests.RequestException as e:
            print(f'Error activating a node: {e}')
    else:
        print("Some nodes are still active.")
        for node, status in active_nodes.items():
            try:
                response = requests.patch(f'{balanceador_url}/nodes/{node}', json={"status": status})
                if response.status_code == 204:
                    print(f'The node {node} has been successfully updated.')
                else:
                    print(f'Error updating the node in balancer {node}. Status code: {response.status_code}')
            except requests.RequestException as e:
                print(f'Error updating the node {node}: {e}')


api.add_resource(VistaReportStatusNode, '/report-status')

if __name__ == '__main__':
    app.run(debug=False, port=5002)
