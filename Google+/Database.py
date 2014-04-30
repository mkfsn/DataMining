#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= ' 4月 30, 2014 '
__author__= 'mkfsn'

import sqlite3

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

def test():
    sqlite = SQLite('./test.sqlite3')
    sqlite.insert("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

if __name__ == '__main__':
    test()
