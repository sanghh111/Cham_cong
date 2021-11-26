from db import *
import os


class NhanVien:
    def __init__(self) -> None:
        self.service = NhanVienService()

    def add_user(self,id,name,gmail,phone):
        self.service.add_user(id,name,gmail,phone)

    def get_gmail(self,id) -> str:
        return self.service.get_gmail(id)
class NhanVienService:
    def __init__(self) -> None:
        pass

    def add_user(self,id,name,gmail,phone):
        add_user(id,name,gmail,phone)
        path = './data'
        path = os.path.join(path,id)
        os.mkdir(path)

    def get_gmail(self,id):
        return show_user_gmail_by_id(id)
