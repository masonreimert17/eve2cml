import sqlite3
from typing import List, Optional, Tuple

class FileMetadataDB:
    def __init__(self, db_name='./file_metadata.db'):
        self.db_name = db_name
        self.__connect_db()
        self.__create_table()

    def __connect_db(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def __create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_metadata (
            filename TEXT PRIMARY KEY,
            date_created BIGINT
        )
        ''')
        self.conn.commit()

    def insert_file_metadata(self, filename, date_created):
        self.cursor.execute('''
        INSERT INTO file_metadata (filename, date_created)
        VALUES (?, ?)
        ''', (filename, date_created))
        self.conn.commit()

    def get_file_metadata(self, filename):
        self.cursor.execute('''
        SELECT * FROM file_metadata WHERE filename = ?
        ''', (filename,))
        result = self.cursor.fetchone()
        return result

    def update_file_metadata(self, filename, date_created):
        self.cursor.execute('''
        UPDATE file_metadata
        SET date_created = ?
        WHERE filename = ?
        ''', (date_created, filename))
        self.conn.commit()

    def delete_file_metadata(self, filename):
        self.cursor.execute('''
        DELETE FROM file_metadata WHERE filename = ?
        ''', (filename,))
        self.conn.commit()
    def search_file_metadata(self, search_term: str) -> List[Tuple[str, int]]:
        search_term = f"%{search_term}%"
        self.cursor.execute('''
        SELECT * FROM file_metadata WHERE filename LIKE ?
        ''', (search_term,))
        results = self.cursor.fetchall()
        return results
    def close_db(self): 
        self.conn.close()