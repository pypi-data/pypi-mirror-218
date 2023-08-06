import json.decoder
from typing import Union
import requests


class YapiBase:
    def __init__(self,base_url):
        self.base_url = base_url
        self.session = requests.session()

    def request(self,method,url,**kwargs) -> Union[dict,list,str]:
        if not url.startswith('http'):
            url = f"{self.base_url}{url}"

        try:
            response = self.session.request(method,url,**kwargs)
        except requests.exceptions.HTTPError:
            raise Exception('连上补上服务器')
        except requests.exceptions.Timeout:
            raise Exception('请求超时')

        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            raise Exception(f'响应不是json {response.text}')

        if data.get('errcode') != 0:
            raise Exception(f'相应错误{data}')
        return data['data']

    def get(self,url,params=None) -> Union[dict,list,str]:
        return self.request('GET' ,url,params= params)

    def post(self,url,paylode) -> Union[dict,list,str]:
        return self.request('POST' ,url,json= paylode)
