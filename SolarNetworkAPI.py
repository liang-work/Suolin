import json
import requests
import readFile
import platform
import uuid
import socket
from json import JSONDecodeError

class SNAPI:
    def __init__(self):
        __VERSION__ = "1.0.0"
        self.UA = f"Suolinclient/{__VERSION__} {platform.system()}/{platform.release()}"
        self.DOMAIN = readFile.LoadJson("config.json").get("APIdomain","https://api.solian.app")

    def requests_API(self,url:str,method:str="GET",params:dict={},data:dict={},headers:dict={}):
        try:
            if method == "GET":
                response = requests.get(url,params=params,headers=headers)
            elif method == "POST":
                response = requests.post(url,params=params,data=json.dumps(data),headers=headers)
            elif method == "PATCH":
                response = requests.patch(url,params=params,data=json.dumps(data),headers=headers)
            elif method == "DELETE":
                response =  requests.delete(url,params=params,headers=headers)
            else:
                return None
            if response.status_code != 200:
                return {"error":f"HTTP {response.status_code}: {response.text}"}
            return response.json()
        except JSONDecodeError:
            return {"error":"Invalid JSON response"}
        except requests.RequestException as e:
            return {"error":str(e)}
        
        
    ##login changellenge
    def create_challenge(self,username:str, platform:int=1):
        api_url = f"{self.DOMAIN}/pass/auth/challenge"
        response = self.requests_API(api_url,
                                method="POST",
                                data={
                                    "account": username,
                                    "device_id": str(uuid.getnode()),
                                    "device_name": socket.gethostname(),
                                    "platform": platform
                                },
                                headers={"User-Agent":self.UA,
                                        "Content-Type":"application/json"})
        return response

    def get_challenge_factors(self,challenge_id:str):
        api_url = f"{self.DOMAIN}/pass/auth/challenge/{challenge_id}/factors"
        response = self.requests_API(api_url,
                                method="GET",
                                headers={"User-Agent":self.UA,
                                        "Content-Type":"application/json"})
        return response
    
    def send_factor_code(self,challenge_id:str, factor:str):
        api_url = f"{self.DOMAIN}/pass/auth/challenge/{challenge_id}/factors/{factor}"
        response = self.requests_API(api_url,
                                method="POST",
                                headers={"User-Agent":self.UA,
                                        "Content-Type":"application/json"})
        return response

    def update_challenge(self,challenge_id:str, factor_id:str, password:str):
        api_url = f"{self.DOMAIN}/pass/auth/challenge/{challenge_id}"
        response = self.requests_API(api_url,
                                method="PATCH",
                                data={
                                    "factor_id": factor_id,
                                    "password": password
                                },
                                headers={"User-Agent":self.UA,
                                        "Content-Type":"application/json"})
        return response

    def exchange_token(self,challenge_id:str):
        api_url = f"{self.DOMAIN}/pass/auth/token"
        response = self.requests_API(api_url,
                                method="POST",
                                data={
                                    "grant_type": "authorization_code",
                                    "code": challenge_id
                                },
                                headers={"User-Agent":self.UA,
                                        "Content-Type":"application/json"})
        return response
    
    def post_session_token(self):
        api_url = f"{self.DOMAIN}/pass/auth/session"
        response = self.requests_API(api_url,
                                method="POST",
                                data={
                                    "device_id": str(uuid.getnode()),
                                    "device_name": socket.gethostname(),
                                    "platform": 0,
                                    "expired_at": {}
                                },
                                headers={"User-Agent":self.UA,
                                        "Content-Type":"application/json"})
        return response
##chat

##realms

##user profile

##solarnetwork drive