from kafka import KafkaProducer
import hashlib

"""
数据处理

数据打入kafka

"""


class CommentPipeline(object):

    # 初始化函数，一般用作建立数据库连接
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='node1:9092,node2:9092,node3:9092')

    # 输出据处理方法
    def process_item(self, item, spider):

        if item["flag"] == 'comment':
            id = item["id"]
            productId = item["productId"]
            score = item["score"]
            nickname = item["nickname"]
            productColor = item["productColor"]
            productSize = item["productSize"]
            userClientShow = item["userClientShow"]
            userLevelName = item["userLevelName"]
            content = item["content"].replace("\n", " ")
            referenceName = item["referenceName"]

            # 用户名MD5加密
            m = hashlib.md5()
            m.update(nickname.encode("utf-8"))
            nickname = m.hexdigest().upper()

            line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
                id, productId, score, nickname, productColor, productSize, userClientShow, userLevelName, content,
                referenceName)

            # 数据打入kafka
            self.producer.send("comment", line.encode('utf-8'))
            self.producer.flush()

        if item["flag"] == "info":
            price = item["price"]
            id = item["id"]
            StockStateName = item["StockStateName"]
            vender = item["vender"]

            line = "%s\t%s\t%s\t%s" % (id, price, vender, StockStateName)

            # 数据打入kafka
            self.producer.send("info", line.encode('utf-8'))
            self.producer.flush()
