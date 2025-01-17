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
    host: str
    session: requests.Session 
    captcha_interface: CaptchaInterface

    def __init__(self, id: str, session: str, captcha_interface: CaptchaInterface, host="2dfan.com") -> None:
        self.id = id
        self.host = host
        self.session = requests.Session() 
        self.session.headers.update({
            'accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
            'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': '_ga=GA1.1.1106942088.1711578378; pop-blocked=true; _ga_RF77TZ6QMN=GS1.1.1720365165.27.1.1720366078.0.0.0; _project_hgc_session=4z0HMXrKqKm0FPT9eKC%2BEy3vAGst%2F%2BlwdigcuvHWectxz4tGlZkaMPLXM5RSL%2FqImdQkYCC0xKljeVFYd3HWldmh37WiX5xqcpw4pQYXSU4SnaKKFt9LCC5boe0AehNEQgXgASKtIFL0sj%2FOBu8A3rpMIvfFdXxjY%2FuxwRFGeS75gVo3tCcFSnOW6NKduYZ6uwFhyM872dqPRpgo6TTpakEu4VlW4kqV5bE21KfqMFZoQAvXe3qsk6QpIeS7TqqMDTOM%2Bd3llcaoLXPetfsSDgSOLiFwlfWjKpCCvh9g%2BCtpyVp34I388ZaIZsmQLU9%2BLu%2B9kf2Kh5drHP8KDbNBlRk%2BkCceTWs1fyssuPzTNjWoKzVP1IjZkLfZUe8%2F8rGgaCaNIjCczZBZbeQrg8j0CiuUlYuyfnv8JQjmMrrJTof19NjYEMiNTg%3D%3D--Xhv6nFAyw1bh9yeH--8cCB5xrV%2B%2FrGaps3sqYAvw%3D%3D',
            'origin': f'https://{host}',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': f'https://{host}/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        })
        self.session.cookies.update({
            '_project_hgc_session': session, 
            'pop-blocked': 'true',
            '_ga_RF77TZ6QMN': 'GS1.1.1737081048.3.1.1737081780.0.0.0',
            '_ga': 'GA1.1.1480083206.1736996753',
        })
        self.captcha_interface = captcha_interface

    def get_authenticity_token(self):
        # resp = self.session.get(url=f"https://2dfan.com/users/{self.id}/recheckin")
        # new_cookie = resp.cookies.get_dict('2dfan.com')
        # for key in new_cookie.keys():
        #     self.session.cookies.set(key, new_cookie[key])
        # h5 = BeautifulSoup(resp.text, 'html.parser')
        # token: str = h5.find('input', attrs={'name': 'authenticity_token'}).attrs['value']
        # return token
        # return "HiwMzbrAhxg0C5evBNa5lfMKvkls1LwuFzv1BPczqPTDzZ9LcdJV1TVbySDEjsoaUMyc7ltxs85uXE7K5BOVFQ"
        return "jr6AtXdCIKtHrwXgnGySFRcbis1b2SAs3XMGVXNvHJ-7ZLH3AUeLnYIEgL26_Th63vwfjDf9q07jp8Y4i537HA"

    class CheckinResult:
        checkins_count: int 
        serial_checkins: int 
        def __init__(self, checkins_count: int, serial_checkins: int) -> None:
            self.checkins_count = checkins_count 
            self.serial_checkins = serial_checkins 
        def from_json(json_str: str): 
            data = json.loads(json_str)
            return User.CheckinResult(**data)
        
    def create_cf_token(self, rqData: dict= {}) -> str:
        return self.captcha_interface.tft(
            websiteURL=f"https://{self.host}/",
            websiteKey="0x4AAAAAAAju-ZORvFgbC-Cd",
            rqData = {
                'mode':'',
                'metadataAction': 'checkin',
                'metadataCdata': '',
            },
        )

    def checkin(self) -> CheckinResult: 
        auth_token = self.get_authenticity_token()
        cf_token = self.create_cf_token()
        # cf_token = '0.2tG-solu7uH0o3cc0r1806kTmNO-gf2fulHBfwOVr8aPmADbNJHQAKPKYgsi_0j4C2A7fBr38rNVwEpd3eeZVRVmgw4rStC_3Ukc-B41kdroLQ1D6Q0skDg_XZJE0saXlWZauoSdvp7pZPqArhf6gBDwIO6xWdy461vb0tHMoXDhBHIeCOWlZaKLeRljLxthKjBYuohvpM2ZgbtXo70Km9scNkuRw6txGFzcNFc_FnscURzxKKiUPMJzOGaSHzClOdaJLGwDETYCmkJIvquPiqKzqMOY0RxpvhjKXaubMh0JVlbZg9rZ7EnV7y9w3izQK_K_Q-tKtvhq2QFsNEVRgTCEbBoWwbQarJchRbelaBdHUrSutcX4pyST3b3GW30vFFGuHOQ6UxyQyDhqV4dq8zmZ1t9kaoWpU8p6NgCj8eYvuUM1caRRwBdNgDKj1Gu-iCgXysZ7RB_uGbYD7vZIpa_SLi9GBoWUZ6nQUhs8k-Q8kfy4ID9r-8b7E0BZgLsOc7sca9ZnW_s9om9WEweLoYKo3U1HwVPz2y9VBp9m-qd-U1NaDSjSfokFX4GY3NJ0yW-hfN3hYhr0hb3E4Lf5W-C6bw3cVOQCycMdA4tBx0q-6AUNQZY2db28rRahZ52IGh9PgxRdBwJg-x2pGFvsBiUsL_9mKj4aJsH2QV0Jg7MEu7A7xE03mhrDCPNrc47pj-l9dvU3cV57hBYEU8OJix4_WnAx29AVydJek8brtQiPpI0gvMGdys2PPPOH6QbvZ1vRa2wf95ITKz8yfTTZzg-ywM_HItttnI-h89tAD_v0F1GROYEDydqiFNCgDdKudx5ZQC89MVyA1cpnttYG1xeWJnkpx8phhw8fR98HUQyqKhkbJWCNEARBQWHl4lUx.QdEPwXZRs574LVkBKdD72A.a3332e5a384dbb407d153353d1e562497c86c55c89ae0ea558e60ebe8fb14b25'
        response = self.session.post(url= f'https://{self.host}/checkins', headers={
            'referer': f"https://{self.host}/users/{self.id}/recheckin",
            'x-csrf-token': auth_token,
        }, data={
            # 'g-recaptcha-response-data[checkin]': self.captcha_interface.cap(
            #     websiteURL='https://2dfan.com/',
            #     websiteKey='6LdUG0AgAAAAAAfSmLDXGMM7XKYMTItv87seZUan',
            #     pageAction="checkin",
            #     isInvisible=True,
            # ),
            'cf-turnstile-response': cf_token,
            'authenticity_token': auth_token,
            'format': 'json',
            # 'g-recaptcha-response': '',
            # 'button': '',
        }) 
        if response.status_code != 200:
            raise ValueError(response.text)
        return User.CheckinResult.from_json(response.text) 
