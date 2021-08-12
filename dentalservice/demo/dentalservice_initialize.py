import sqlite3

# initialize database 
def create_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(''' CREATE TABLE IF NOT EXISTS DENTALINFO 
                 (dentist_id integer PRIMARY KEY AUTOINCREMENT,
                  dentist_name text NOT NULL,
                  location text NOT NULL,
                  specialization text NOT NULL,
                  phone text NOT NULL); ''')
    print("Table created")            
    c.close()
    conn.commit()
    conn.close()

def inserst_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO DENTALINFO (dentist_name, location, specialization, phone) \
                                        VALUES ('dr.sharon', 'Burwood', 'Oral Surgery', '0451028117')")
    c.execute("INSERT INTO DENTALINFO (dentist_name, location, specialization, phone) \
                                        VALUES ('dr.henry', 'Randwick', 'Paediatric Dentistry', '0451123456')")                                           
    c.execute("INSERT INTO DENTALINFO (dentist_name, location, specialization, phone) \
                                        VALUES ('dr.suzy', 'Eastwood', 'Orthodontics','0451456789')") 
    print("Inserted")
    c.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db("DentalService.db")
    inserst_db("DentalService.db")

