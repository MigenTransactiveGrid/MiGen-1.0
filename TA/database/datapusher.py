import csv, sqlite3
import datetime

con = sqlite3.connect("TAdb.db")
cur = con.cursor()
def DateFormater(DateString):
    d, m, Y, I, M, S = DateString.replace(':','/').replace(' ','/').split("/")
    DateTime = str(datetime.datetime.combine(datetime.date(int(Y), int(m), int(d)), datetime.time(int(I), int(M), int(S))))
    return DateTime

with open('consumption.csv','rb') as f: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(f, delimiter=',') # comma is default delimiter
    header = dr.fieldnames
    line = next(dr)
    j = 0
    to_db = [( DateFormater(i['Date'] + ' ' + i['Time']), i['mRID'], float(i['power'])*1000) for i in dr]

cur.executemany("INSERT INTO power (Date, mRID, Power) VALUES (?, ?, ?);", to_db)
con.commit()
con.close()
