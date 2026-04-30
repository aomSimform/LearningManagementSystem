import pytest 
from users.models import User
from rest_framework.test import APIClient

@pytest.fixture
def first_name():
    return 'aom'

@pytest.fixture
def last_name():
    return 'kapadia'

@pytest.fixture
def email():
    return 'aom.k@ahduni.edu.in'

@pytest.fixture
def password():
    return 'aomkapadia1234567890'

@pytest.fixture
def user(first_name, last_name, password, email):
    user = User.objects.create_user(first_name=first_name, last_name=last_name, password=password,email=email)
    return user


@pytest.fixture 
def api_client():
    yield APIClient()