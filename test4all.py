# -*- coding: utf-8- -*-

import redis
from scrapy.utils.request import request_fingerprint
from scrapy.http.request import Request


if __name__ == '__main__':
    redis_server = redis.StrictRedis(host="192.168.1.76", port=6379, password="279279", db=1)
    test_request = Request(url="https://www.google.com?pwd=handsome&user=vander", method="GET")

    # 这是redis set集合插入操作
    # test_key = "dupefilter:request_seen"
    # test_fp = request_fingerprint(test_request)
    # if not redis_server.exists(test_key):
    #     redis_server.sadd(test_key, "test field")
    #
    # if redis_server.sismember(test_key, test_fp):
    #     print "the test request in set"
    # else:
    #     redis_server.sadd(test_key, test_fp)
    #     print "the test request not in"

    # 这是redis zset插入操作
    test_key = "sorted_set: test"
    # pairs = {
    #     "https://www.baidu.com": 0,
    #     "https://www.google.com": 0,
    #     "https://stackoverflow.com/": 0
    # }
    # redis_server.zadd(test_key, **pairs)

    pipe = redis_server.pipeline()
    pipe.multi()
    pipe.zrange(test_key, 0, 0).zremrangebyrank(test_key, 0, 0)
    results, count = pipe.execute()
    print results[0]
    print count
