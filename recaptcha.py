
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
    
    def tft(
            self,
            websiteURL: str, 
            websiteKey: str
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
        print('wait cap', end='')
        result = self.__get_task_result(task_id)
        print('done')
        return result
    
    class CloudFlareTurnstileTask:
        taskId: str
        clientKey: str
        def __init__(self, taskId: str, clientKey: str):
            self.clientKey = clientKey
            self.taskId = taskId

        def create(clientKey: str, websiteURL: str, websiteKey: str):
            response = requests.post(url = "https://api.ez-captcha.com/createTask", headers={
                'Content-Type': 'application/json'
            }, data=json.dumps({
                "clientKey": clientKey,
                "task": {
                    "websiteURL": websiteURL,
                    "websiteKey": websiteKey,
                    "type": "CloudFlareTurnstileTask",
                }
            }))
            data = json.loads(response.content)
            if data['errorId']:
                raise ValueError(data)
            return EzCaptchaImpl.CloudFlareTurnstileTask(
                taskId = data['taskId'], 
                clientKey = clientKey,
            )
            

        def getResult(self) -> str:
            response = requests.post(url = "https://api.ez-captcha.com/getTaskResult", headers={
                'Content-Type': 'application/json'
            }, data=json.dumps({
                "clientKey": self.clientKey,
                "taskId": self.taskId
            }))
            data = json.loads(response.content)
            if data['errorId']:
                raise ValueError(data)
            if data['status'] == 'processing':
                print('.', end='')
                time.sleep(3)
                return self.getResult()
            elif data['status'] == 'ready': 
                print('done')
                return data['solution']['token']
            else:
                raise ValueError(data)
            
    def tft(
            self,
            websiteURL: str, 
            websiteKey: str
        ) -> str:
        cap = EzCaptchaImpl.CloudFlareTurnstileTask.create(
            clientKey=self.client_key,
            websiteURL=websiteURL,
            websiteKey=websiteKey
        )
        return cap.getResult()



    

if __name__ == '__main__':
    ez = EzCaptchaImpl()
    cap = EzCaptchaImpl.CloudFlareTurnstileTask.create(
        clientKey=ez.client_key,
        websiteURL="https://www.2dfan.com/",
        websiteKey="0x4AAAAAAAju-ZORvFgbC-Cd"
    )
    print(cap.getResult())