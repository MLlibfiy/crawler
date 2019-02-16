import scrapy
from bs4 import BeautifulSoup
from lxml import etree
import js2xml

import re
import json

from crawler.items import Comment

class JingDongSpider(scrapy.Spider):
    name = "JingDongSpider"

    url = "https://search.jd.com/Search?keyword=%E7%94%B5%E8%84%91&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=dian%27nao&page=5"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    # 获取到搜索页面的所有商品列表
    def parse(self, response):
        items = response.xpath("//li[@class='gl-item']/@data-sku").extract()

        #for id in items:
        url = "https://item.jd.com/%s.html" % items[0]
        print(url)

        yield scrapy.Request(url=url, callback=self.parse_item_list)


    #爬取这个商品的所有型号
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


            url = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv563&productId=%s&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1" % id
            yield scrapy.Request(url=url, callback=self.parse_info)

    def parse_info(self, response):
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
            item['score']  = score
            item['nickname']  = nickname
            item['productColor']  = productColor
            item['productSize']  = productSize
            item['userClientShow']  = userClientShow
            item['userLevelName']  = userLevelName
            item['content']  = content
            item['referenceName']  = referenceName


            #返回给pipeline 处理
            yield item
