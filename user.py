
# Работа с пользователем
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email 

def chek_user(user):
    if user:
        print('OK')
