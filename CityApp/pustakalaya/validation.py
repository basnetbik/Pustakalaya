__author__ = 'Pravesh'
from models import *

def UserExists(username):
    try :
        _ = User.objects.get(username=username)
        return True
    except User.DoesNotExist:
        return False

def EmailExists(email):
    try :
        _ = User.objects.get(email=email)
        return True
    except User.DoesNotExist:
        return False


def Validate(username, password):
    try:
        user = User.objects.get(username = username, password = password)
        return user
    except User.DoesNotExist:
        return False