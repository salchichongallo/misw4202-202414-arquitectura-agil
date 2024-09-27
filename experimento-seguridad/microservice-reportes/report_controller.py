from flask import jsonify, make_response
from flask_restful import Resource
from report_models import db, ReportModel


class ReportController(Resource):
    def get(self, report_id):
        # TODO: check if user is authorized to view this report
        return self.get_report(report_id)

    def get_report(self, report_id):
        report = db.session.query(ReportModel).get(report_id)
        if report:
            return jsonify(report.to_dict())
        return make_response(jsonify({ 'message': 'Report not found' }), 404)
