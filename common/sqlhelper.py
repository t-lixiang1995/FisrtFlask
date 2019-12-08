"""

# 方式一
# helper = SQLHelper()
# helper.open()
# result = helper.fetchone('select * from users where name=%s and pwd = %s',[request.form.get('user'),request.form.get('pwd'),])
# helper.close()
# 方式二：
# with SQLHelper() as helper:
#     result = helper.fetchone('select * from users where name=%s and pwd = %s',[request.form.get('user'),request.form.get('pwd'),])
# if result:
#     current_app.auth_manager.login(result['name'])
#     return redirect('/index')


"""

from common.pool import POOL
import pymysql


class SQLHelper(object):
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open(self, cursor=pymysql.cursors.DictCursor):
        self.conn = POOL.connection()
        self.cursor = self.conn.cursor(cursor=cursor)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def fetchone(self, sql, params=None):
        cursor = self.cursor
        if params is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, params)
        if count > 0:
            result = cursor.fetchone()
        else:
            result = None
        return result

    def fetchall(self, sql, params=None):
        cursor = self.cursor
        if params is None:
            count=cursor.execute(sql)
        else:
            count=cursor.execute(sql,params)
        if count>0:
            result = cursor.fetchall()
        else:
            result = None
        return result

    def fetchmany(self, sql, num , params=None):
        cursor = self.cursor
        if params is None:
            count=cursor.execute(sql)
        else:
            count=cursor.execute(sql,params)
        if count>0:
            result = cursor.fetchmany(num)
        else:
            result = None
        return result

    def insertOne(self,sql,value):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        self.cursor.execute(sql,value)
        return self.__getInsertId()

    def insertMany(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self.cursor.executemany(sql, values)
        return count

    def __query(self, sql, param=None):
        if param is None:
            count = self.cursor.execute(sql)
        else:
            count = self.cursor.execute(sql, param)
        return count

    def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self.cursor.execute("SELECT @@IDENTITY AS id")
        result = self.cursor.fetchone()
        return result['id']

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    # def begintransaction(self):
    #     """
    #     @summary: 开启事务
    #     """
    #     self.conn.
    #
    # def endtransaction(self, option='commit'):
    #     """
    #     @summary: 结束事务
    #     """
    #     if option == 'commit':
    #         self.conn.commit()
    #     else:
    #         self.conn.rollback()

    def commit(self):
        self.conn.commit()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        # with SQLHelper() as obj:
        #
        #     print(obj)
        #     print('正在执行')
