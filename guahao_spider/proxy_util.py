#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2019 LeonTao
#
# Distributed under terms of the MIT license.

"""
Proxy Util
- get proxy
- get all proxy
- get proxy count
- delete proxy
"""

import time
import json
import requests
import logging
from requests.compat import urljoin
from requests.exceptions import ProxyError
from guahao_spider.constant import Constant



class ProxyUtil:
    base_url = 'http://127.0.0.1:5010'

    def get_proxy(self):
        logging.info('get_proxy ...')
        count = self.get_proxy_count()
        if count == 0:
            time.sleep(60 * 1)

        get_url = urljoin(self.base_url, 'get/')
        proxy = '127.0.0.1:8787'
        retry_count = Constant.retry_count
        # get available proxy
        while retry_count > 0:
            try:
                proxy = requests.get(get_url).text
                logging.info('proxy: %s' % proxy)
                proxies = {'https': proxy}
                res = requests.get(Constant.GUAHAO_URL, proxies=proxies)
                status_code = res.status_code
                logging.info('guahao status code: %d', status_code)
                if status_code != 200:
                    self.delete_proxy(proxy)
                    retry_count -= 1
                    continue
                else:
                    return proxy
            except Exception as e:
                logging.info('proxy: {}, error: {}'.format(proxy, e))
                self.delete_proxy(proxy)
                retry_count -= 1
                continue

        if retry_count <= 0:
            return '127.0.0.1:8787'
        return proxy

    def get_all_proxy(self):
        count = self.get_proxy_count()
        if count == 0:
            time.sleep(60 * 1)

        get_all_url = urljoin(self.base_url, 'get_all/')
        return requests.get(get_all_url).text

    def get_proxy_count(self):
        logging.info('get_proxy_count ...')
        get_count_url = urljoin(self.base_url, 'get_status/')
        res_dict = json.loads(requests.get(get_count_url).text)
        count = res_dict['useful_proxy']
        logging.info('proxy count: %d' % count)
        return count

    def delete_proxy(self, proxy):
        delete_url = urljoin(self.base_url, 'delete/?proxy={}'.format(proxy))
        requests.get(delete_url)


