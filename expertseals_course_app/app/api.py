from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from .models import Course, Enrollment, User
from . import _db

bp = Blueprint('api', __name__, url_prefix='/api')

# Course API endpoints
@bp.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([{
        'id': c.id,
        'title': c.title,
        'description': c.description,
        'instructor': c.instructor,
        'duration_hours': c.duration_hours,
        'created_by': User.query.get(c.created_by).username
    } for c in courses])

@bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify({
        'id': course.id,
        'title': course.title,
        'description': course.description,
        'instructor': course.instructor,
        'duration_hours': course.duration_hours,
        'created_by': User.query.get(course.created_by).username,
        'enrollments': [{
            'id': e.id,
            'student_name': e.student_name
        } for e in course.enrollments]
    })

@bp.route('/courses', methods=['POST'])
@login_required
def create_course():
    data = request.get_json()
    if not data or not all(k in data for k in ['title', 'instructor', 'duration_hours']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    course = Course(
        title=data['title'],
        description=data.get('description'),
        instructor=data['instructor'],
        duration_hours=data['duration_hours'],
        created_by=current_user.id
    )
    _db.session.add(course)
    _db.session.commit()
    return jsonify({'message': 'Course created', 'id': course.id}), 201

@bp.route('/courses/<int:course_id>', methods=['PUT'])
@login_required
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    
    if course.created_by != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Permission denied'}), 403
    
    data = request.get_json()
    course.title = data.get('title', course.title)
    course.description = data.get('description', course.description)
    course.instructor = data.get('instructor', course.instructor)
    course.duration_hours = data.get('duration_hours', course.duration_hours)
    _db.session.commit()
    return jsonify({'message': 'Course updated'}), 200

@bp.route('/courses/<int:course_id>', methods=['DELETE'])
@login_required
def delete_course_api(course_id):
    course = Course.query.get_or_404(course_id)
    
    if course.created_by != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Permission denied'}), 403
    
    _db.session.delete(course)
    _db.session.commit()
    return jsonify({'message': 'Course deleted'}), 200

# Enrollment API endpoints
@bp.route('/courses/<int:course_id>/enrollments', methods=['GET'])
def get_enrollments(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify([{
        'id': e.id,
        'student_name': e.student_name
    } for e in course.enrollments])

@bp.route('/courses/<int:course_id>/enrollments', methods=['POST'])
@login_required
def add_enrollment(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    
    if not data or 'student_name' not in data:
        return jsonify({'error': 'Missing student_name'}), 400
    
    enrollment = Enrollment(student_name=data['student_name'], course=course)
    _db.session.add(enrollment)
    _db.session.commit()
    return jsonify({'message': 'Enrollment created', 'id': enrollment.id}), 201

@bp.route('/enrollments/<int:enrollment_id>', methods=['DELETE'])
@login_required
def delete_enrollment_api(enrollment_id):
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    
    if enrollment.course.created_by != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Permission denied'}), 403
    
    _db.session.delete(enrollment)
    _db.session.commit()
    return jsonify({'message': 'Enrollment deleted'}), 200

# Health check endpoint
@bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200
