import sqlite3
import datetime
import random
DateTime = datetime.datetime.combine(datetime.date(int(2018), int(2), int(2)), datetime.time(int(23), int(47), int(0)))
CreditList = []; dateTime = []; Credit = []; mRID = [];
for i in range(30):
    dateTime.append(str(DateTime + datetime.timedelta(days = i + 1)))
    Credit.append(random.randint(900,1150))
    mRID.append('x11')

to_db = zip(dateTime, mRID, Credit)
con = sqlite3.connect("TAdb.db")
cur = con.cursor()
cur.executemany("INSERT INTO credit (Date, mRID, credit) VALUES (?, ?, ?);", to_db)
con.commit()
con.close()
