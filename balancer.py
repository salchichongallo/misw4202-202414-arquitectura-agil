import os
from requests import post
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return {'message': 'Hello, Balancer!'}

@app.post('/forward-call')
def forward_call():
    # TODO: Forward call to the next available microservice
    response = post('http://localhost:5002/call', json=request.json)
    return { 'data': response.json(), 'forwarded': True }

if __name__ == '__main__':
    app.run(debug=True, port=os.environ.get('PORT', 5001))
