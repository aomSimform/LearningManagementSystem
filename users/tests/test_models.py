import pytest
from users.models import User



def test_user():
    assert 2==2 
    

@pytest.mark.django_db
def tt_user_created():
    user = User.objects.create(email='aom.k@ahduni8.edu.in',password='cndjvnvjfnvjfn',first_name = 'aom', last_name='kapadia')
    assert user.email == 'aom.k@ahduni8.edu.in'
    
    
    
