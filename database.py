import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ZONES (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number_of_stops INTEGER DEFAULT 0
            );
        ''')
        self.connection.commit()

    def insert_zone(self):
        self.cursor.execute('''
            INSERT INTO ZONES (number_of_stops)
            VALUES (0);
        ''')
        self.connection.commit()

    def add_element(self, id):
        self.cursor.execute('''
            UPDATE ZONES
            SET number_of_stops = number_of_stops + 1
            WHERE id = ?;
        ''', (id,))
        self.connection.commit()

    def close(self):
        self.connection.close()



