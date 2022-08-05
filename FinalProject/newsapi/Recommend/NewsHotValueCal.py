import logging
import math
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

import pymysql

from Spider.settings import DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)-7s - %(message)s')

log_file_handler = TimedRotatingFileHandler(filename="Recommend/analysis/hvg.log",
                                            when="S", interval=5,
                                            backupCount=20)
log_file_handler.setFormatter(formatter)

logger.addHandler(log_file_handler)

class CalHotValue:
    def __init__(self):
        self.db = self.connect()
        self.cursor = self.db.cursor()
        self.result = self.calHotValue()

    def connect(self):
        db = pymysql.Connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD, database=DB_NAME, port=DB_PORT,
                             charset='utf8')
        return db

    def calHotValue(self):
        '''
           计算热度值
        '''
        base_time = datetime.now()
        sql = "select news_id, category, readnum , comments, date from news_api_newsdetail"
        self.cursor.execute(sql)
        result_list = self.cursor.fetchall()
        result = list()

        for row in result_list:
            try:
                # time = row[4].replace("年", "-").replace("月", "-").replace("日", " ")
                time = row[4].replace("年", "-").replace("月", "-").replace("日", " ")
                diff = base_time - datetime.strptime(str(time), '%Y-%m-%d %H:%M')
                # row[2] 阅读数，row[3] 评论数，diff.days，过去的天数
                # 热度
                hot_value = ((math.log(1+row[2])+1.75*row[3])/ math.exp((diff.days+1)*0.05))*1000
                logger.info("HotValue:{}".format(hot_value))
                result.append((row[0], row[1], format(hot_value, ".4f")))
            except Exception:
                logger.error("转换出错")
        logger.info("新闻热度值计算完毕,返回结果 ...")
        return result

    def writeToMySQL(self):
        '''
            将热度值写入数据库
        '''
        for row in self.result:
            sql_w = "insert into news_api_newshot( news_id,category,news_hot ) " \
                    "values(%s, %s ,%s) on DUPLICATE KEY UPDATE news_hot=%s"% \
                    (row[0], row[1], row[2],row[2])
            try:
                # 执行sql语句
                self.cursor.execute(sql_w)
                # 提交到数据库执行
                self.db.commit()
            except Exception:
                logger.error("rollback:{}".format(row))
                self.db.rollback()
                # 发生错误时回滚
        logger.info("热度数据写入数据库:news.newshot")


def beginCalHotValue():
    '''
        开始计算新闻的热度值
    '''
    logger.info("开始计算新闻的热度值 ...")
    chv = CalHotValue()
    chv.writeToMySQL()
