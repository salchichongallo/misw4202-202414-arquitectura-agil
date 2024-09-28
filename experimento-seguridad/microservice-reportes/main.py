from flask import Flask
from flask_restful import Api

from report_models import db
from report_controller import ReportController

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(ReportController, '/reports/<string:report_id>')


if __name__ == '__main__':
    db.init_app(app)
    db.create_all()
    app.run(debug=False, port=5002, host='0.0.0.0')
