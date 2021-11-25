from db import *
import os


class NhanVien:
    def __init__(self) -> None:
        self.service = NhanVienService()

    def add_user(self,id,name,gmail,phone):
        self.service.add_user(id,name,gmail,phone)


class NhanVienService:
    def __init__(self) -> None:
        pass

    def add_user(self,id,name,gmail,phone):
        add_user(id,name,gmail,phone)
        path = './data'
        path = os.path.join(path,id)
        os.mkdir(path)
