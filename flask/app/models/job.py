from app.extensions import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jobTitle = db.Column(db.String(150), nullable=False)
    jobUrl = db.Column(db.Text)
    callBack = db.Column(db.Boolean, nullable=True)
    interview = db.Column(db.Boolean, nullable=True)
    dateApplied = db.Column(db.Date)
    
    personApplied = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Job "{self.jobTitle}">'
