"""
time: 2019/9/9 
author：hph
"""
import sqlite3
import os
from login.settings import BASE_DIR

class Role():
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(BASE_DIR, '/login/login/user.db'))
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS role
                            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                             role_name TEXT NOT NULL
                            );
''')

    def add_role(self,role_name):
        rs = self.cursor.execute('''
        INSERT INTO role(role_name) VALUES ('{}')
        '''.format(role_name))

        return True

    def get_role_id_by_role_name(self,role_name):
        self.cursor.execute('''
          select id from role WHERE  role_name='{}'
        '''.format(role_name))

        rs = self.cursor.fetchone()
        if rs:
            return rs[0]
    def __del__(self):
        self.conn.commit()
        self.conn.close()
if __name__ == '__main__':
    role = Role()
    role.add_role('user')

    # print(role.get_role_id_by_role_name('admin'))