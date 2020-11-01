import pymysql


class DatabaseWorker:
    def __init__(self):
        self.connection = pymysql.connect("localhost", "root", "12345678", "asanadatabase")
        self.connection.autocommit_mode = True

    def setToken(self, task_gid, sync_token):
        with self.connection.cursor() as cur:
            cur.execute("INSERT INTO  `asanasynctokens` (`TaskGid`, `SyncToken`) VALUES (%s,%s)",
                        (task_gid, sync_token))
        self.connection.commit()

    def getToken(self, task_gid):
        with self.connection.cursor() as cur:
            cur.execute("SELECT `SyncToken` From `asanasynctokens` where `taskGid`=%s", task_gid)
            res = cur.fetchone()
            if res is None:
                return None
            else:
                return res[0]

    def updateToken(self, task_gid, sync_token):
        with self.connection.cursor() as cur:
            cur.execute("Update `asanasynctokens` SET `SyncToken`=%s Where `TaskGid`=%s", (sync_token, task_gid))
        self.connection.commit()


if __name__ == '__main__':
    dw = DatabaseWorker()
    dw.setToken("11", "1rdqaczcvbszfdVz c")
    dw.updateToken("11", "new")
