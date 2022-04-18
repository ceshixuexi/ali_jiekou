import json
import time

import pytest

from base.base_analyze import analyze_file
import requests

from base.base_mysql import con, Conn
from base.basic_log_config import logger


class TestRequest:
    # 测试结束后进行数据库写入的 脏数据擦除
    def teardown(self):
        time.sleep(2)
        logger.info('测试结束后进行数据库写入的 脏数据擦除!')
        print("测试结束后进行数据库写入的 脏数据擦除")
        if Conn():
            connect = Conn()
            cur = connect.cursor()
            request_data_list = analyze_file('../data/ali_request.json')
            aliOrderNo_list=list()
            for ele in request_data_list:
                aliOrderNo_list.append(ele['request']['aliOrderNo'])
            SQL = "select df.aliOrderNo,notifyInfoCode,notifyEventTime,de.fileType,de.fileName,de.fileUrl,remark from ali_order_declarationfiles  as df inner join ali_order_declarationfiles_detail as de on df.aliOrderNo=de.aliOrderNo where de.aliOrderNo in {}".format(tuple(aliOrderNo_list))
            cur.execute(SQL)
            print("擦除前写入数据库的测试数据为{}".format(cur.fetchall()))
            SQL_delete_detail = "delete from ali_order_declarationfiles_detail where aliOrderNo in {}".format(tuple(aliOrderNo_list))
            cur.execute(SQL_delete_detail)
            connect.commit()
            SQL_delete = "delete from ali_order_declarationfiles where aliOrderNo in {}".format(tuple(aliOrderNo_list))
            cur.execute(SQL_delete)
            connect.commit()
            SQL = "select df.aliOrderNo,notifyInfoCode,notifyEventTime,de.fileType,de.fileName,de.fileUrl,remark from ali_order_declarationfiles  as df inner join ali_order_declarationfiles_detail as de on df.aliOrderNo=de.aliOrderNo where de.aliOrderNo in {}".format(
                tuple(aliOrderNo_list))
            cur.execute(SQL)
            print("擦除后数据库的测试数据为{}".format(cur.fetchall()))
    # 测试阿里->APEX的报关接口推送数据与数据库写入字段是否一致
    def test_request_declartion(self):
        request_data_list = analyze_file('../data/ali_request.json')
        data = dict()
        print("推送数据一共有{}条".format(len(request_data_list)))
        for every_data in request_data_list:
            url = every_data['url']
            data['sign'] = every_data['sign']
            data['appkey'] = every_data['appkey']
            data['request'] = json.dumps(every_data['request'])
            print("推送报关接口的数据为%s\n"%data)
            response = requests.post(url=url, json=data)
            result = response.json()['success']
            logger.info('开始新一轮测试!')
            if result:
                logger.info('接口访问成功!')
                print("接口访问成功，接口返回结果为\n", response.json())
                sql_test=con(every_data['request']['aliOrderNo'])
                for i in range(len(sql_test)):
                    print("数据库一共查到了%s条数据，这是第%s条数据的比对结果" % (len(sql_test),i+1))
                    if every_data['request']['aliOrderNo']==sql_test[i][0]:
                        logger.info('aliOrderNo相等!')
                        print("aliOrderNo相等,推送字段为%s,数据库为%s"%(every_data['request']['aliOrderNo'],sql_test[i][0]))
                    else:
                        logger.info('aliOrderNo不相等!')
                        print("aliOrderNo不相等,推送字段为%s,数据库为%s" % (every_data['request']['aliOrderNo'], sql_test[i][0]))
                    if every_data['request']['notifyInfoCode'] == sql_test[i][1]:
                        logger.info('notifyInfoCode相等!')
                        print("notifyInfoCode相等,推送字段为%s,数据库为%s" % (every_data['request']['notifyInfoCode'], sql_test[i][1]))
                    else:
                        logger.info('notifyInfoCode不相等!')
                        print("notifyInfoCode不相等,推送字段为%s,数据库为%s" % (every_data['request']['notifyInfoCode'], sql_test[i][1]))
                    if every_data['request']['notifyEventTime'] == sql_test[i][2]:
                        logger.info('notifyEventTime相等!')
                        print("notifyEventTime相等,推送字段为%s,数据库为%s" % (every_data['request']['notifyEventTime'], sql_test[i][2]))
                    else:
                        logger.info('notifyEventTime不相等!')
                        print("notifyEventTime不相等,推送字段为%s,数据库为%s" % (every_data['request']['notifyEventTime'], sql_test[i][2]))

                    if every_data['request']['content'][i]['fileType'] == sql_test[i][3]:
                        logger.info('fileType相等!')
                        print("fileType相等,推送字段为%s,数据库为%s" % (every_data['request']['content'][i]['fileType'], sql_test[i][3]))
                    else:
                        logger.info('fileType不相等!')
                        print("fileType不相等,推送字段为%s,数据库为%s" % (every_data['request']['content'][i]['fileType'], sql_test[i][3]))
                    if every_data['request']['content'][i]['fileName'] == sql_test[i][4]:
                        logger.info('fileName相等!')
                        print("fileName相等,推送字段为%s,数据库为%s" % (every_data['request']['content'][i]['fileName'], sql_test[i][4]))
                    else:
                        logger.info('fileName不相等!')
                        print("fileName不相等,推送字段为%s,数据库为%s" % (every_data['request']['content'][i]['fileName'], sql_test[i][4]))
                    if every_data['request']['content'][i]['fileUrl'] == sql_test[i][5]:
                        logger.info('fileUrl相等!')
                        print("fileUrl相等,推送字段为%s,数据库为%s" % (every_data['request']['content'][i]['fileUrl'], sql_test[i][5]))
                    else:
                        logger.info('fileUrl不相等!')
                        print("fileUrl不相等,推送字段为%s,数据库为%s" % (every_data['request']['content'][i]['fileUrl'], sql_test[i][5]))
                    if every_data['request']['content'][i]['remark'] == sql_test[i][6]:
                        logger.info('remark相等!')
                        print("remark相等,推送字段为%s,数据库为%s" % (every_data['request']['content'][i]['remark'], sql_test[i][6]))
                    else:
                        logger.info('remark不相等!')
                        print("remark不相等,推送字段为%s,数据库为%s" % (every_data['request']['content'][i]['remark'], sql_test[i][6]))
                    assert (every_data['request']['aliOrderNo'] == sql_test[i][0] and every_data['request']['notifyInfoCode'] == sql_test[i][1] and every_data['request']['notifyEventTime'] == sql_test[i][2] and every_data['request']['content'][i]['fileType'] == sql_test[i][3] and every_data['request']['content'][i]['fileName'] == sql_test[i][4]
                                and every_data['request']['content'][i]['fileName'] == sql_test[i][4] and every_data['request']['content'][i]['fileUrl'] == sql_test[i][5]
                                and every_data['request']['content'][i]['remark'] == sql_test[i][6] )
            else:

                logger.info('接口访问失败!')
                print("接口访问失败，接口返回结果为\n",response.json())

