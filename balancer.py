import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return {'message': 'Hello, Balancer!'}

if __name__ == '__main__':
    app.run(debug=True, port=os.environ.get('PORT', 5001))
