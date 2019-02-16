# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CommentPipeline(object):

    # 初始化函数，一般用作建立数据库连接
    def __init__(self):
        self.comment = open("E:\\第二期\\大数据\\项目\\网络爬虫\\crawler\\data\\comment.txt", "a", encoding="utf-8")
        self.info = open("E:\\第二期\\大数据\\项目\\网络爬虫\\crawler\\data\\info.txt", "a", encoding="utf-8")

    # 输出据处理方法
    def process_item(self, item, spider):

        if item["flag"] == 'comment':
            id = item["id"]
            score = item["score"]
            nickname = item["nickname"]
            productColor = item["productColor"]
            productSize = item["productSize"]
            userClientShow = item["userClientShow"]
            userLevelName = item["userLevelName"]
            content = item["content"]
            referenceName = item["referenceName"]

            line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
                id, score, nickname, productColor, productSize, userClientShow, userLevelName, content, referenceName)

            line = line.replace("\n", " ")

            print(line)

            self.comment.write(line)
            self.comment.write("\n")

        if item["flag"] == "info":
            price = item["price"]
            id = item["id"]
            StockStateName = item["StockStateName"]
            vender = item["vender"]

            line = "%s\t%s\t%s\t%s" % (id, price, vender, StockStateName)

            print(line)
            self.info.write(line)
            self.info.write("\n")
