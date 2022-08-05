import numpy as np
import datetime
import logging
import os
from logging.handlers import TimedRotatingFileHandler

import pymysql

from Spider.settings import DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)-7s - %(message)s')


log_file_handler = TimedRotatingFileHandler(filename="Recommend/recommend/rlg.log",
                                            when="S", interval=10,
                                            backupCount=20)
log_file_handler.setFormatter(formatter)


logger.addHandler(log_file_handler)

class NewsRecommend:
    def __init__(self, file):
        self.file = file
        self.db = self.connect()
        self.cursor = self.db.cursor()
        self.user_dict = self.loadDBData()
        self.news_tags = self.loadFileData()
        self.result = self.getRecResult()

    def connect(self):

        db = pymysql.Connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD, database=DB_NAME, port=DB_PORT,
                             charset='utf8')
        return db

    def loadDBData(self):

        logging.info("从数据库获取数据")
        sql_s = 'select userid,tags from news_api_user'
        try:
            self.cursor.execute(sql_s)
            message = self.cursor.fetchall()
        except:
            logging.error("Database Error")
            self.db.rollback()
        return message


    def loadFileData(self):

        print("开始加载文件数据：%s" % self.file)
        news_tags = dict()
        for line in open(self.file, "r", encoding="utf-8").readlines():
            try:
                newid, newtags = line.strip().split("\t")
                news_tags[newid] = newtags
                logger.info("Loading：{}".format(newtags))
            except:
                logger.info("读取分词数据过程中出现错误，错误行为：{}".format(line))
                pass
        return news_tags

    def cos_Sim(self,s1,s2):
        list_all = s1 + s2
        v1 = np.zeros(len(list_all))
        v2 = np.zeros(len(list_all))
        for i in range(len(list_all)):
            if list_all[i] in s1:
                v1[i] += 1
            if list_all[i] in s2:
                v2[i] += 1
        sim = np.dot(v1, v2) / np.sqrt(np.dot(v1, v1) * np.dot(v2, v2))
        # print(sim)
        return sim

    def getRecResult(self):

        news_cor_list = list()
        # 取出user的标签“user[1]”
        for user in self.user_dict:
            # 取出news的标签self。news_tags[newsid]
            usertags = list(set(user[1].split(",")))
            count = 0
            for newsid in self.news_tags:
                newstags = list(set(self.news_tags[newsid].split(",")))
                # cor = (len(usertags & newstags) / len(usertags | newstags))
                cor = self.cos_Sim(usertags,newstags)
                if cor > 0.00 and count < 20:
                    count += 1
                    news_cor_list.append([user[0], int(newsid), float(format(cor, ".3f"))])
                    logger.info("news_cor_list:{}".format(news_cor_list))
        return news_cor_list

    def writeToMySQL(self):
        '''
           将推荐结果写入数据库
        '''
        logging.info("将数据写入数据库...")
        for row in self.result:
            time = datetime.datetime.now().strftime("%Y-%m-%d")
            sql_i = 'insert into news_api_recommend(userid, newsid, hadread, cor, species, time) ' \
                    'values (%d, %d, 0, %.3f, 0, \'%s\') on DUPLICATE KEY UPDATE cor=%.3f, species=0' % \
                    (int(row[0]), int(row[1]), float(row[2]), time,float(row[2]))
            try:
                self.cursor.execute(sql_i)
                self.db.commit()
            except:
                logger.error("rollback:{}".format(row))
                self.db.rollback()



def beginNewsRecommendByTags():
    original_data_path = "Recommend/data/keywords/"
    files = os.listdir(original_data_path)
    for file in files:
        cor = NewsRecommend(original_data_path + file)
        cor.writeToMySQL()
    print("\n推荐内容数据写入完成....")