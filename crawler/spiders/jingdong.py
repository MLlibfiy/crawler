import scrapy
from bs4 import BeautifulSoup
from lxml import etree
import js2xml
import re
import json
import time
from crawler.items import Comment, ItemInfo

import random


class JingDongSpider(scrapy.Spider):
    name = "JingDongSpider"

    keyword = "手机"

    url = "https://search.jd.com/Search?keyword=%E7%94%B5%E8%84%91&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=dian%27nao&page="

    def start_requests(self):

        # 爬去所有页面
        for page in range(1, 5, 2):
            url = self.url + str(page)
            yield scrapy.Request(url=url, callback=self.parse)

    # 获取到搜索页面的所有商品列表
    def parse(self, response):
        items = response.xpath("//li[@class='gl-item']/@data-sku").extract()

        for id in items:
            url = "https://item.jd.com/%s.html" % id

            # 睡一会，防止被封
            #time.sleep(random.randint(1, 3))
            yield scrapy.Request(url=url, callback=self.parse_item_list)

    # 爬取这个商品的所有型号
    def parse_item_list(self, response):
        # html --> xml 对象
        soup = BeautifulSoup(response.text, 'lxml')

        # 选择script 标签
        src = soup.select("html head script")[0].string

        # js代码  -->  xml文档对象
        src_text = js2xml.parse(src, debug=False)
        src_tree = js2xml.pretty_print(src_text)

        # xml   --->  html 文档对象
        selector = etree.HTML(src_tree)

        # 使用html xpath 查找标签

        name = selector.xpath("//property[@name='name']/string/text()")

        print(name)

        for obj in selector.xpath("//property[@name='colorSize']/array/object"):
            # @value  获取标签属性的值
            # ./   从当前标签开始寻找
            id = obj.xpath("./property/number/@value")[0]
            str = ",".join(obj.xpath("./property/string/text()"))
            # 请求产品评价

            for page in range(1, 100):



                url = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv563" \
                      "&productId=%s&score=0&sortType=5&page=%d&pageSize=10&isShadowSku=0&rid=0&fold=1" % (id, page)
                yield scrapy.Request(url=url, callback=self.parse_comment)

            # 获取商品价格和基本的信息
            url = "https://c0.3.cn/stock?skuId=%s&cat=9987,653,655&venderId=1000004123&area=1_72_2799_0" % id
            yield scrapy.Request(url=url, callback=self.parse_info)

    # 获取商品价格
    def parse_info(self, response):
        content = json.loads(response.text)
        # # 获取评价列表
        price = content['stock']['jdPrice']['p']
        id = content['stock']['realSkuId']
        StockStateName = content['stock']['StockStateName']
        vender = content['stock']['self_D']["vender"]

        item = ItemInfo()
        item["price"] = price
        item["id"] = id
        item["StockStateName"] = StockStateName
        item["vender"] = vender

        # 标记，区分多个item
        item["flag"] = "info"

        yield item

    def parse_comment(self, response):

        time.sleep(1)

        p = re.compile(r'[(](.*)[)]', re.S)  # 贪婪匹配
        r = re.findall(p, response.text)
        content = json.loads(r[0])
        # # 获取评价列表
        comments = content['comments']

        for comment in comments:
            item = Comment()

            id = comment["id"]
            score = comment["score"]
            nickname = comment["nickname"]
            productColor = comment["productColor"]
            productSize = comment["productSize"]
            userClientShow = comment["userClientShow"]
            userLevelName = comment["userLevelName"]
            content = comment["content"]
            referenceName = comment["referenceName"]

            item['id'] = id
            item['score'] = score
            item['nickname'] = nickname
            item['productColor'] = productColor
            item['productSize'] = productSize
            item['userClientShow'] = userClientShow
            item['userLevelName'] = userLevelName
            item['content'] = content
            item['referenceName'] = referenceName

            # 标记，区分多个item
            item["flag"] = "comment"

            # 返回给pipeline 处理
            yield item
