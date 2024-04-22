import pytest 
from main import app
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Fixtures to follow DRY
@pytest.fixture 
def arranged_client():
    return TestClient(app)

@pytest.fixture
def arranged_course_manager():
    from course import CourseManager 
    my_course_manager = CourseManager()
    return my_course_manager

@pytest.fixture
def arranged_user_manager():
    from user import UserManager
    my_user_manager = UserManager()
    return my_user_manager


def test_welcome(arranged_client):
    #Act
    response = arranged_client.get("/")
    #Assert
    assert response.status_code == 200
    # Always should be the following string
    assert response.json() == "Welcome to our miniCanvas!"


def test_create_a_course(arranged_client, arranged_user_manager):
    #Arrange
    arranged_user_manager.create_a_user("John", "pwd", "student")
    arranged_user_manager.create_a_user("Alice", "pwd", "teacher")
    arranged_user_manager.create_a_user("Jimmy", "pwd", "student")

    #Act
    response = arranged_client.post(
        "/courses/{coursecode}",
            headers = {"accept" : "application/json"},
            json = {"coursecode" : "COSC381", "semester" : "Winter2024", "teacher_id_list" : [2]}
    )
    
    #Assert
    assert response.status_code == 200
      


def test_import_students(arranged_client, arranged_user_manager, arranged_course_manager):
    #Arrange
    arranged_user_manager.create_a_user("John", "pwd", "student")
    arranged_user_manager.create_a_user("Alice", "pwd", "teacher")
    arranged_user_manager.create_a_user("Jimmy", "pwd", "student")

    #Act
    teacher_list = arranged_user_manager.find_users([2])
    course_id = arranged_course_manager.create_a_course("COSC381", "Winter2024", teacher_list)

    response = arranged_client.put(
        "/courses/1/students",
            headers = {"accept" : "application/json"},
            json = {"courseid" : 1, "student_id_list" : [1,3]}
    )

    #Assert
    assert response.status_code == 200


def test_import_students_invalid(arranged_client, arranged_user_manager, arranged_course_manager):
    arranged_user_manager.create_a_user("John", "pwd", "student")
    arranged_user_manager.create_a_user("Alice", "pwd", "teacher")
    arranged_user_manager.create_a_user("Jimmy", "pwd", "student")

    teacher_list = arranged_user_manager.find_users([2])
    course_id = arranged_course_manager.create_a_course("COSC381", "Winter2024", teacher_list)

    response = arranged_client.put(
        "/courses/1/students",
            headers = {"accept" : "application/json"},
            json = {"courseid" : 1, "students" : [1,3]}
    )
    
    assert response.status_code == 422
    assert response.json() == {"detail" : "Request body must contain 'student_id_list'."}


def test_create_a_course_not_found(arranged_client, arranged_user_manager, arranged_course_manager):
    arranged_user_manager.create_a_user("John", "pwd", "student")
    arranged_user_manager.create_a_user("Alice", "pwd", "teacher")
    arranged_user_manager.create_a_user("Jimmy", "pwd", "student")

    teacher_list = arranged_user_manager.find_users([2])
    course_id = arranged_course_manager.create_a_course("COSC381", "Winter2024", teacher_list)
    
    response = arranged_client.put(
        "/courses/4/students",
            headers = {"accept" : "application/json"},
            json = {"courseid" : 4, "student_id_list" : [1,3]}
    )

    assert response.status_code == 404
    assert response.json() == {"detail" : "Course not found."}