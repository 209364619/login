"""
time: 2019/9/10 
author：hph
"""
import uuid
from pymongo import MongoClient
class User():
    def __init__(self):
        self.client = MongoClient('localhost:27017')
        self.db = self.client.get_database('user')
        self.collections = self.db.get_collection('user')

    def add_user(self,username,password,role,phone_num):
        flag = self.collections.find_one({'phone_num': phone_num})
        if flag:
            return 'the phone already existed'
        _id = str(uuid.uuid4())
        body = {
            '_id':_id,
            'username':username,
            'password':password,
            'role':role,
            'phone_num':phone_num
        }

        if self.collections.insert_one(body):
            return True
    def del_user(self,username):
        pass
    def update_user(self):
        pass
    def search_user_by_name_and_password(self,username,password):
        user = self.collections.find_one({'username':username,'password':password})
        if user:
            return user
        return False

if __name__ == '__main__':
    user = User()
    user.add_user('hph','123','admin','17712153637')