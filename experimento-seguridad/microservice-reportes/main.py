from flask import Flask
from flask_restful import Api

from report_controller import ReportController


app = Flask(__name__)

app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(ReportController, '/reports/<string:report_id>')


if __name__ == '__main__':
    app.run(debug=False, port=5002)
