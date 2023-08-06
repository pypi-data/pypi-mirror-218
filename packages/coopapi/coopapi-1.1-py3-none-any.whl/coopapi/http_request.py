import logging
import uuid

import requests
from typing import Dict, Any, Union
from fastapi import Request, HTTPException, status, Response
from coopapi.enums import RequestType
import json
import pprint
from dataclasses import dataclass, field

logger = logging.getLogger('coop.http')


def _response_handler(response: Response):
    pass

def _log_send(id:str, lvl: int, method: RequestType, url, label: str = None, **kwargs):
    _lbl_txt = f"[{label}]: " if label else ""
    _txt = f"{_lbl_txt}{method.name} @URL: {url} [{id}]"
    if kwargs.get('data', None) is not None:
        _txt += f"\ndata: {pprint.pformat(kwargs['data'])}"
    if kwargs.get('json', None) is not None:
        _txt += f"\njson: {pprint.pformat(kwargs['json'])}"

    logger.log(lvl, _txt)

def _log_receive(id:str, lvl:int , method: RequestType, response: Response, url, label: str = None):
    _lbl_txt = f"[{label}]: " if label else ""

    if response.encoding is not None:
        content_txt = pprint.pformat(json.loads(response.content.decode(response.encoding)))
    else:
        content_txt = response.content

    logger.log(lvl, f"{_lbl_txt}{method.name} @URL: {url} returned [{response.status_code}] [{id}] in {int(response.elapsed.microseconds / 1000)} ms\n"
                     f"{content_txt}")


@dataclass
class RequestArgs:
    url: str
    bearer_token:str = None
    id: str = None
    data: Dict = field(default_factory=dict, init=False)
    json: str = field(default=None, init=False)

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())

    def with_payload(self, data_dict: Dict = None, json: str = None):
        if data_dict is not None:
            self.data = data_dict

        if json is not None:
            self.json = json


def request(url: str,
            method: RequestType,
            bearer_token: str = None,
            loggingLvl=logging.INFO,
            label: str = None,
            request_id: str = None,
            payload: Union[str, Dict] = None,
            ** kwargs) -> Response:
    headers = {}
    if bearer_token is not None:
        headers['Authorization'] = f"Bearer {bearer_token}"

    if request_id is None:
        request_id = str(uuid.uuid4())

    json = None
    data = None

    if payload is not None and type(payload) == str:
        data = payload
    elif payload is not None and type(payload) == dict:
        json = payload

    kwargs['json'] = json
    kwargs['data'] = data

    _log_send(id=request_id, lvl=loggingLvl, method=method, url=url, label=label, **kwargs)
    response: Response = requests.request(method=method.value, url=url, verify=True, headers=headers, **kwargs)
    _log_receive(id=request_id, lvl=loggingLvl, method=method, url=url, label=label, response=response)
    return response


def get(url: str,
        bearer_token: str = None,
        loggingLvl=logging.INFO,
        label: str = None,
        **kwargs) -> Response:
    return request(url=url,
                   method=RequestType.GET,
                   bearer_token=bearer_token,
                   loggingLvl=loggingLvl,
                   label=label,
                   **kwargs)


def post(url: str,
         payload: Union[str, Dict] = None,
         label: str = None,
         loggingLvl=logging.INFO,
         bearer_token: str = None) -> Response:
    return request(url=url,
                   method=RequestType.POST,
                   bearer_token=bearer_token,
                   loggingLvl=loggingLvl,
                   label=label,
                   payload=payload)


def put(url: str,
        payload: Union[str, Dict] = None,
        label: str = None,
        loggingLvl=logging.INFO,
        bearer_token: str = None) -> Response:
    return request(url=url,
                   method=RequestType.PUT,
                   bearer_token=bearer_token,
                   loggingLvl=loggingLvl,
                   label=label,
                   payload=payload)


def patch(url: str,
          payload: Union[str, Dict] = None,
          label: str = None,
          loggingLvl=logging.INFO,
          bearer_token: str = None) -> Response:
    return request(url=url,
                   method=RequestType.PATCH,
                   bearer_token=bearer_token,
                   loggingLvl=loggingLvl,
                   label=label,
                   payload=payload)


def delete(url: str,
           payload: Union[str, Dict] = None,
           label: str = None,
           loggingLvl=logging.INFO,
           bearer_token: str = None) -> Response:
    return request(url=url,
                   method=RequestType.DELETE,
                   bearer_token=bearer_token,
                   loggingLvl=loggingLvl,
                   label=label,
                   payload=payload)


def head(url: str,
         payload: Union[str, Dict] = None,
         label: str = None,
         loggingLvl=logging.INFO,
         bearer_token: str = None) -> Response:
    return request(url=url,
                   method=RequestType.HEAD,
                   bearer_token=bearer_token,
                   loggingLvl=loggingLvl,
                   label=label,
                   payload=payload)


def options(url: str,
            payload: Union[str, Dict] = None,
            label: str = None,
            loggingLvl=logging.INFO,
            bearer_token: str = None) -> Response:
    return request(url=url,
                   method=RequestType.OPTIONS,
                   bearer_token=bearer_token,
                   loggingLvl=loggingLvl,
                   label=label,
                   payload=payload)
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    ret = get(url='https://w3schools.com/python/demopage.htm')
    print(ret)