from db import *

class Manager:
    def __init__(self) -> None:
        self.service = ServiceManager()

    def login(self,account,password):
        return self.service.login(account,password)


class ServiceManager:
    def __init__(self) -> None:
        pass

    def login(self,account,password):
        _password = get_password_manager(account)
        if _password:
            if password  == _password:
                return True
            else :
                return False
        else: 
            return False
