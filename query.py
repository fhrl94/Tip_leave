

class Query(object):

    def _get_data(self):
        # 获取数据
        raise NotImplemented

    # def _transform(self):
    #
    #     raise NotImplemented

    def run(self):
        # 数据处理,并将数据进行返回
        raise NotImplemented

    pass

