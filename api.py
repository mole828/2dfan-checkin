import json
import requests
from recaptcha import CaptchaInterface
from bs4 import BeautifulSoup

def _recap(captcha_interface: CaptchaInterface):
    return captcha_interface.cap(
        websiteURL='https://2dfan.com/',
        websiteKey='6LdUG0AgAAAAAAfSmLDXGMM7XKYMTItv87seZUan',
        pageAction="checkin",
        isInvisible=True,
    )

class User: 
    id: str
    session: requests.Session 
    captcha_interface: CaptchaInterface

    def __init__(self, id: str, session: str, captcha_interface: CaptchaInterface) -> None:
        self.id = id
        self.session = requests.Session() 
        self.session.headers.update({
            'accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
            'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': '_ga=GA1.1.1106942088.1711578378; pop-blocked=true; _ga_RF77TZ6QMN=GS1.1.1720365165.27.1.1720366078.0.0.0; _project_hgc_session=4z0HMXrKqKm0FPT9eKC%2BEy3vAGst%2F%2BlwdigcuvHWectxz4tGlZkaMPLXM5RSL%2FqImdQkYCC0xKljeVFYd3HWldmh37WiX5xqcpw4pQYXSU4SnaKKFt9LCC5boe0AehNEQgXgASKtIFL0sj%2FOBu8A3rpMIvfFdXxjY%2FuxwRFGeS75gVo3tCcFSnOW6NKduYZ6uwFhyM872dqPRpgo6TTpakEu4VlW4kqV5bE21KfqMFZoQAvXe3qsk6QpIeS7TqqMDTOM%2Bd3llcaoLXPetfsSDgSOLiFwlfWjKpCCvh9g%2BCtpyVp34I388ZaIZsmQLU9%2BLu%2B9kf2Kh5drHP8KDbNBlRk%2BkCceTWs1fyssuPzTNjWoKzVP1IjZkLfZUe8%2F8rGgaCaNIjCczZBZbeQrg8j0CiuUlYuyfnv8JQjmMrrJTof19NjYEMiNTg%3D%3D--Xhv6nFAyw1bh9yeH--8cCB5xrV%2B%2FrGaps3sqYAvw%3D%3D',
            'origin': 'https://2dfan.com',
            'priority': 'u=1, i',
            'referer': 'https://2dfan.com/',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            # 'x-csrf-token': 'HiwMzbrAhxg0C5evBNa5lfMKvkls1LwuFzv1BPczqPTDzZ9LcdJV1TVbySDEjsoaUMyc7ltxs85uXE7K5BOVFQ',
            'x-requested-with': 'XMLHttpRequest',
        })
        self.session.cookies.update({
            '_project_hgc_session': session, 
        })
        self.captcha_interface = captcha_interface

    def get_authenticity_token(self):
        resp = self.session.get(url=f"https://2dfan.com/users/{self.id}/recheckin")
        h5 = BeautifulSoup(resp.text, 'html.parser')
        token: str = h5.find('meta', attrs={'name': 'csrf-token'}).attrs['content']
        return token

    class CheckinResult:
        checkins_count: int 
        serial_checkins: int 
        def __init__(self, checkins_count: int, serial_checkins: int) -> None:
            self.checkins_count = checkins_count 
            self.serial_checkins = serial_checkins 
        def from_json(json_str: str): 
            data = json.loads(json_str)
            return User.CheckinResult(**data)
        
    def create_cf_token(self) -> str:
        self.captcha_interface.tft(
            websiteURL="https://www.2dfan.com/",
            websiteKey="0x4AAAAAAAju-ZORvFgbC-Cd",
        )

    def checkin(self) -> CheckinResult: 
        response = self.session.post(url= 'https://2dfan.com/checkins', data={
            # 'g-recaptcha-response-data[checkin]': self.captcha_interface.cap(
            #     websiteURL='https://2dfan.com/',
            #     websiteKey='6LdUG0AgAAAAAAfSmLDXGMM7XKYMTItv87seZUan',
            #     pageAction="checkin",
            #     isInvisible=True,
            # ),
            'cf-turnstile-response': self.create_cf_token(),
            'authenticity_token': self.get_authenticity_token(),
            'format': 'json',
            # 'g-recaptcha-response': '',
            'button': '',
        }) 
        return User.CheckinResult.from_json(response.text) 
