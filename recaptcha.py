
import json
import os
import time

import requests


class CaptchaInterface:
    def cap(
            self,
            websiteURL: str, 
            websiteKey: str, 
            type: str = 'ReCaptchaV2TaskProxyless',
            isInvisible: bool = False
        ) -> str:
        raise NotImplementedError()
    
class EzCaptchaImpl(CaptchaInterface):
    def __init__(self) -> None:
        super().__init__()
        self.client_key = os.environ.get("EZCAPTCHA_CLIENT_KEY", default='')
        if self.client_key == '':
            raise EnvironmentError("缺少环境变量 EZCAPTCHA_CLIENT_KEY")

    def __create_task(
            self,
            websiteURL: str, 
            websiteKey: str, 
            pageAction: str,
            type: str = 'ReCaptchaV3TaskProxyless',
            isInvisible: bool = False,
        ) -> str:

        url = "https://api.ez-captcha.com/createTask"
        payload = json.dumps({
            "clientKey": self.client_key,
            "task": {
                "websiteURL": websiteURL,
                "websiteKey": websiteKey,
                "type": type,
                "isInvisible": isInvisible,
                "pageAction": pageAction
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)
        if data['errorId']:
            raise ValueError(data)
        return data['taskId']
    
    def __get_task_result(self, task_id: str) -> str:
        url = "https://api.ez-captcha.com/getTaskResult"
        payload = json.dumps({
            "clientKey": self.client_key,
            "taskId": task_id
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)
        if data['errorId']:
            raise ValueError(data)
        if data['status'] == 'processing':
            print('.', end='')
            time.sleep(3)
            return self.__get_task_result(task_id)
        elif data['status'] == 'ready': 
            return data['solution']['gRecaptchaResponse']
        else:
            raise ValueError(data)


    def cap(
            self,
            websiteURL: str, 
            websiteKey: str, 
            pageAction: str,
            type: str = 'ReCaptchaV3TaskProxyless',
            isInvisible: bool = False,
        ) -> str:
        task_id = self.__create_task(websiteURL,websiteKey,pageAction,type,isInvisible)
        result = self.__get_task_result(task_id)
        return result

    

if __name__ == '__main__':
    captcha = EzCaptchaImpl()
    res = captcha.cap(
        websiteURL='https://2dfan.com/',
        websiteKey='6LdUG0AgAAAAAAfSmLDXGMM7XKYMTItv87seZUan',
        pageAction="checkin",
        isInvisible=True,
    )
    print(res)