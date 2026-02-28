import pytest
from app import create_app, _db
from app.models import User, Course, Enrollment

@pytest.fixture
def app():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def auth(client):
    class AuthActions:
        def login(self, username='test', password='test123'):
            return client.post(
                '/auth/login',
                data={'username': username, 'password': password}
            )
        
        def logout(self):
            return client.get('/auth/logout')
        
        def register(self, username='test', password='test123'):
            return client.post(
                '/auth/register',
                data={'username': username, 'password': password}
            )
    
    return AuthActions()

def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register',
        data={'username': 'newuser', 'password': 'newpass123'}
    )
    assert response.status_code == 302
    
    with app.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.check_password('newpass123')

def test_login(client, auth):
    auth.register('testuser', 'testpass')
    response = auth.login('testuser', 'testpass')
    assert response.status_code == 302
    
    response = client.get('/')
    assert b'Hello, testuser' in response.data

def test_login_invalid(client, auth):
    auth.register('testuser', 'testpass')
    response = auth.login('testuser', 'wrongpass')
    assert b'Invalid username or password' in response.data

def test_logout(client, auth):
    auth.register('testuser', 'testpass')
    auth.login('testuser', 'testpass')
    response = auth.logout()
    assert response.status_code == 302
    
    response = client.get('/')
    assert b'Login' in response.data
    assert b'Hello, testuser' not in response.data

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Training Courses' in response.data

def test_create_course(client, auth, app):
    auth.register('testuser', 'testpass')
    auth.login('testuser', 'testpass')
    
    response = client.post(
        '/course/new',
        data={
            'title': 'Python Basics',
            'instructor': 'John Doe',
            'duration': '10',
            'description': 'Learn Python from scratch'
        }
    )
    assert response.status_code == 302
    
    with app.app_context():
        course = Course.query.first()
        assert course is not None
        assert course.title == 'Python Basics'
        assert course.instructor == 'John Doe'
        assert course.duration_hours == 10
        assert course.description == 'Learn Python from scratch'

def test_create_course_requires_login(client):
    response = client.post(
        '/course/new',
        data={
            'title': 'Python Basics',
            'instructor': 'John Doe',
            'duration': '10'
        }
    )
    assert response.status_code == 302
    assert 'login' in response.location

def test_view_course(client, auth, app):
    auth.register('testuser', 'testpass')
    auth.login('testuser', 'testpass')
    
    client.post(
        '/course/new',
        data={
            'title': 'Advanced Python',
            'instructor': 'Jane Smith',
            'duration': '20',
            'description': 'Advanced concepts'
        }
    )
    
    with app.app_context():
        course = Course.query.first()
        response = client.get(f'/course/{course.id}')
        assert response.status_code == 200
        assert b'Advanced Python' in response.data
        assert b'Jane Smith' in response.data

def test_edit_course(client, auth, app):
    auth.register('testuser', 'testpass')
    auth.login('testuser', 'testpass')
    
    client.post(
        '/course/new',
        data={
            'title': 'Original Title',
            'instructor': 'Original Instructor',
            'duration': '10'
        }
    )
    
    with app.app_context():
        course = Course.query.first()
        response = client.post(
            f'/course/{course.id}/edit',
            data={
                'title': 'Updated Title',
                'instructor': 'Updated Instructor',
                'duration': '15'
            }
        )
        assert response.status_code == 302
        
        updated_course = Course.query.get(course.id)
        assert updated_course.title == 'Updated Title'
        assert updated_course.instructor == 'Updated Instructor'
        assert updated_course.duration_hours == 15

def test_delete_course(client, auth, app):
    auth.register('testuser', 'testpass')
    auth.login('testuser', 'testpass')
    
    client.post(
        '/course/new',
        data={
            'title': 'Course to Delete',
            'instructor': 'John Doe',
            'duration': '10'
        }
    )
    
    with app.app_context():
        course = Course.query.first()
        course_id = course.id
        
        response = client.post(f'/course/{course_id}/delete')
        assert response.status_code == 302
        
        deleted_course = Course.query.get(course_id)
        assert deleted_course is None

def test_enroll_student(client, auth, app):
    auth.register('testuser', 'testpass')
    auth.login('testuser', 'testpass')
    
    client.post(
        '/course/new',
        data={
            'title': 'Test Course',
            'instructor': 'John Doe',
            'duration': '10'
        }
    )
    
    with app.app_context():
        course = Course.query.first()
        response = client.post(
            f'/course/{course.id}/enroll',
            data={'student': 'Alice Johnson'}
        )
        assert response.status_code == 302
        
        enrollment = Enrollment.query.first()
        assert enrollment is not None
        assert enrollment.student_name == 'Alice Johnson'
        assert enrollment.course_id == course.id

def test_delete_enrollment(client, auth, app):
    auth.register('testuser', 'testpass')
    auth.login('testuser', 'testpass')
    
    client.post(
        '/course/new',
        data={
            'title': 'Test Course',
            'instructor': 'John Doe',
            'duration': '10'
        }
    )
    
    with app.app_context():
        course = Course.query.first()
        
    client.post(
        f'/course/{course.id}/enroll',
        data={'student': 'Bob Smith'}
    )
    
    with app.app_context():
        enrollment = Enrollment.query.first()
        response = client.post(f'/enrollment/{enrollment.id}/delete')
        assert response.status_code == 302
        
        deleted_enrollment = Enrollment.query.get(enrollment.id)
        assert deleted_enrollment is None

def test_api_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_api_get_courses(client, auth, app):
    auth.register('testuser', 'testpass')
    auth.login('testuser', 'testpass')
    
    client.post(
        '/course/new',
        data={
            'title': 'API Test Course',
            'instructor': 'John Doe',
            'duration': '10'
        }
    )
    
    response = client.get('/api/courses')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == 'API Test Course'

def test_api_create_course(client, auth):
    auth.register('testuser', 'testpass')
    auth.login('testuser', 'testpass')
    
    response = client.post(
        '/api/courses',
        json={
            'title': 'REST API Course',
            'instructor': 'Jane Smith',
            'duration_hours': 15,
            'description': 'Learn REST APIs'
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data

def test_api_get_course(client, auth, app):
    auth.register('testuser', 'testpass')
    auth.login('testuser', 'testpass')
    
    client.post(
        '/course/new',
        data={
            'title': 'Course for API',
            'instructor': 'John Doe',
            'duration': '10'
        }
    )
    
    with app.app_context():
        course = Course.query.first()
        response = client.get(f'/api/courses/{course.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Course for API'
        assert data['instructor'] == 'John Doe'
