import sys
sys.path.insert(0, '/c/Kandasamy/Code/GithubCopilot Model/expertseals_course_app')

from app import create_app, _db
from app.models import User, Course

# Create app context
app = create_app()

with app.app_context():
    # Create new users
    print("=" * 60)
    print("CREATING USERS")
    print("=" * 60)
    
    # Admin Instructor User
    admin_instructor = User(username='admin_instructor', is_admin=False)
    admin_instructor.set_password('AdminPass123!')
    _db.session.add(admin_instructor)
    print("\n✓ Admin Instructor User created:")
    print(f"  Username: admin_instructor")
    print(f"  Password: AdminPass123!")
    
    # Student User
    student_user = User(username='student_john', is_admin=False)
    student_user.set_password('StudentPass123!')
    _db.session.add(student_user)
    print("\n✓ Student User created:")
    print(f"  Username: student_john")
    print(f"  Password: StudentPass123!")
    
    _db.session.commit()
    
    # Get the admin_instructor user to use as creator
    admin_instructor = User.query.filter_by(username='admin_instructor').first()
    
    # Create 3 courses
    print("\n" + "=" * 60)
    print("CREATING COURSES")
    print("=" * 60)
    
    courses_data = [
        {
            "title": "Python for Beginners",
            "instructor": "Dr. Sarah Mitchell",
            "duration_hours": 20,
            "description": "Learn Python fundamentals including variables, loops, functions, and basic data structures. Perfect for beginners with no programming experience."
        },
        {
            "title": "Advanced Web Development with React",
            "instructor": "James Chen",
            "duration_hours": 40,
            "description": "Master modern web development using React.js, including state management, hooks, and building scalable single-page applications."
        },
        {
            "title": "Cloud Architecture on AWS",
            "instructor": "Emma Rodriguez",
            "duration_hours": 30,
            "description": "Learn AWS cloud services including EC2, S3, Lambda, RDS, and design scalable cloud-based applications. Industry-standard practices included."
        }
    ]
    
    print("\n✓ Adding 3 Courses:\n")
    for idx, course_data in enumerate(courses_data, 1):
        course = Course(
            title=course_data['title'],
            instructor=course_data['instructor'],
            duration_hours=course_data['duration_hours'],
            description=course_data['description'],
            created_by=admin_instructor.id
        )
        _db.session.add(course)
        print(f"  {idx}. {course_data['title']}")
        print(f"     Instructor: {course_data['instructor']}")
        print(f"     Duration: {course_data['duration_hours']} hours\n")
    
    _db.session.commit()
    
    print("=" * 60)
    print("SUMMARY - LOGIN CREDENTIALS")
    print("=" * 60)
    
    print("\n📋 DEFAULT ADMIN USER (Pre-existing):")
    print("  Username: admin")
    print("  Password: admin123")
    print("  Role: System Administrator")
    
    print("\n📋 NEW ADMIN INSTRUCTOR USER:")
    print("  Username: admin_instructor")
    print("  Password: AdminPass123!")
    print("  Role: Instructor (Can create and manage courses)")
    
    print("\n📋 NEW STUDENT USER:")
    print("  Username: student_john")
    print("  Password: StudentPass123!")
    print("  Role: Student (Can view and enroll in courses)")
    
    print("\n" + "=" * 60)
    print("✓ ALL SETUP COMPLETE!")
    print("=" * 60)
    print("\nYou can now:")
    print("  1. Login with any of the above credentials")
    print("  2. View the 3 new courses created")
    print("  3. Enroll students in courses")
    print("  4. Use the API endpoints")
    print("\nAccess the app at: http://127.0.0.1:5000")
    print("=" * 60)
