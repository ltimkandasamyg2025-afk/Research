from . import _db
from flask_login import UserMixin
from flask import current_app
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, _db.Model):
    id = _db.Column(_db.Integer, primary_key=True)
    username = _db.Column(_db.String(100), unique=True, nullable=False)
    password_hash = _db.Column(_db.String(255), nullable=False)
    is_admin = _db.Column(_db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_reset_token(self):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps({'user_id': self.id}, salt='password-reset-salt')

    @staticmethod
    def verify_reset_token(token, max_age=1800):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token, salt='password-reset-salt', max_age=max_age)
        except (BadSignature, SignatureExpired):
            return None

        return User.query.get(data.get('user_id'))

class Course(_db.Model):
    id = _db.Column(_db.Integer, primary_key=True)
    title = _db.Column(_db.String(100), nullable=False)
    description = _db.Column(_db.Text, nullable=True)
    instructor = _db.Column(_db.String(100), nullable=False)
    duration_hours = _db.Column(_db.Integer, nullable=False)
    created_by = _db.Column(_db.Integer, _db.ForeignKey('user.id'), nullable=False)
    created_user = _db.relationship('User', backref=_db.backref('courses', lazy=True))

class Enrollment(_db.Model):
    id = _db.Column(_db.Integer, primary_key=True)
    student_name = _db.Column(_db.String(100), nullable=False)
    course_id = _db.Column(_db.Integer, _db.ForeignKey('course.id'), nullable=False)
    course = _db.relationship('Course', backref=_db.backref('enrollments', lazy=True))
