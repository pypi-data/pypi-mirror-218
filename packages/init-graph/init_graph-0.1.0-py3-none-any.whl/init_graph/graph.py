import sqlite3
import time
import os

from sqlite3 import Error
from .chapters import chapters, modules


class Graph:
    def __init__(self, chapter, parent_path):
        '''
        chapter -> kinematics, projectile ...
        parent_path -> '/Users/vaibhavblayer/10xphysics'
        '''

        self.chapter = chapter
        self.parent_path = parent_path


    def path_graph(self):
        '''
        returns the path for respective graph chapterwise
        '''

        if self.chapter in chapters[0]:
            return f'{self.parent_path}/{modules[0]}/{self.chapter}/graphs'
        elif self.chapter in chapters[1]:
            return f'{self.parent_path}/{modules[1]}/{self.chapter}/graphs'
        elif self.chapter in chapters[2]:
            return f'{self.parent_path}/{modules[2]}/{self.chapter}/graphs'
        elif self.chapter in chapters[3]:
            return f'{self.parent_path}/{modules[3]}/{self.chapter}/graphs'
        elif self.chapter in chapters[4]:
            return f'{self.parent_path}/{modules[4]}/{self.chapter}/graphs'





    def create_connection(self):
        '''
        creates connection with sqlite database at given path.
        '''

        db_file = f'{self.path_graph()}/graph.db'
        try:
            conn = sqlite3.connect(db_file)
        except:
            os.makedirs(self.path_graph())

        return conn


    def create_database(self):
        '''
        creates the database according to init params in the respective directory
        '''
        database = self.create_connection()
        try:
            database.execute(
                """ CREATE TABLE IF NOT EXISTS graph(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chapter TEXT NOT NULL,
                    date TEXT
                ); """
                )
        except Error as e:
            print(e)

        database.close()


    def get_data(self, n):
        try:
            database = self.create_connection()
            cursor = database.cursor()
            execute_statement = f'SELECT * FROM graph ORDER BY id DESC LIMIT {n};'
            output = cursor.execute(execute_statement)
            return output.fetchmany(n)
            database.close()
        except:
            self.create_database()


    def insert_data(self):
        try:
            database = self.create_connection()
            cursor = database.cursor()
            time_date = f'{int(time.strftime("%H%M%S%d%m%Y")):14}'
            execute_statement = f'INSERT INTO graph(chapter, date) VALUES("{self.chapter}", "{time_date}");'
            cursor.execute(execute_statement)
            database.commit()
            database.close()
        except Error as e:
            print(e)




