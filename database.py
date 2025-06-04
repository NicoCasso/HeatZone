import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ZONES (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number_of_stops INTEGER DEFAULT 0
            );
        ''')
        self.conn.commit()

    def insert_zone(self, zone_id):
        self.cursor.execute("SELECT id FROM ZONES WHERE id=?", (zone_id,))
        if self.cursor.fetchone() is None:
            self.cursor.execute("INSERT INTO ZONES (id, number_of_stops) VALUES (?, 0)", (zone_id,))
            self.conn.commit()

    def add_element(self, id):
        self.cursor.execute('''
            UPDATE ZONES
            SET number_of_stops = number_of_stops + 1
            WHERE id = ?;
        ''', (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()




