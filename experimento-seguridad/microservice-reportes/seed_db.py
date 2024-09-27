from report_models import ReportModel
from main import app, db


db.init_app(app)
db.create_all()

reports = [
    ReportModel(user_id=1, title='Sample Report', content='This is a sample report.'),
    ReportModel(user_id=1, title='Another Report', content='This is another sample report.'),
    ReportModel(user_id=2, title='Foo Report', content='Content of foo report.'),
]

db.session.bulk_save_objects(reports)
db.session.commit()
db.session.close()

print('Reports database seeded successfully.')
