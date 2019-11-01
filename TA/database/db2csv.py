import sqlite3
import pandas as pd

conn = sqlite3.connect("TAdb.db")
cursor = conn.cursor()
cursor.execute('select * from XF')
while True:
    # Read the data
    df = pd.DataFrame(cursor.fetchall())
    # We are done if there are no data
    if len(df) == 0:
        break
    # Let's write to the file
    else:
        df.to_csv("/data.csv", header=False, encoding='utf-8')
conn.commit()
conn.close()
