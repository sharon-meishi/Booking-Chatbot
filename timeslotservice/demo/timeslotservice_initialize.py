import sqlite3

# initialize database 
def create_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(''' CREATE TABLE IF NOT EXISTS DENTAL_TIMESLOTS 
                 (timeslot integer PRIMARY KEY AUTOINCREMENT,
                  dentist_id integer NOT NULL,
                  dentist_name text NOT NULL,
                  time integer NOT NULL,
                  status text DEFAULT 'available' ); ''')
    print("Table created")            
    c.close()
    conn.commit()
    conn.close()

def inserst_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    dentist_id = [1,2,3]
    dentist_name = ['dr.sharon', 'dr.henry', 'dr.suzy']
    for did in dentist_id:
        for time in range(9,17):
            statement = f"INSERT INTO DENTAL_TIMESLOTS ('dentist_id', 'dentist_name','time') \
                            VALUES ({did}, '{dentist_name[did-1]}', {time}) "
            print(statement)
            c.execute(statement)
    print("Inserted")
    c.close()
    conn.commit()
    conn.close()

create_db('timeslot.db')
inserst_db('timeslot.db')
