import pytest

@pytest.fixture
def arranged_user_manager():
    from user import UserManager
    my_user_manager = UserManager()
    return my_user_manager

@pytest.fixture
def arranged_user_ids(arranged_user_manager):
    arranged_user_manager.create_a_user("Kevin Hart", "khart", "teacher")
    arranged_user_manager.create_a_user("Steve Carell", "steve01", "student")
    arranged_user_manager.create_a_user("Jenna Fischer", "fischjen", "student")
    ids = (1, 2, 3)
    return ids


def test_generate_id(arranged_user_manager):
    #Arrange
    count = arranged_user_manager.counter

    #Act
    result = arranged_user_manager.generate_id()

    #Assert
    assert(result == (count + 1))


def test_create_a_user(arranged_user_manager):
    #Arrange
    new_index = len(arranged_user_manager.user_list)
    count = arranged_user_manager.counter

    #Act 
    arranged_user_manager.create_a_user("Apollo Schaefer", "cs123", "student")

    #Assert
    assert((len(arranged_user_manager.user_list)) == (new_index + 1))
    assert(arranged_user_manager.user_list[new_index].name == "Apollo Schaefer")
    assert(arranged_user_manager.user_list[new_index].password == "cs123")
    assert(arranged_user_manager.user_list[new_index].type == "student")
    assert(arranged_user_manager.counter == (count + 1))


def test_find_users_empty(arranged_user_manager):
    #Act
    ids = (1, 2, 3)
    result = arranged_user_manager.find_users(ids)

    #Assert
    assert(result == "Not found.")


def test_find_users(arranged_user_manager, arranged_user_ids):
    #Act
    result = arranged_user_manager.find_users(arranged_user_ids)

    #Assert
def test_find_users(arranged_user_manager, arranged_user_ids):
    # Act
    result = arranged_user_manager.find_users(arranged_user_ids)

    # Assert
    assert len(result) == 3
    assert result[0].name == "Kevin Hart"
    assert result[1].name == "Steve Carell"
    assert result[2].name == "Jenna Fischer"
    


def test_find_users_behavior(mocker, arranged_user_manager, arranged_user_ids):
    #Arrange
    mocked_find_users = mocker.patch('user.UserManager.find_users')
   
    #Act
    result = arranged_user_manager.find_users(arranged_user_ids)

    #Assert
    mocked_find_users.assert_called_with(arranged_user_ids)



def test_create_a_user_behavior(mocker, arranged_user_manager):
    #Arrange
    mocked_create_a_user = mocker.patch('user.UserManager.create_a_user')

    #Act 
    arranged_user_manager.create_a_user("James Franco", "fracoj34", "student")

    #Assert
    mocked_create_a_user.assert_called_with("James Franco", "fracoj34", "student")