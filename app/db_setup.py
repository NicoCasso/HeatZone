from database import DatabaseManager

def initialize_database():
    db = DatabaseManager("data/zones.db")
    db.create_table_zones()
    db.create_table_passage()
    db.insert_zone(1)
    db.insert_zone(2)
    return db

if __name__ == "__main__" :
   initialize_database() 
