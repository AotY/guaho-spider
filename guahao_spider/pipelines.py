# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os

from guahao_spider.constant import Constant


class GuahaoSpiderPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        if item is None:
            return item

        """
        if isinstance(items, CommentList):
            for item in items:
                self.save_item(item)
        else:
            self.save_item(items)
        """
        self.save_item(item)
        return item

    def save_item(self, item):
        #  logging.info('item: {}'.format(item))
        grade_dir = os.path.join(Constant.data_dir, item['hospital_grade'])
        if not os.path.exists(grade_dir):
            os.mkdir(grade_dir)

        hospital_path = os.path.join(grade_dir, item['hospital_name'] + '.txt')
        if not os.path.exists(hospital_path):
            hospital_file = open(hospital_path, 'w', encoding='utf-8')
        else:
            hospital_file = open(hospital_path, 'a', encoding='utf-8')

        hospital_file.write('%s\t%s\t%s\t%s\t%s\n' % (
            item['disease'], item['doctor'], item['date'], item['score'], item['text']))
        hospital_file.close()

    def __del__(self):
        pass
