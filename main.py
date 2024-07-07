import os
from api import User
from recaptcha import EzCaptchaImpl

sessions = os.environ.get(key='SESSIONS', default='').split(',')
http_proxy = os.environ.get(key='HTTP_PROXY', default=None)

if __name__ == '__main__': 
    print("begin checkin")
    for session in sessions:
        if session:
            user = User(session, EzCaptchaImpl())
            if http_proxy:
                user.session.proxies.update({
                    'http': http_proxy,
                    'https': http_proxy,
                })
            print('session:',session[:3], '签到结果:', user.checkin().__dict__) 
    print("finish checkin")