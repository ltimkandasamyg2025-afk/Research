from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Course, Enrollment
from . import _db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@bp.route('/course/new', methods=('GET', 'POST'))
@login_required
def new_course():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description')
        instructor = request.form['instructor']
        duration = int(request.form['duration'])
        course = Course(title=title, description=description, instructor=instructor, 
                       duration_hours=duration, created_by=current_user.id)
        _db.session.add(course)
        _db.session.commit()
        flash('Course created successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('new_course.html')

@bp.route('/course/<int:course_id>')
def view_course(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course.html', course=course)

@bp.route('/course/<int:course_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    
    if course.created_by != current_user.id and not current_user.is_admin:
        flash('You do not have permission to edit this course.', 'error')
        return redirect(url_for('main.view_course', course_id=course_id))
    
    if request.method == 'POST':
        course.title = request.form['title']
        course.description = request.form.get('description')
        course.instructor = request.form['instructor']
        course.duration_hours = int(request.form['duration'])
        _db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('main.view_course', course_id=course_id))
    
    return render_template('edit_course.html', course=course)

@bp.route('/course/<int:course_id>/delete', methods=('POST',))
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    
    if course.created_by != current_user.id and not current_user.is_admin:
        flash('You do not have permission to delete this course.', 'error')
        return redirect(url_for('main.view_course', course_id=course_id))
    
    _db.session.delete(course)
    _db.session.commit()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('main.index'))

@bp.route('/course/<int:course_id>/enroll', methods=('POST',))
@login_required
def enroll(course_id):
    course = Course.query.get_or_404(course_id)
    student = request.form['student']
    enrollment = Enrollment(student_name=student, course=course)
    _db.session.add(enrollment)
    _db.session.commit()
    flash(f'{student} enrolled successfully!', 'success')
    return redirect(url_for('main.view_course', course_id=course_id))

@bp.route('/enrollment/<int:enrollment_id>/delete', methods=('POST',))
@login_required
def delete_enrollment(enrollment_id):
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    course_id = enrollment.course_id
    
    if enrollment.course.created_by != current_user.id and not current_user.is_admin:
        flash('You do not have permission to remove this enrollment.', 'error')
        return redirect(url_for('main.view_course', course_id=course_id))
    
    _db.session.delete(enrollment)
    _db.session.commit()
    flash('Enrollment removed successfully!', 'success')
    return redirect(url_for('main.view_course', course_id=course_id))

