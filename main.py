import os
from api import User

sessions = os.environ.get(key='SESSIONS',default='').split(',')

if __name__ == '__main__': 
    print("begin checkin")
    for session in sessions:
        user = User(session) 
        print('session:',session[:3], '签到结果:', user.checkin().__dict__) 
    print("finish checkin")