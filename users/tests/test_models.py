import pytest
from users.models import User



def tt_user():
    assert 2==2 
    

@pytest.mark.django_db
def tt_user_create():
    user = User.objects.create_user(first_name='aom',last_name='kapadia',email='aom.k@ahduni.edu.in',password='cdnuvncjijn')
    assert user.email == 'aom.k@ahduni.edu.in'
    
@pytest.mark.django_db
def tt_user_read(user):
    user=User.objects.all()
    assert user.exists()==True  
    
@pytest.mark.django_db
def tt_user_update(user):
    user.first_name = 'aomkaapdia'
    user.save()
    assert user.first_name=='aomkaapdia'
    
@pytest.mark.django_db
def tt_user_delete(user):
    s = User.objects.all().delete()
    assert User.objects.all().exists()==False
    
@pytest.mark.django_db
def tt_first_name_required():
    try:
        User.objects.cerate_user(last_name='cmndj cnn', email='ndnvnvn@gamil.com',password='fnnrjnjvvvhv')
    except Exception as e:
        assert True

@pytest.mark.django_db
def tt_set_password(user):
    user.set_password='aomkapadia123456'
    user.save()
    assert user.password != 'aomkapadia123456'
        
    
        



    
    
