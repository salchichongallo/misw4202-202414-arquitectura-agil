from flask import jsonify
from flask_restful import Resource


class ReportController(Resource):
    def get(self, report_id):
        return jsonify({ 'report_id': report_id })
