import time

import pymysql
import re
import pytest
import json

from base.basic_log_config import logger

sql_path='hscode-test.mysql.database.azure.com'


def Conn():
    server_name = 'hscode-test.mysql.database.azure.com'
    username = 'testadmin@hscode-test'
    password = '4Ly-Zgd-HKw-Q5x'
    database_name = 'apex_sh03'

    connect = pymysql.connect(server_name, username, password, database_name,ssl={"ssl": {"ca":"./id_rsa.pem"}}) #服务器名,账户,密码,数据库名
    return connect
def con(aliOrderNo):
    try:
        connect = Conn()
        if connect:
            logger.info('数据库连接成功!')
            print("数据库连接成功!")
            cur = connect.cursor()
            SQL ="select df.aliOrderNo,notifyInfoCode,notifyEventTime,de.fileType,de.fileName,de.fileUrl,remark from ali_order_declarationfiles  as df inner join ali_order_declarationfiles_detail as de on df.aliOrderNo=de.aliOrderNo where de.aliOrderNo='{}'".format(aliOrderNo)
            cur.execute(SQL)
            sql_list=[]
            for i in cur.fetchall():
                sql_list.append(i)
            logger.info('数据库连接成功!')
            print("数据库查询sql为%s\n"%SQL)
            print("数据库查询结果为\n",sql_list)
            # SQL_delete_detail = ('delete from ali_order_declarationfiles_detail where aliOrderNo in ("2531471592252","2531471592263")')
            # cur.execute(SQL_delete_detail)
            # connect.commit()
            return sql_list



    except Exception as e:
            print("报错:",e)
if __name__=="__main__":
    con('1531471592683')