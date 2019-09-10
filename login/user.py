"""
time: 2019/9/9 
author：hph
"""
import sqlite3
import hashlib
from login.role import Role
class User():
    def __init__(self):
        self.conn = sqlite3.connect('user.db')
        self.cursor = self.conn.cursor()

    def create_user_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                    username TEXT,
                                    password TEXT,
                                    role_id INT,
                                    FOREIGN KEY (role_id) REFERENCES Role(id) 
                                    );
                ''')

    def add_user(self,username,password,role_name):
        role = Role()
        role_id = role.get_role_id_by_role_name(role_name)
        password = self.password_encrypt(password)
        if role_id:
            #用户名是否可以用
            self.cursor.execute('''select * from user WHERE username='%s' ''' % username)
            user = self.cursor.fetchone()
            if not user:
                self.cursor.execute('''
                insert into user(username,password,role_id) VALUES ('{}','{}','{}')
                '''.format(username,password,role_id))
            else:
                return 'username exist'
        else:
            return 'role_name not exist'
        return True
    def auth_by_name_passwd(self,username,passwd):
        passwd = self.password_encrypt(passwd)
        self.cursor.execute('''
        select * from user WHERE username='%s' and password='%s'
        ''' % (username, passwd))
        user = self.cursor.fetchone()

        if user:
            return self.get_user_by_username()
        else:
            return False

    def get_user_by_username(self,username):
        self.cursor.execute('''
        select user.username,role.role_name from user LEFT JOIN role ON user.role_id=role.id WHERE username='%s'
        ''' % username)

        user = self.cursor.fetchone()
        if user:
            user = {'username':user[0],'role':user[1]}
        return user
    def password_encrypt(self,password):
        passwd = password.encode('utf-8')
        hash_passwd = hashlib.md5(passwd).hexdigest()
        return hash_passwd
    def __del__(self):
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    user = User()
    # user.create_user_table()
    # print(user.add_user('hph','123','admin'))
    # rs = user.auth_by_name_passwd('hph','123')
    rs = user.get_user_by_username('hph')
    print(rs)