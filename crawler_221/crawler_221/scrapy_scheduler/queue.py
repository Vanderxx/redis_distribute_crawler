# -*- coding: utf-8 -*-

import six
import simplejson as json
from scrapy.http.request import Request


class FifoQueue(object):
    def __init__(self, server, key, spider=None):
        self.server = server
        self.spider = spider
        self.key = key

    @staticmethod
    def find_func_name(obj, func):
        if obj:
            try:
                fun_self = six.get_method_self(func)
            except AttributeError:
                pass
            else:
                if fun_self is obj:
                    return six.get_method_function(func).__name__
        raise ValueError("Function %s is not a method of: %s" % (func, obj))

    def _encode_request(self, request):
        cb = request.callback
        if self.spider:
            if callable(cb):
                cb = self.find_func_name(self.spider, cb)
            else:
                cb = "%r" % cb
        else:
            cb = "parse"

        eb = request.errback
        if self.spider:
            if callable(eb):
                eb = self.find_func_name(self.spider, eb)
            else:
                eb = "%r" % eb
        else:
            eb = "errback"

        params = {
            'url': request.url,
            'callback': cb,
            'errback': eb,
            'method': request.method,
            'dont_filter': request.dont_filter,
            'meta': request.meta,
        }
        return params

    def push(self, request):
        self.server.lpush(self.key, self._encode_request(request))

    @staticmethod
    def name_get_func(obj, name):
        name = str(name)
        try:
            return getattr(obj, name)
        except AttributeError:
            raise ValueError("Method %r not found in: %s" % (name, obj))

    def _decode_request(self, params):
        cb = params['callback']
        if cb and self.spider:
            cb = self.name_get_func(self.spider, cb)

        eb = params['errback']
        if eb and self.spider:
            eb = self.name_get_func(self.spider, eb)

        return Request(
            url=params['url'],
            callback=cb,
            errback=eb,
            method=params['method'],
            dont_filter=params['dont_filter']
        )

    def pop(self):
        params = self.server.rpop(self.key)
        if params:
            params = params.replace("'", "\"").replace("False", "false").replace("True", "true")
            params = json.loads(params)
            return self._decode_request(params)
        else:
            # self.spider.logger.info("params None")
            pass

    def __len__(self):
        return self.server.llen(self.key)

    def clear(self):
        self.server.delete(self.key)


if __name__ == '__main__':
    import redis

    redis_server = redis.StrictRedis(host="192.168.1.76", port=6379, password="279279", db=1)
    key = "tasks_queue:todo_tasks"

    from scrapy.http.request import Request

    # request_inst_ = Request(url="https://book.douban.com/tag/",
    #                         dont_filter=False,
    #                         meta={"retry_times": 5})
    request_inst_ = Request(url="http://economy.caijing.com.cn/economynews",
                            dont_filter=False,
                            meta={"retry_times": 5})
    queue_inst_ = FifoQueue(redis_server, key)
    num = 5
    for _ in range(num):
        queue_inst_.push(request_inst_)
