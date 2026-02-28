import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:5000"

# First, register the new users
print("=" * 60)
print("REGISTERING NEW USERS")
print("=" * 60)

# Register Admin User
admin_data = {
    "username": "admin_instructor",
    "password": "AdminPass123!"
}
admin_response = requests.post(f"{BASE_URL}/auth/register", data=admin_data)
print(f"\n✓ Admin User Registration:")
print(f"  Username: {admin_data['username']}")
print(f"  Password: {admin_data['password']}")
print(f"  Status: {'Success' if admin_response.status_code in [200, 302] else 'Failed'}")

# Register Student User
student_data = {
    "username": "student_john",
    "password": "StudentPass123!"
}
student_response = requests.post(f"{BASE_URL}/auth/register", data=student_data)
print(f"\n✓ Student User Registration:")
print(f"  Username: {student_data['username']}")
print(f"  Password: {student_data['password']}")
print(f"  Status: {'Success' if student_response.status_code in [200, 302] else 'Failed'}")

# Login as admin_instructor to create courses
print("\n" + "=" * 60)
print("LOGGING IN AND CREATING COURSES")
print("=" * 60)

session = requests.Session()
login_response = session.post(f"{BASE_URL}/auth/login", data=admin_data)
print(f"\n✓ Admin Login Status: {'Success' if login_response.status_code == 302 else 'Failed'}")

# Create 3 courses
courses_data = [
    {
        "title": "Python for Beginners",
        "instructor": "Dr. Sarah Mitchell",
        "duration": "20",
        "description": "Learn Python fundamentals including variables, loops, functions, and basic data structures. Perfect for beginners with no programming experience."
    },
    {
        "title": "Advanced Web Development with React",
        "instructor": "James Chen",
        "duration": "40",
        "description": "Master modern web development using React.js, including state management, hooks, and building scalable single-page applications."
    },
    {
        "title": "Cloud Architecture on AWS",
        "instructor": "Emma Rodriguez",
        "duration": "30",
        "description": "Learn AWS cloud services including EC2, S3, Lambda, RDS, and design scalable cloud-based applications. Industry-standard practices included."
    }
]

print("\n✓ Creating 3 Courses:\n")
for idx, course in enumerate(courses_data, 1):
    response = session.post(f"{BASE_URL}/course/new", data=course)
    status = "✓ Created" if response.status_code == 302 else "✗ Failed"
    print(f"  {idx}. {course['title']}")
    print(f"     Instructor: {course['instructor']}")
    print(f"     Duration: {course['duration']} hours")
    print(f"     Status: {status}\n")

print("=" * 60)
print("SUMMARY - LOGIN CREDENTIALS")
print("=" * 60)

print("\n📋 DEFAULT ADMIN USER (Pre-existing):")
print("  Username: admin")
print("  Password: admin123")

print("\n📋 NEW ADMIN INSTRUCTOR USER:")
print(f"  Username: {admin_data['username']}")
print(f"  Password: {admin_data['password']}")

print("\n📋 NEW STUDENT USER:")
print(f"  Username: {student_data['username']}")
print(f"  Password: {student_data['password']}")

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
