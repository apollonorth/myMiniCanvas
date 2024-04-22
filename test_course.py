import pytest
from course import Course, CourseManager

# Fixtures to abide by DRY
@pytest.fixture
def arranged_user_manager():
    from user import UserManager
    my_user_manager = UserManager()
    return my_user_manager

@pytest.fixture
def arranged_course_manager():
    my_course_manager = CourseManager()
    return my_course_manager

@pytest.fixture
def arranged_teacher_list(arranged_user_manager):
    arranged_user_manager.create_a_user("Apollo Schaefer", 
                                        "computerscience123", 
                                        "teacher")
    teacher_ids = [1]
    teacher_list = arranged_user_manager.find_users(teacher_ids)
    return teacher_list

@pytest.fixture
def arranged_new_course(arranged_teacher_list):
    from course import Course
    new_course = Course(1, "COSC 381", "W24", arranged_teacher_list)
    return new_course



def test_generate_id(arranged_course_manager):
    #Arrange
    count = arranged_course_manager.counter

    #Act
    result = arranged_course_manager.generate_id()

    #Assert
    assert(result == (count + 1))



def test_find_a_course(arranged_course_manager, arranged_teacher_list):
    #Arrange    
    new_course_id = arranged_course_manager.create_a_course("COSC381", "Winter2024", arranged_teacher_list)

    #Act
    result = arranged_course_manager.find_a_course(new_course_id)

    #Assert
    for teacher in result.teacher_list:
        assert(teacher.type == "teacher")

    assert(result.course_code == "COSC381")
    assert(result.semester == "Winter2024")
    assert(result.course_id == new_course_id)
    


def test_create_a_course(mocker, arranged_course_manager, arranged_teacher_list):
    #Arrange    
    new_index = len(arranged_course_manager.course_list)
    new_count = arranged_course_manager.counter
    mocked_create_a_course = mocker.patch('course.CourseManager.create_a_course')

    #Act
    new_course_id = arranged_course_manager.create_a_course("COSC381", "Winter2024", arranged_teacher_list)

    #Assert
    mocked_create_a_course.assert_called_with("COSC381", "Winter2024", arranged_teacher_list)


def test_import_students(arranged_user_manager, arranged_new_course):
    #Arrange
    arranged_user_manager.create_a_user("Steve Carell", "steve01", "student")
    arranged_user_manager.create_a_user("Kevin Hart", "khart", "student")
    arranged_user_manager.create_a_user("Jenna Fischer", "fischjen", "student")
    student_ids = [2, 3, 4]
    student_list = arranged_user_manager.find_users(student_ids)

    #Act 
    arranged_new_course.import_students(student_list)

    #Assert
    for student in arranged_new_course.student_list:
        assert(student.type == "student")



def test_create_an_assignment(arranged_new_course):
    #Arrange
    new_count = arranged_new_course.assignment_counter
    new_index = len(arranged_new_course.assignment_list)

    #Act
    arranged_new_course.create_an_assignment("April 22")

    #Assert
    assert(arranged_new_course.assignment_list[new_index].due_date == "April 22")
    assert(arranged_new_course.assignment_counter == (new_count + 1))
    assert(len(arranged_new_course.assignment_list) == (new_index + 1))
    
def test_generate_assignment_id(arranged_new_course):
    #Arrange
    count = arranged_new_course.assignment_counter

    #Act 
    result = arranged_new_course.generate_assignment_id()

    #Assert
    assert(result == (count + 1))