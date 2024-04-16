import json
import requests


class User: 
    session: requests.Session 

    def __init__(self, session: str) -> None:
        self.session = requests.Session() 
        self.session.headers.update({
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
            'origin': 'https://2dfan.com',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'x-csrf-token': 'cg30SzeY1l6AR/hJeSu2OEVfftVyNKuJfaNnK5cPqe0i1IFXJxO0Dpro10YE3vU27YkETUylcpZfs7CgBbOUbQ==',
            'x-requested-with': 'XMLHttpRequest',
        })
        self.session.cookies.update({
            '_project_hgc_session': session, 
        })

    class CheckinResult:
        checkins_count: int 
        serial_checkins: int 
        def __init__(self, checkins_count: int, serial_checkins: int) -> None:
            self.checkins_count = checkins_count 
            self.serial_checkins = serial_checkins 
        def from_json(json_str: str): 
            data = json.loads(json_str)
            return User.CheckinResult(**data)
        

    def checkin(self) -> CheckinResult: 
        response = self.session.post(url= 'https://2dfan.com/checkins') 
        return User.CheckinResult.from_json(response.text) 


if __name__ == '__main__': 
    json_str = '{"checkins_count":3,"serial_checkins":3}'
    cr = User.CheckinResult.from_json(json_str) 
    print(cr.__dict__)
    

