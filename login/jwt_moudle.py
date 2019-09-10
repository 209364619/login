import jwt
import time

class JwtMoudle():
    def __init__(self, secret_key='secret_key', algorithm='HS256'):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.duration = 3600*3

    def get_token(self, data_dict):
        '''
        generate token
        :param data_dict: information needed to transfor to token
        :return: str token
        '''
        generate_time = int(time.time())
        end_time = int(time.time())+self.duration

        data_dict['generate_time'] = generate_time
        data_dict['end_time'] = end_time

        return jwt.encode(data_dict, self.secret_key, algorithm=self.algorithm).decode('utf-8')

    def get_origin_msg(self, token):
        '''
        get message in msg
        :param token:  str
        :return: str the information in token
        '''
        return jwt.decode(token, self.secret_key, self.algorithm)


if __name__ == '__main__':
    j = JwtMoudle()
    data = {'name': 'mike', 'age': 23}
    token = j.get_token(data)
    print(token)
    msg = j.get_origin_msg(token)
    print(msg)
