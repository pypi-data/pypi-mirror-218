#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# @Time    :  2023/6/27 14:40
# @Author  : chenxw
# @Email   : gisfanmachel@gmail.com
# @File    : pgTools.py
# @Descr   : 
# @Software: PyCharm
import psycopg2


class PgHelper:
    def __int__(self):
        pass

    @staticmethod
    def get_field_info_list_by_table(logger, conn, tablename):
        field_name_list = []
        field_type_list = []
        field_desc_list = []
        try:
            sql = "select a.attname AS \"列名\",concat_ws('',t.typname,SUBSTRING(format_type(a.atttypid,a.atttypmod) from '\(.*\)')) as \"字段类型\",d.description AS \"备注\""
            sql += " from pg_class c, pg_attribute a , pg_type t, pg_description d "
            sql += " where  c.relname = '{}' ".format(tablename)
            sql += " and a.attnum>0 "
            sql += " and a.attrelid = c.oid "
            sql += " and a.atttypid = t.oid "
            sql += " and  d.objoid=a.attrelid "
            sql += " and d.objsubid=a.attnum "
            sql += " and  d.objoid=a.attrelid "
            sql += " ORDER BY c.relname DESC,a.attnum ASC ; "
            cursor = conn.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            for record in records:
                field_name_list.append(record[0])
                field_type_list.append(record[1])
                field_desc_list.append(record[2])
            logger.info("数据表的字段查询成功")
        except Exception as exp:
            conn = None
            logger.error("数据表的字段查询失败，可能原因：{}".format(str(exp)))
        # 需要判断是否连接可视化数据库成功
        return field_name_list, field_type_list, field_desc_list

    @staticmethod
    def get_database_conection(HOST, PORT, USER, PASSWORD, DATABASE):
        # HOST = "192.168.3.191"
        # PORT = "5432"
        # USER = "postgres"
        # PASSWORD = "postgres123"
        # DATABASE = "BXJCXTDB"
        try:
            conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD,
                                    host=HOST, port=PORT)
            sql = "select count(*) from pg_tables;"
            cursor = conn.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            print("建立数据库连接成功")
        except Exception as exp:
            conn = None
            print("建立数据库连接失败，可能原因：{}".format(str(exp)))
        # 需要判断是否连接可视化数据库成功
        return conn
