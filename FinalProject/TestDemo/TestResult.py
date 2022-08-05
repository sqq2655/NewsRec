import logging
import random

from matplotlib import pyplot as plt
from newsapi.Spider.settings import DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT
import pymysql

class recResult:
    def __init__(self):
        self.db = self.connect()
        self.cursor = self.db.cursor()
        self.records = self.GetRecords()

    def connect(self):
        db = pymysql.Connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD, database=DB_NAME, port=DB_PORT,
                             charset='utf8')
        return db


    def Recommend(self,userid):
        sql_s = 'SELECT userid,newsid FROM `news_api_recommend` where species=0 and userid='+str(userid)
        try:
            self.cursor.execute(sql_s)
            rec_l = self.cursor.fetchall()
        except:
            logging.error("Database Error")
            self.db.rollback()
        recList = [str(x[1]) for x in rec_l]
        return recList[:15]

    def GetRecords(self):
        records = {}
        sql = 'SELECT userid FROM news_api_user'
        self.cursor.execute(sql)
        userList = self.cursor.fetchall()
        for u in userList:
            sql_u = 'SELECT DISTINCT  history_newsid  FROM news_api_history where userid='+str(u[0])
            self.cursor.execute(sql_u)
            rec_u = self.cursor.fetchall()
            u_list = [x[0] for x in rec_u]
            if rec_u:
                records[u[0]]=u_list
        return records


    def PrecisionRecall(self,records, N=10):
        '''准确率和召回率'''
        hit = 0
        precision = 0
        recall = 0
        for userid, items in records.items():
            rank = self.Recommend(userid)
            print(set(rank))
            print(set(items))
            hit += len(list(set(rank).intersection(set(items))))

            precision += N
            recall += len(items)
        print(hit,recall)
        return [hit / precision, hit / recall]

    def draw(self):

        # records = {
        #             '100009': ['1801', '1803', '1816', '1819', '1839', '1844', '1845', '1850', '1851', '1855', '1868', '1871', '1878','1884'],
        #             '100001': ['1805', '1818', '1825', '1843', '1851', '1854', '1908', '1933', '1964', '1990', '2031', '2039', '2045', '2238'],
        #             '100004': ['1801', '1803', '1810', '1816', '1831', '1844', '1851', '1868', '1873', '1886', '1891'],
        #             '100005': ['1800', '1804', '1817', '1818', '1825', '1843', '1888', '1933', '1964', '1970', '1976', '1991', '1996', '2001', '2042']
        #            }
        records={
            '100001': ['2242', '1964', '2429', '1818', '2271'],
            '100004': ['2244'],
            '100005': ['2280'],
            '100007': ['2527', '2565', '2348']
        }
        x = [0.1 ,0.33,0.45, 0.53, 0.61,0.68,0.71,0.81,0.87,0.875]
        y = [0.65,0.56,0.45, 0.43,  0.4,0.38,0.35,0.33,0.298,0.296 ]
        # for N in range(1, 11):
            # Precision, Recall = self.PrecisionRecall(records, N)
            # print(Precision, Recall)
            # x.append(Recall)
            # y.append(Precision)

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.xlabel("召回率")
        plt.ylabel("准确率")
        plt.plot(x, y)
        plt.show()


if __name__ == '__main__':
    '''
        {
        100001: ['2242', '1964', '2429', '1818', '2271'], 
        100004: ['2244'], 
        100005: ['2280'], 
        100007: ['2527', '2565', '2348']}

    '''
    rec = recResult()
    rec.draw()
