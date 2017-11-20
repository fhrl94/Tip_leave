import requests

from query import Query


class Client(Query):
    def __init__(self, code):
        self.code = code

    def run(self):
        self._get_data()
        return self._req_json
        pass

    def _get_data(self):
        req = requests.get(url='http://172.16.9.144:8080/query/{code}'.format(code=self.code))
        # print(req.url)
        # print(req.text)
        # print(req.json())
        # print(type(req.json()))
        self._req_json = req.json()
        pass

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        try:
            assert len(code) == 10 and isinstance(code, str), "输入工号错误"
        except AssertionError:
            raise UserWarning("无此工号")
        self._code = str(code)
