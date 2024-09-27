import requests
from flask_restful import Resource
from report_models import db, ReportModel
from flask import jsonify, make_response, request


def get_role_url(permission):
    return f'http://localhost:5001/validate-role?permiso={permission}'


class ReportController(Resource):
    def get(self, report_id):
        response = self.check_read_permission()
        if not response.ok:
            return make_response(response.json(), response.status_code)
        return self.get_report(report_id)

    def check_read_permission(self):
        url = get_role_url(permission='PUEDE_VER_REPORTES')
        return requests.get(url, headers=request.headers)

    def get_report(self, report_id):
        report = db.session.query(ReportModel).get(report_id)
        if report:
            return jsonify(report.to_dict())
        return make_response(jsonify({ 'message': 'Report not found' }), 404)
