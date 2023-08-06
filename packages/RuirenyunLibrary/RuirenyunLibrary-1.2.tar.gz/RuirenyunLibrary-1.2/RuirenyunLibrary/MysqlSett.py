import pymysql
import argparse


class MysqlDB(object):
    def __init__(self, host, port, username, password, database="settle_dev"):
        # 打开数据库连接
        self.connect = pymysql.connect(host=host, port=int(port), user=username, password=password, database=database,
                                       connect_timeout=30, read_timeout=30, write_timeout=30)
        # 使用cursor()方法获取操作游标
        self.cursor = self.connect.cursor()

    def close(self):
        self.cursor.close()
        self.connect.close()

    def execute(self, sql):
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.connect.commit()
        except Exception as e:
            print(str(e))
            # 发生错误时回滚
            self.connect.rollback()

    def fetchall(self):
        show = self.cursor.fetchall()
        print(f"数据库命令回显:{show}")

    def fetchone(self):
        show = self.cursor.fetchone()
        print(f"数据库命令回显:{show}")

    def fetchmany(self):
        show = self.cursor.fetchmany()
        print(f"数据库命令回显:{show}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='mysql sett tools')
    parser.add_argument('-t', dest='type', metavar='the type of the environment', action='store', help='结算平台环境类型')
    parser.add_argument('-c', dest='code', metavar='the credit code of the enterprise', action='store', help='企业税号')
    args = parser.parse_args()
    db = MysqlDB("39.108.112.37", "3306", "settle_dev", "dev#20211228#L7Lhk3")

    if "production" in args.type:
        sql = 'UPDATE `settle_dev`.`stt_en_auth_info` SET `third_info_back` = "06f2dc0c0a9a551caaa4f31a7qmnnvdi" WHERE `en_auth_id` = 367;'
        db.execute(sql)
    else:
        sql = "UPDATE `settle_dev`.`stt_en_auth_info` SET `third_info_back` = null WHERE `en_auth_id` = 367;"
        db.execute(sql)
    if args.code:
        code = str(args.code).strip()
        sql = f'UPDATE `settle_dev`.`stt_en_auth_info` SET `credit_code` = "{code}" WHERE `en_auth_id` = 229'
        db.execute(sql)

    db.close()
