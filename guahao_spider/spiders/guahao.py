# -*- coding: utf-8 -*-
import time
import logging
import scrapy

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from guahao_spider.items import CommentItem


class GuahaoSpider(scrapy.Spider):
    name = 'guahao'
    allowed_domains = ['guahao.com']
    login_url = 'https://www.guahao.com/user/login'
    #  start_url = 'https://www.guahao.com/hospital/all/%E5%85%A8%E5%9B%BD/all/%E4%B8%8D%E9%99%90/1/all/all/all/0/false/order/p{}'
    #  start_url = 'https://www.guahao.com/hospital/all/%E5%85%A8%E5%9B%BD/all/%E4%B8%8D%E9%99%90/all/all/all/all/0/false/7/p{}'
    #  start_url = 'https://www.guahao.com/hospital/all/%E5%85%A8%E5%9B%BD/all/%E4%B8%8D%E9%99%90/p{}'
    start_url = 'https://www.guahao.com/hospital/all/%E5%85%A8%E5%9B%BD/all/%E4%B8%8D%E9%99%90/all/33/all/all/0/false/region_sort/p{}'
    #  start_url = 'https://www.guahao.com/hospital/all/%E5%85%A8%E5%9B%BD/all/%E4%B8%8D%E9%99%90/1/all/all/all/0/false/region_sort/p{}'

    #  comment_template_url = 'https://www.guahao.com/commentslist/h-{}/1-0?pageNo=1&sign=4C57CE49D28160821F8F746581C5AE62B390D283A43F3CA2C0D00977F19B36DA3998E934AEE1CA2A839CBDA0DAF11EEC889477289C283BDA20C8D75096DB67F8&timestamp=1550890253700'
    comment_template_url = 'https://www.guahao.com/commentslist/h-{}/1-0'
    hospital_ids = [
        #  '17634310-b567-4d21-8a02-20dc15e90da5000',
        #  'dde98fc9-4183-48ee-8c84-453058fa7fe3000',
        #  '5cee04f9-4cc8-4499-a35b-6f37f2dd8a74000',
        #  '60cd2663-d69d-4f63-bc17-8618d6e5e609000',
        #  '34250b55-2a8b-474a-95e9-48150516d7a5000',
        #  'fb60b555-d22d-4229-b79c-ce9e96c82863000',
        #  '5d04ae45-d4f9-42d8-a7f2-8f25897e197d000',
        #  'a986c8d76-c720-11e1-913c-5cf9dd2e7135000',
        #  '8f113a19-eee7-47b8-9517-2ad069a2f57a000',
        #  '448f9a19-8cd2-4ccf-a152-3930ec622d9f000',
        #  '986c9800-c720-11e1-913c-5cf9dd2e7135000',
        #  '125361059609302000',
        #  '9ff45a91-1e70-4fa5-b0af-2cd51d559a91000',
        #  '08991199-fee5-48cc-b827-95eb0fdbd980000',
        #  '05ba2f6c-ec92-4a58-a6d0-31befb5474ed000',
        #  '137228411103168000',
        #  '8cda804a-9de1-48cb-b99a-08c0c3e4672d000',
        #  '6d71e862-8cbc-4b92-b7de-db272d9e53c3000',
        #  '3b79d438-b0c8-436f-8e11-2f3120be91cf000',
        #  '9869d542-c720-11e1-913c-5cf9dd2e7135000',
        #  'f981627f-aa7e-40a7-9999-895377aa2031000',
        #  '73b2d4d7-6604-471a-8f2b-4efe6bb3ce35000',
        '253aa3fe-45ea-45e0-976b-c49ee58b92fb000',
        '125336754304601000',
        '128229647014009000',
        'eba8a3ab-dcde-4538-9a7e-05c55732b5f8000',
        '125336131920301000',
        'ce1fa639-29f5-4443-a76c-2006e445206e000',
        'a37ef412-f31e-421d-a291-2521ea6f74d8000',
        'BF314EAD23323ED3E040007F01004B66000',
        '4ed5457b-721f-4d81-bcf6-b018234886b2000',
        '70e69226-fcde-4c4b-9e0b-05802890863c000',
        '08991199-fee5-48cc-b827-95eb0fdbd980000',
        '1ee21b16-9630-4e97-b4d6-daa6218b4c98000',
        '138872494057004000',
        '8888a69d-5648-4710-99dd-92ee5e2ef1fe000',
        '6d71e862-8cbc-4b92-b7de-db272d9e53c3000',
        '136400854463027000',
        'DC2F8A126980DCE4E040A8C00F012A34000',
        'd4b40a10-5f19-458a-b5e4-8273597be106000',
        '64f9440a-dda7-4219-af06-cad2815359c2000',
        'a8d8d82e-7b49-496c-8dd7-fe8989d79bb4000',
        'c1623fc3-1926-44df-9de4-1562c162add9000',
        'f226027e-7533-4834-b790-40f205e42ad5000',
        '141135273808672000'
    ]

    min_page = 1  # 21
    max_page = 15  # 91

    def __init__(self):
        self.driver = webdriver.Firefox()
        #  self.driver = webdriver.Chrome()
        self.hospital_set = set()
        pass

    def start_requests(self):
        logging.info('start_request.............')
        """This function is called before crawling starts."""

        #  yield SeleniumRequest(
        #  url=self.login_url,
        #  callback=self.start_crawl,
        #  wait_time=10,
        #  wait_until=EC.element_to_be_clickable((By.ID, 'gh'))
        #  )

        self.driver.get(self.login_url)
        element = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "gh"))
        )
        for hospital_id in self.hospital_ids:
            hospital_comment_url = self.comment_template_url.format(
                hospital_id)
            yield scrapy.Request(hospital_comment_url, cookies=self.driver.get_cookies(), callback=self.parse_comment)

        """
        for page_num in range(self.min_page, self.max_page):
            url = self.start_url.format(page_num)
            #  time.sleep(1)
            #  yield SeleniumRequest(url=url, callback=self.parse)
            yield scrapy.Request(url, cookies=self.driver.get_cookies(), callback=self.parse)

        """

        """
        first_page = self.start_url.format(self.min_page)
        yield scrapy.Request(first_page, cookies=self.driver.get_cookies(), callback=self.parse)

        """

    def parse(self, response):
        logging.info('-----------> parse, response url: %s, code: %s' %
                     (response.url, response.status))

        if response.url.find('commentslist') != -1:
            #  yield scrapy.Request(url=response.url, cookies=self.driver.get_cookies(), callback=self.parse_comment)
            yield scrapy.Request(response.url, callback=self.parse_comment)
            #  yield SeleniumRequest(url=response.url, callback=self.parse_comment)

        # hospital list
        hospital_list = response.xpath(
            '//ul[@class="hos_ul"]/li[contains(@class, "g-hospital-item")]')

        if hospital_list is not None and len(hospital_list) > 0:
            #  logging.info('len(hospital_list): ', len(hospital_list))
            for hospital in hospital_list:
                hospital_url = hospital.xpath(
                    'a[contains(@class, "cover-bg")]/@href').extract_first()
                hospital_id = hospital_url.split('/')[-1]

                hospital_comment_url = self.comment_template_url.format(
                    hospital_id)
                #  yield scrapy.Request(url=hospital_comment_url, cookies=self.driver.get_cookies(), callback=self.parse_comment)
                yield scrapy.Request(hospital_comment_url, callback=self.parse_comment)

        """

        cur_page = response.xpath(
            '//div[@class="papers"]/span[@class="current"]/text()').extract_first()
        if cur_page is None:
            cur_page = response.xpath(
                '//*[@id="g-cfg"]/div[1]/div[4]/div/form/div[1]/span/text()').extract_first()

        #  logging.info('cur_page ------------------> : %s' % cur_page)
        #  if cur_page is not None and int(cur_page) <= self.max_page:
        if cur_page is not None:
            nex_page = int(cur_page) + 1

            next_page_url = self.start_url.format(nex_page)
            logging.info('next_page_url ------------------> : %s' %
                         next_page_url)

            #  yield scrapy.Request(next_page_url, cookies=self.driver.get_cookies(), callback=self.parse)
            yield scrapy.Request(next_page_url, callback=self.parse)
        """

    def parse_comment(self, response):
        #  if response.url.find('commentslist') == -1:
            #  yield scrapy.Request(url=response.url, cookies=self.driver.get_cookies(), callback=self.parse)
        logging.info('parse_comment-----------> url: %s, code: %s' %
                     (response.url, response.status))
        # selenium get
        self.driver.get(response.url)
        try:
            next_page = self.driver.find_element_by_xpath(
                '//div[@class="g-pagination"]/div/form/div[@class="pagers"]/a[contains(@class, "next")]')
        except NoSuchElementException as e:
            return None

        items = list()

        hospital_name = str(
            self.driver.find_element_by_xpath('//h1/strong/a').text)

        hospital_grade = str(
            self.driver.find_element_by_xpath('//h1/span').text)
        hospital_grade = hospital_grade.replace(
            '\n', '').replace('\t', '').replace(' ', '')

        #  if hospital_name in self.hospital_set:
        #  return None

        #  self.hospital_set.add(hospital_name)

        while next_page is not None:
            logging.info('current url -----------------> : %s' %
                         self.driver.current_url)
            comment_lis = self.driver.find_elements_by_xpath(
                '//ul[@id="comment-list"]/li')
            for comment_li in comment_lis:
                try:
                    item = CommentItem()

                    row1_ps = comment_li.find_elements_by_xpath(
                        './/div[@class="row-1"]/p')
                    #  logging.info('len(row1_ps) -----------------> : %s' %
                    #  len(row1_ps))

                    # disease name
                    try:
                        disease = str(
                            row1_ps[0].find_element_by_xpath('.//span').text)
                        disease = disease.replace('\n', '').replace(
                            '\t', '').replace(' ', '')
                    except NoSuchElementException as e:
                        disease = '无'
                        logging.info(e)
                    #  logging.info('disease -----------------> : %s' % disease)

                    # score
                    score = str(len(row1_ps[1].find_elements_by_xpath(
                        './/span[contains(@class, "giS-star-0")]')))
                    #  logging.info('score -----------------> : %s' % score)

                    row2_divs = comment_li.find_elements_by_xpath(
                        './/div[@class="row-2"]/div')

                    # comment text
                    try:
                        text = row2_divs[0].find_element_by_xpath(
                            './/span[@class="detail"]')
                    except NoSuchElementException as e:
                        text = row2_divs[0].find_element_by_xpath(
                            './/span[@class="summary"]')
                    text = str(text.text)
                    #  logging.info('text -----------------> : %s' % text)

                    # comment date
                    date = row2_divs[1].find_element_by_xpath('.//p/span[1]')
                    date = str(date.text.split()[-1][1:-1])

                    # doctor
                    try:
                        doctor = row2_divs[1].find_element_by_xpath(
                            './/p/span[2]/a')
                        doctor = str(doctor.text)
                    except NoSuchElementException as e:
                        doctor = '佚名'
                    #  logging.info('doctor -----------------> : %s' % doctor)

                    item['hospital_name'] = hospital_name
                    item['hospital_grade'] = hospital_grade

                    item['disease'] = disease
                    item['text'] = text
                    item['score'] = score
                    item['date'] = date
                    item['doctor'] = doctor

                    items.append(item)
                except Exception as e:
                    logging.info(
                        'item error -----------------------> {}'.format(e))
                    logging.info('item: {}'.format(item))
                    continue
            try:
                next_page = self.driver.find_element_by_xpath(
                    '//div[@class="g-pagination"]/div/form/div[@class="pagers"]/a[contains(@class, "next")]')
            except NoSuchElementException as e:
                break
            next_page.click()
            time.sleep(0.35)

        logging.info('len(items) -----------------> : %d' % len(items))
        for item in items:
            yield item

        #  return None

        """
        hospital_name = response.xpath('//h1/strong/a/text()').extract_first()
        if hospital_name is None:
            hospital_name = response.xpath(
                '//*[@id="hospital-card-inner"]/div[1]/div[2]/h1/strong/a/text()').extract_first()
        if hospital_name is None:
            hospital_name = '佚名'
        hospital_name = hospital_name.replace(
            '\n', '').replace('\t', '').replace(' ', '')

        hospital_grade = response.xpath('//h1/span/text()').extract_first()
        if hospital_grade is None:
            hospital_grade = response.xpath(
                '//*[@id="hospital-card-inner"]/div[1]/div[2]/h1/span[1]').extract_first()
        if hospital_grade is None:
            hospital_grade = '无等级'
        hospital_grade = hospital_grade.replace(
            '\n', '').replace('\t', '').replace(' ', '')

        comment_lis = response.xpath('//ul[@id="comment-list"]/li')
        for comment in comment_lis:
            #  try:
            item = CommentItem()
            disease = ''
            text = ''
            score = 0
            date = ''
            doctor = ''

            row1_ps = comment.xpath('div[@class="row-1"]/p')

            # disease name
            disease = row1_ps[0].xpath('span/text()').extract_first()
            if disease is None:
                disease = '无'
            disease = disease.replace('\n', '').replace(
                '\t', '').replace(' ', '')

            # score
            score = len(row1_ps[1].xpath(
                'span[contains(@class, "giS-star-0")]'))

            row2_divs = comment.xpath('div[@class="row-2"]/div')

            # comment text
            text = row2_divs[0].xpath(
                'span[@class="detail"]/text()').extract_first()
            if text is None:
                text = row2_divs[0].xpath(
                    'span[@class="summary"]/text()').extract_first()

            # comment date
            date = row2_divs[1].xpath(
                'p/span[1]/text()').extract_first().split()[-1][1:-1]

            # doctor
            doctor = row2_divs[1].xpath(
                'a[class="name"]/text()').extract_first()
            if doctor is None:
                doctor = response.xpath(
                    '//*[@id="comment-list"]/li[1]/div[3]/div[2]/p/span[2]/a/text()').extract_first()

            item['hospital_name'] = hospital_name
            item['hospital_grade'] = hospital_grade

            item['disease'] = disease
            item['text'] = text
            item['score'] = score
            item['date'] = date
            item['doctor'] = doctor

            yield item
            #  except Exception as e:
            #  logging.info('e: {}'.format(e))
            #  continue
        """

        """
        page_no = response.xpath(
            '//form[@name="qPagerForm"]/input[@name="pageNo"]/@value').extract_first()
        if page_no is None:
            page_no = response.xpath(
                '//*[@id="g-cfg"]/div[3]/div/div/section/div[2]/div[1]/div/form/div[1]/span/text()').extract_first()

        if page_no is None:
            page_no = response.xpath(
                '//*[@id="g-cfg"]/div[3]/div/div/section/div[2]/div[1]/div/form/input[1]/@value').extract_first()

        if page_no is not None:
            logging.info('current url -----------------> : %s' % response.url)

            logging.info('current page_no --------------> : %s ' % page_no)
            next_page_no = int(page_no) + 1
            logging.info('next_page_no--------------> : %d ' % next_page_no)

            # sign
            sign = response.xpath(
                '//form[@name="qPagerForm"]/input[@name="sign"]/@value').extract_first()
            if sign is None:
                sign = response.xpath(
                    '//*[@id="g-cfg"]/div[3]/div/div/section/div[2]/div[1]/div/form/input[2]/@value').extract_first()

            logging.info('sign--------------> : %s ' % sign)

            # timestamp
            timestamp = response.xpath(
                '//form[@name="qPagerForm"]/input[@name="timestamp"]/@value').extract_first()
            if timestamp is None:
                timestamp = response.xpath(
                    '//*[@id="g-cfg"]/div[3]/div/div/section/div[2]/div[1]/div/form/input[3]/@value').extract_first()

            logging.info('timestamp--------------> : %s ' % timestamp)
            """

        """
            if response.url.find('pageNo') != -1:
                next_url = response.url.split('pageNo')[0] + 'pageNo={}&sign={}&timestamp={}'.format(next_page_no, sign, timestamp)
            else:
                next_url = response.url + '?pageNo={}&sign={}&timestamp={}'.format(next_page_no, sign, timestamp)
            """

        """
            hospital_id = response.xpath(
                '//h1/strong/a/@href').extract_first().split('/')[-1]
            logging.info('hospital_id--------------> : %s ' % hospital_id)
            hospital_comment_url = self.comment_template_url.format(hospital_id)
            #  hospital_comment_url = response.url.split('pageNo')[0]
            next_url = hospital_comment_url + \
                '?pageNo={}&sign={}&timestamp={}'.format(
                    next_page_no, sign, timestamp)

            logging.info('next_url--------------> : %s ' % next_url)
            #  self.driver.get(next_url)
            time.sleep(0.3)
            yield scrapy.Request(next_url, callback=self.parse_comment)
            """

        """
            if next_page_no < 5:
                for i in range(next_page_no, 5):
                    next_url = hospital_comment_url + \
                        '?pageNo={}&sign={}&timestamp={}'.format(
                            i, sign, timestamp)

                    logging.info(
                        'next_url--------------> : %s ' % next_url)
                    self.driver.get(next_url)
                    time.sleep(0.8)
                    yield scrapy.Request(next_url, callback=self.parse_comment)
            else:
                next_url = hospital_comment_url + \
                    '?pageNo={}&sign={}&timestamp={}'.format(
                        next_page_no, sign, timestamp)

                logging.info(
                    'next_url--------------> : %s ' % next_url)
                self.driver.get(next_url)
                time.sleep(0.8)
                yield scrapy.Request(next_url, callback=self.parse_comment)
            """

        #  if next_page_no <= 3500:
        #  yield scrapy.Request(next_url, cookies=self.driver.get_cookies(), callback=self.parse_comment)

        #  except Exception as e:
        #  logging.info('e: {}'.format(e))

        """
        # has next page
        #  self.driver.get(response.url)
        #  time.sleep(1)
        while True:
            try:
                #  next_page = self.driver.find_element_by_xpath(
                    #  '//div[@class="g-pagination"]/div/form/div[@class="pagers"]/a[contains(@class, "next")]')

                next_page = response.xpath(
                    '//div[@class="g-pagination"]/div/form/div[@class="pagers"]/a[contains(@class, "next")]')

                if next_page is None:
                    break

                # sign
                sign = response.xpath('//form[@class="qPagerForm"]/input[@name="sign"]/@value').extract_first()
                logging.info('sign--------------> : %s ' % sign)

                # timestamp
                timestamp = response.xpath('//form[@class="qPagerForm"]/input[@name="timestamp"]/@value').extract_first()
                logging.info('timestamp--------------> : %s ' % timestamp)

                #  'https://www.guahao.com/commentslist/h-af25fd28-0a0c-415a-b00a-24f1d4405b3c000/1-0?pageNo=2&sign=A069467567A3E903F777152708F9C5EEA864BE3A5888BD44E5BA169A01FB77B59C8A6ED97998CEE90DBC558C0A06B9EC2D2AFA4C1C965140D2BC2EE52C8AF64B&timestamp=1550646591738'
                next_url = response.url + 'pageNo={}sign={}&timestamp={}'.format(page_no, sign, timestamp)
                logging.info('next_url--------------> : %s ' % next_url)
                yield scrapy.Request(next_url, cookies=self.driver.get_cookies(), callback=self.parse_comment)

                page_no += 1

                #  next_page.click()
                #  # get the data and write it to scrapy items
                #  next_url = self.driver.current_url
                #  logging.info('--------------------> current_url: %s' % next_url)
                #  yield scrapy.Request(next_url, cookies=self.driver.get_cookies(), callback=self.parse_comment)
                #  yield SeleniumRequest(next_page, self.parse_comment)
            except:
                break
    """

    """
    def start_crawl(self, response):
        #  logging.info('cookie: {}'.format(self.driver.get_cookies()))
        logging.info('start_crawl.............')
        for page_num in range(self.min_page, self.max_page):
            url = self.start_url.format(page_num)
            #  time.sleep(1)
            #  yield SeleniumRequest(url=url, callback=self.parse)
            yield scrapy.Request(url, cookies=self.driver.get_cookies(), callback=self.parse)
    """

    def __del__(self):
        self.driver.close()
        self.hospital_set = None
        pass
