# -*- coding: utf-8 -*-
import sqlite3


class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect('music/base.db')
        self.cursor = self.connection.cursor()

    def select_all(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM music').fetchall()

    def select_single(self, rownum):
        with self.connection:
            return self.cursor.execute('SELECT * FROM music WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM music').fetchall()
            return len(result)

    def close(self):
        self.connection.close()
