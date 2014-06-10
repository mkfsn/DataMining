#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= ' 4月 30, 2014 '
__author__= 'mkfsn'

import json
import sqlite3
import MySQLdb
import MySQLdb.cursors

class SQLite:

    connection = None
    cursor = None

    def __init__ (self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS stocks (date text, trans text, symbol text, qty real, price real)')
        self.connection.commit()

    def insert (self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def __exit__ (self):
        self.connection.close()

class MySQL:
    DB_HOST = ""
    DB_NAME = ""
    DB_USER = ""
    DB_PASS = ""
    db = None

    def __init__(self):
        json_data = open ('mkfsn_secrets.json')
        secrets = json.load (json_data)
        self.DB_HOST = secrets['Database']['Host']
        self.DB_NAME = secrets['Database']['Name']
        self.DB_USER = secrets['Database']['Username']
        self.DB_PASS = secrets['Database']['Password']
        self.db = MySQLdb.connect ( host   = self.DB_HOST,
                                    user   = self.DB_USER,
                                    passwd = self.DB_PASS,
                                    db     = self.DB_NAME,
                                    cursorclass = MySQLdb.cursors.DictCursor)

    def friend_list(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM `Google_Friends` WHERE `Done`=0")
        self.db.commit()
        result = cursor.fetchall()
        return result

    def freiend_complete(self, userid):
        cursor = self.db.cursor()
        cursor.execute("UPDATE `Google_Friends` SET `Done`=1 WHERE id = %s",(userid,))
        self.db.commit()

    def article_save(self, posturl, userid, urls, verb, date, kind, postid):
        cursor = self.db.cursor()
        where = (posturl, userid, urls, verb, date, kind, postid)
        cursor.execute("INSERT IGNORE INTO `Google_Posts` VALUES (%s,%s,%s,%s,%s,%s,%s)", where)
        self.db.commit()

    def article_list(self):
        cursor = self.db.cursor()
        sql = """SELECT Post_ID FROM `Google_Posts` WHERE Post_ID NOT IN (SELECT Post_ID FROM `Google_Comments`)"""
        cursor.execute(sql)
        self.db.commit()
        result = cursor.fetchall()
        return result

    def comment_save(self, data):
        sql = """INSERT IGNORE INTO `Google_Comments` VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor = self.db.cursor()
        for where in data:
            cursor.execute(sql, where)
        self.db.commit()

def test():
    # sqlite = SQLite('./test.sqlite3')
    # sqlite.insert("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    db = MySQL()
    print db.friend_list()

if __name__ == '__main__':
    test()
