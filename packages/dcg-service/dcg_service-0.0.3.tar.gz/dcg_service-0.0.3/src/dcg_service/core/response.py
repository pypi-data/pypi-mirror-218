import json
from flask import request
from .exceptions import logger


class CustomResponse(object):
    def __init__(self, response):
        self.response = response

    def render(self):
        message = None
        status_code = self.response.status_code
        data = json.loads(self.response.data)

        if type(data) == dict:
            message = data.pop('message', None)
            data = data.pop('data', None) if data.get('data') else data

        if 400 <= status_code <= 499:
            message = data.copy() if not message else message
            data.clear()

        response_json = {
            "data": data,
            "message": message,
            "title": self.response.status,
            "code": self.response.status_code
        }
        self.response.data = json.dumps(response_json)
        self.log(response_json)
        return self.response

    def log(self, data):
        if self.response.status_code == 400:
            log = '[{} {} {}]--{}'.format(
                self.response.status_code, request.method,
                request.full_path, data.get('message'))
            logger.error(log)
