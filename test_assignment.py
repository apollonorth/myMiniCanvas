import pytest

@pytest.fixture
def arranged_assignment():
    from assignment import Assignment
    my_assignment = Assignment(1, 'April 22', 2)
    return my_assignment

@pytest.fixture
def arranged_submission():
    from assignment import Submission
    my_submission = Submission(5, "assignment")
    return my_submission


def test_submit(arranged_assignment, arranged_submission):  
    #Arrange
    new_index = len(arranged_assignment.submission_list)
    
    #Act
    arranged_assignment.submit(arranged_submission)
    
    #Assert
    assert(len(arranged_assignment.submission_list) == (new_index + 1))
    assert(arranged_assignment.submission_list[0].student_id == 5)
    assert(arranged_assignment.submission_list[0].submission == "assignment")
    


def test_submit_behavior(mocker, arranged_assignment, arranged_submission):
    #Arrange
    new_index = len(arranged_assignment.submission_list)
    mocked_submit = mocker.patch('assignment.Assignment.submit')

    #Act
    arranged_assignment.submit(arranged_submission)
    
    #Assert
    mocked_submit.assert_called_with(arranged_submission)