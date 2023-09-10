import json
import os
# import sqlite3

# import requests

def get_file(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def load_config():
    with open(get_file('../config.json')) as f:
        return json.load(f)

# class TimeoutRequestsSession(requests.Session):
#     def request(self, *args, **kwargs):
#         kwargs.setdefault('timeout', 200)
#         return super(TimeoutRequestsSession, self).request(*args, **kwargs)


# class Database():
#     def __init__(self, file_name):
#         self.file_name = file_name
#         self.computer = "Home"
#         self.pool = None
#         self.setup()
#         self.hours_back = 7

#     def newConnection(self, autoCommit, dic=False):
#         return Connection(self,  autoCommit, dic=dic)

#     def setup(self):
#         query = """CREATE TABLE IF NOT EXISTS "recent_run"(
#                 style TEXT, 
#                 last_run TEXT NULL
#                 )"""
#         self.run_query(query, commit=True)

#     def run_query(self, query, commit=False, args=None, has_rows_result=True, headers=False, dic=True):
#         with self.newConnection(commit, dic=dic) as cur:
#             if args == None:
#                 cur.execute(query)
#             else:
#                 cur.execute(query, args)
#             if has_rows_result:
#                 if headers:
#                     return cur.fetchall(), cur.description
#                 return cur.fetchall()
            
#     def insert_recent_run(self, style):
#         query = "insert into recent_run (style, last_run) VALUES (?, datetime('now'))"

#         self.run_query(query, args=(style,), commit=True, has_rows_result=False)

#     def insert_recent_run(self, style):
#         query = "insert into recent_run (style, last_run) VALUES (?, datetime('now'))"

#         self.run_query(query, args=(style,), commit=True, has_rows_result=False)

#     def clean_up(self):
#         query = "delete from recent_run where last_run < datetime('now', '-2 days')"
#         self.run_query(query, has_rows_result=False, commit=True)

#     def is_recent_run(self, style, hours_back=None):
#         if hours_back == None:
#             hours_back = self.hours_back

#         query = """
#         select 1 from recent_run where last_run > datetime('now', '-{} hours') and style = ?
#         union all
#         select 0 limit 1""".format(hours_back)

#         return self.run_query(query, args=(style,), dic=False)[0][0] ==1


# class Connection():
#     def __init__(self, db,  autocommit, dic=False):
#         self.db= db
#         self.autocommit=autocommit
#         self.dic=dic

#     def dict_factory(self, cursor, row):
#         d = {}
#         for idx, col in enumerate(cursor.description):
#             d[col[0]] = row[idx]
#         return d

#     def __enter__(self):
#         if self.db.pool != None:
#             self.conn = self.db.pool.getconn()
#         else:
#             self.conn = conn = sqlite3.connect(get_file(self.db.file_name))

#         if self.dic:
#             self.conn.row_factory = self.dict_factory
#             self.cur = self.conn.cursor()
#         else:
#             self.cur = self.conn.cursor()
#         return self.cur

#     def __exit__(self, type, value, traceback):
#         if self.autocommit:
#             self.conn.commit()
#         self.cur.close()


#         if self.db.pool != None:
#             self.db.pool.putconn(self.conn)
#         else:
#             self.conn.close()
