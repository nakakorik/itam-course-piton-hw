import string
import random

_letters = string.ascii_letters + string.digits

def rand_string(k:int)->str:
    return ''.join(random.choices(_letters,k=k))
