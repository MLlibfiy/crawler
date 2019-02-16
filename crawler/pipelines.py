# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CommentPipeline(object):

    # 初始化函数，一般用作建立数据库连接
    def __init__(self):
        self.file = open("E:\\第二期\\大数据\\项目\\网络爬虫\\crawler\\data\\a.txt", "a")

    # 输出据处理方法
    def process_item(self, item, spider):
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

        print(line)
