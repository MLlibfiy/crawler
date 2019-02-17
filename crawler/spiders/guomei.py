import scrapy
from bs4 import BeautifulSoup
from lxml import etree
import js2xml
import re
import json
import time
from crawler.items import Comment, ItemInfo


class GuoMeiSpider(scrapy.Spider):
    name = "GuoMeiSpider"

    url = "https://search.gome.com.cn/search?search_mode=normal&reWrite=true&question=%%E6%%89%%8B%%E6%%9C%%BA&searchType=goods&&page=%d&type=json&aCnt=0&reWrite=true"

    head = {
        ":authority": "search.gome.com.cn",
        ":method": "GET",
        ":path": "/search?search_mode=normal&reWrite=true&question=%E6%89%8B%E6%9C%BA&searchType=goods&&page=2&type=json&aCnt=0&reWrite=true",
        ":scheme": "https",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "z h-CN,zh;q=0.9",
        "referer": "https://search.gome.com.cn/search?question=%E6%89%8B%E6%9C%BA&searchType=goods&search_mode=normal&reWrite=true",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    def start_requests(self):


        #最多可以爬去100页
        for page in range(10):
            url = self.url%page
            yield scrapy.Request(url=url, headers=self.head, callback=self.parse)

    # 获取到搜索页面的所有商品列表
    def parse(self, response):
        jsonStr = json.loads(response.text)
        for product in jsonStr['content']['prodInfo']['products']:
            pId = product['pId']
            url = "https://item.gome.com.cn/%s.html" % pId

            # 获取这个手机的所有型号
            yield scrapy.Request(url=url, headers=self.head, callback=self.parse_item_list)

    def parse_item_list(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        src = soup.select("html head script")[1].string
        src_text = js2xml.parse(src, debug=False)
        src_tree = js2xml.pretty_print(src_text)
        selector = etree.HTML(src_tree)
        for i in selector.xpath("//property[@name = 'ColorVersion']/object"):
            # 循环所有型号
            for pid in i.xpath("./property/string/text()"):
                url = "https://item.gome.com.cn/%s.html" % pid

                # 获取这个手机的所有型号的详细信息（价格）
                yield scrapy.Request(url=url, headers=self.head, callback=self.parse_info)

                # 爬取商品评价
                for page in range(30):
                    url = "https://ss.gome.com.cn/item/v1/prdevajsonp/appraiseNew/%s/%d/all/0/3997/flag/appraise/"
                    url = url % (pid, page)
                    yield scrapy.Request(url=url, headers=self.head, callback=self.parse_comment)

    # 获取商品评价回调函数
    def parse_comment(self, response):
        jsonStr = json.loads(response.text)
        for c in jsonStr["evaList"]["Evalist"]:
            id = c["shippingGroupId"]  # 评价id
            score = c["mscore"]  # 评分
            nickname = c["loginname"]  # 登录名
            skuInfo = c["skuInfo"]  # 颜色和版本号
            # 默认分隔符空格
            skuInfos = skuInfo.split()

            productColor = skuInfos[0]  # 商品颜色
            productSize = skuInfos[1]  # 商品版本

            content = c["appraiseElSum"]  # 评价内容

            productId = c["productId"]  # 商品id
            referenceTime = c["post_time"]  # 评价时间

            item = Comment()

            item['id'] = id
            item["productId"] = productId
            item['score'] = score
            item['nickname'] = nickname
            item['productColor'] = productColor
            item['productSize'] = productSize
            item['userClientShow'] = ""
            item['userLevelName'] = ""
            item['content'] = content
            item['referenceName'] = ""
            item['referenceTime'] = referenceTime

            yield item

    # 获取商品信息回调函数
    def parse_info(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        src = soup.select("html head script")[1].string
        src_text = js2xml.parse(src, debug=False)
        src_tree = js2xml.pretty_print(src_text)
        selector = etree.HTML(src_tree)
        price = selector.xpath("//property[@name='gomePrice']/string/text()")[0]
        prdId = selector.xpath("//property[@name='prdId']/string/text()")[0]
        prdName = selector.xpath("//property[@name='prdName']/string/text()")[0]
        print(prdId)
        print(price)
        print(prdName)

        pname = response.xpath("//a[@class='name']/text()")[0].extract()

        item = ItemInfo()
        item["price"] = price
        item["id"] = prdId
        item["StockStateName"] = prdName
        item["pname"] = pname

        item["vender"] = ""

        item["website"] = "国美"

        # 标记，区分多个item
        item["flag"] = "info"

        yield item
