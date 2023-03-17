#!/usr/bin/python
# -*- coding:utf-8 -*-

import sqlite3
from dbutils.pooled_db import PooledDB


class databaseRequest:
    db = None
    cursor = None

    def __init__(self, dbpath):
        self.pool = PooledDB(
            check_same_thread=False,
            creator=sqlite3,  # 使用链接数据库的模块
            database=dbpath,  # 数据库文件db
            maxconnections=6,  # 连接池允许的最大连接数
            mincached=1,  # 初始化时，连接池中至少创建的空闲链接，0表示不创建
            maxcached=5,  # 连接池中允许最多的空闲连接数
            maxshared=3,  # 连接池中最多允许共享的连接数
            blocking=True,  # 连接池中如果没有可用的连接，当前的连接请求是否阻塞
            maxusage=None,  # 一个连接最多被重复使用的次数，None表示不限制
            ping=0,
        )

    def open(self):
        conn = self.pool.connection()
        cursor = conn.cursor()
        return conn, cursor

    def close(self, conn, cursor):
        cursor.close()
        conn.close()

    # 新增数据
    def add(self, table, params):
        sql = "INSERT INTO `" + table + "` ("
        for i in params:
            if params[i] == None:
                continue
            sql += i + ", "
        sql = sql[0:len(sql) - 2]

        sql += ") values ("
        for i in params:
            if params[i] == None:
                continue
            sql += "\'" + str(params[i]).replace('\'', '') + "\', "
        sql = sql[0:len(sql) - 2]
        sql += ")"
        try:
            result = self.execute(sql)
        except sqlite3.DatabaseError as e:
            raise Exception(e)
        return result

    def addMore(self, table, keys, values):
        try:
            sql = "INSERT INTO `" + table + "` ("
            for k in keys:
                sql += k + ", "
            sql = sql[0:len(sql) - 2]

            sql += ") values "
            limit = 0
            sqlval = ""
            for val in values:
                sqlval += '('
                for v in val:
                    sqlval += "\'" + str(v).replace('\'', '') + "\', "
                sqlval = sqlval[0:len(sqlval) - 2]
                sqlval += "),"
                limit = limit + 1
                if limit > 999 or limit >= len(values):
                    sqlval = sqlval[0:len(sqlval) - 1]
                    self.execute(sql + sqlval)
                    limit = 0
        except sqlite3.DatabaseError as e:
            raise Exception(e)
        return True

    # 编辑数据
    def edit(self, table, id, params):
        sql = "update `" + table + "`"
        sql += " set "
        for i in params:
            if params[i] == None:
                continue
            sql += i + "= \'" + str(params[i]).replace('\'', '') + '\', '
        sql = sql[0:len(sql) - 2] + " where id = " + str(id)
        result = self.execute(sql)
        return result

    # 删除数据
    def delete(self, table, id):
        sql = "delete from `" + table + "` where id = " + str(id)
        result = self.execute(sql)
        return result

    # 取单条数据
    def get(self, table, id, params='*'):
        sql = "select " + params + " from `" + table + "` where id = " + str(id) + " limit 1"
        conn, cursor = self.open()
        cursor.execute(sql)
        result = cursor.fetchone()
        self.close(conn, cursor)
        return result

    # 取多条数据
    def gets(self, table, condition, params='*', limit=0, offset=0):
        sql = "select " + params + " from `" + table + "`"
        sql = self._condition(sql, condition)
        if limit > 0:
            if offset > 1:
                sql += ' limit ' + str(offset) + ', ' + str(limit)
            else:
                sql += ' limit 0, ' + str(limit)
        try:
            conn, cursor = self.open()
            cursor.execute(sql)
            result = cursor.fetchall()
            self.close(conn, cursor)
            return result
        except:
            return False

    # 执行SQL
    def query(self, sql):
        conn, cursor = self.open()
        cursor.execute(sql)
        result = cursor.fetchone()
        self.close(conn, cursor)
        return result

    # 编辑数据
    def execute(self, sql):
        conn, cursor = self.open()
        result = cursor.execute(sql)
        conn.commit()
        self.close(conn, cursor)
        return result

    # 查询条件数据
    def _condition(self, sql, condition):
        sql_where = []
        for i in condition:
            # if isinstance(condition[i], int) or isinstance(condition[i], long):
            if isinstance(condition[i], int):
                sql_where.append('`' + i + '`' + ' = ' + str(condition[i]))
            elif condition[i][:2] in ['> ', '< ', '!=', '>=', '<=']:
                sql_where.append('`' + i + '` ' + condition[i])
            elif isinstance(condition[i], str):
                sql_where.append('`' + i + '`' + ' = \'' + condition[i] + '\'')
            elif isinstance(condition[i], list):
                tmp_sql = '`' + i + '`' + ' in ('
                for t in condition[i]:
                    tmp_sql += '\'' + t + '\', '
                tmp_sql = tmp_sql[0:len(tmp_sql) - 2] + ')'
                sql_where.append(tmp_sql)
        if len(sql_where) > 0:
            i = 0
            for l in sql_where:
                if i == 0:
                    sql += ' where '
                else:
                    sql += ' and '
                sql += l
                i += 1
        return sql


if __name__ == '__main__':
    pass
