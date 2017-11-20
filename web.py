import json

from aiohttp import web


# noinspection PyCompatibility
class Web(object):
    def __init__(self, proxy_handle, logger, port=None):
        self.app = web.Application()
        # self.app.router.add_get('/', self.handle)
        self.app.router.add_get('/query/{code}', self.handle)
        self.proxy_handle = proxy_handle
        self.logger = logger
        if port is None:
            self.port = 8000
        self.port = port

    async def handle(self, request):
        code = request.match_info.get('code', None)
        self.logger.debug("工号是{code}，ip是{ip_addr}".format(code=code, ip_addr=request.remote))
        try:
            if code is not None:
                text = self.proxy_handle.run(code=code, ip_addr=request.remote)
        except Exception as ex:
            text = json.dumps(str(ex))
        self.logger.debug("返回文本是{text}".format(text=text))
        # return web.Response(text=text,content_type='text/html')
        return web.json_response(text=text, content_type='text/html')

    def get_web_install(self):
        """
        运行
        web.run_app(app)
        :return:
        """
        return web.run_app(self.app, port=self.port)
