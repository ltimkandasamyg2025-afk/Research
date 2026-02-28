# ExpertSeals Training Course Management Application

This is a fully-featured Python-based web application built with Flask that allows the ExpertSeals organization to manage training courses and student enrollments. It includes user authentication, course and enrollment management with edit/delete functionality, a RESTful API, responsive styling, and comprehensive unit/integration tests.

---

## 🔧 Project Structure

```
expertseals_course_app/
├── app/
│   ├── __init__.py        # Application factory and extension setup
│   ├── models.py          # SQLAlchemy models (User, Course, Enrollment)
│   ├── routes.py          # View functions and blueprint for web UI
│   ├── auth.py            # Authentication routes (login, register, logout)
│   ├── api.py             # REST API endpoints
│   ├── static/
│   │   └── style.css      # Comprehensive CSS styling
│   └── templates/         # HTML templates (Jinja2)
│       ├── base.html      # Base template with navigation
│       ├── index.html     # Course listing page
│       ├── course.html    # Course detail page
│       ├── new_course.html
│       ├── edit_course.html
│       └── auth/
│           ├── login.html
│           └── register.html
├── test_app.py            # Unit and integration tests
├── requirements.txt       # Python dependencies
├── run.py                 # Entry point to launch the development server
└── DOCUMENTATION.md       # This documentation file
```

> The code uses a SQLite database named `courses.db` by default. The file is created automatically in the project root when the app first runs. A default admin user (username: `admin`, password: `admin123`) is created automatically.

---

## ✨ Features

### User Authentication
- **Registration** – Create a new user account with a username and password.
- **Login/Logout** – Secure user sessions with Flask-Login.
- **Admin Users** – Special privileges for administrators to manage all courses and enrollments.
- **Default Admin** – Pre-configured admin account for initial setup.

### Course Management (CRUD)
- **Create Courses** – Add new courses with title, instructor, duration, and description (requires login).
- **View Courses** – Browse all available courses on the home page with card-based layout.
- **Edit Courses** – Update course details (only the creator or admin can edit).
- **Delete Courses** – Remove courses from the system (only the creator or admin can delete).
- **Course Details** – View comprehensive course information including enrollment list.

### Student Enrollments
- **Enroll Students** – Add students to courses by name.
- **View Enrollments** – See all enrolled students for a specific course.
- **Remove Enrollments** – Delete student enrollments (only the course creator or admin can remove).

### REST API
- **GET /api/courses** – Retrieve all courses as JSON.
- **GET /api/courses/<course_id>** – Get details of a specific course including enrollments.
- **POST /api/courses** – Create a new course (requires authentication).
- **PUT /api/courses/<course_id>** – Update a course (requires permission).
- **DELETE /api/courses/<course_id>** – Delete a course (requires permission).
- **GET /api/courses/<course_id>/enrollments** – Get enrollments for a course.
- **POST /api/courses/<course_id>/enrollments** – Add a student enrollment.
- **DELETE /api/enrollments/<enrollment_id>** – Remove an enrollment.
- **GET /api/health** – Health check endpoint.

### User Interface
- **Responsive Design** – Mobile-friendly layout that adapts to different screen sizes.
- **Professional Styling** – Clean, modern CSS with color scheme and intuitive navigation.
- **Flash Messages** – User feedback for successful actions and error messages.
- **Navigation Bar** – Easy access to main pages and user account controls.
- **Card-Based Layout** – Courses displayed in an attractive grid.

### Testing
- **Unit Tests** – Comprehensive tests for models and core functionality.
- **Integration Tests** – Full workflow tests including authentication, CRUD, and API operations.
- **Test Database** – In-memory SQLite for fast, isolated test execution.
- **Pytest Framework** – Modern testing framework with fixtures and parametrization support.

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or navigate to the project directory**:
   ```powershell
   cd expertseals_course_app
   ```

2. **Create a virtual environment** (recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```powershell
   python run.py
   ```

   The development server will start at `http://127.0.0.1:5000/`.

5. **Access the application** – Open your browser and navigate to the URL above.

### Default Credentials
- **Username:** `admin`
- **Password:** `admin123`

---

## 🔐 Authentication & Authorization

The application uses Flask-Login for session management and supports role-based access control:

- **Authenticated Users** – Can create courses and enroll students.
- **Course Creators** – Can edit and delete their own courses.
- **Admins** – Can edit and delete any course or enrollment.
- **Public Access** – View courses and course details without logging in.

---

## ⚙️ Configuration

Settings are defined in `app/__init__.py`:

```python
app.config.from_mapping(
    SECRET_KEY='dev-secret-key-change-in-production',
    SQLALCHEMY_DATABASE_URI='sqlite:///courses.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
```

### For Production:
- Change `SECRET_KEY` to a strong, random value (load from environment variable).
- Switch `SQLALCHEMY_DATABASE_URI` to PostgreSQL or MySQL.
- Set `FLASK_ENV=production` and `FLASK_DEBUG=False`.

---

## 🧪 Testing

Run all tests with code coverage:

```powershell
pytest test_app.py --cov=app --cov-report=html
```

Run specific tests:

```powershell
pytest test_app.py::test_register
pytest test_app.py::test_create_course
pytest test_app.py::test_api_get_courses
```

### Test Coverage
The test suite includes:
- User authentication (register, login, logout)
- Course CRUD operations
- Enrollment management
- Permission checks
- REST API endpoints
- Health check

---

## 🚀 API Usage Examples

### Get All Courses
```bash
curl http://127.0.0.1:5000/api/courses
```

### Create a Course (requires authentication)
```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Web Development",
    "instructor": "Alice Brown",
    "duration_hours": 40,
    "description": "Learn modern web technologies"
  }'
```

### Get Course Details
```bash
curl http://127.0.0.1:5000/api/courses/1
```

### Update a Course
```bash
curl -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Advanced Web Development"}'
```

### Delete a Course
```bash
curl -X DELETE http://127.0.0.1:5000/api/courses/1
```

---

## 📊 Database Models

### User
- `id` – Primary key
- `username` – Unique identifier
- `password_hash` – Hashed password
- `is_admin` – Boolean flag for admin privileges

### Course
- `id` – Primary key
- `title` – Course name
- `description` – Detailed description
- `instructor` – Instructor name
- `duration_hours` – Course length in hours
- `created_by` – Foreign key to User who created it

### Enrollment
- `id` – Primary key
- `student_name` – Name of enrolled student
- `course_id` – Foreign key to Course

---

## 🧩 Extending the Application

Here are some ideas for next steps:

1. **Authentication**: Add user login so only administrators can create courses or enrollments.
2. **Editing/Deleting**: Provide endpoints to update or remove courses and enrollments.
3. **REST API**: Expose JSON endpoints for integration with external systems.
4. **Styling**: Add CSS/JS in `app/static` for improved UI.
5. **Deployment**: Containerize with Docker and deploy to a cloud provider.
6. **Testing**: Write unit and integration tests using Flask’s `app.test_client()` and a temporary database.

---

## ✅ Summary

This repository delivers a lightweight yet functional course management tool for ExpertSeals, built entirely in Python using Flask. The architecture emphasizes clarity and extensibility, making it an excellent starting point for further features and real-world deployment.

Feel free to modify the models, add new views, or integrate with existing systems as needed.

_for questions or support, reach out to the development team at ExpertSeals._
