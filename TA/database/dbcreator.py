import sqlite3

conn = sqlite3.connect("TAdb.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE power
                  (ID INTEGER PRIMARY KEY, mRID TEXT, Date TEXT, Power REAL) 
               """)
# Committing changes and closing the connection to the database file
cursor.execute("""CREATE TABLE credit
                  (ID INTEGER PRIMARY KEY, mRID TEXT, Date TEXT, credit REAL) 
               """)
			   
cursor.execute("""CREATE TABLE XF
                  (ID INTEGER PRIMARY KEY, mRID TEXT, Date TEXT, Volt_AB REAL, Currnet_A REAL, Currnet_B REAL, Power_A REAL, Power_B REAL, Freq REAL, pf_A REAL, pf_B REAL, CaseTemp REAL, EnvTemp REAL) 
               """)
conn.commit()
conn.close()