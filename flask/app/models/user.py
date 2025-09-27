from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    jobs = db.relationship('Job', backref='applicant', lazy=True)

    def __repr__(self):
        return f'<User "{self.username}">'