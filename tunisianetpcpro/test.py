import os
import csv
import glob
import mysql.connector
from mysql.connector import errorcode


csv_file = max(glob.iglob('*.csv'),key=os.path.getctime )
print (csv_file)

cnx = mysql.connector.connect(user='lina', password='lina@je22', host='127.0.0.1', database='testpfa')


test=open(csv_file)
print(test)
csv_data = csv.reader(test,delimiter = ',')
print(csv_data)
row_count = 0
cursor = cnx.cursor()
print(cursor)
for row in csv_data:
    if row_count != 0:
        cursor.execute('INSERT INTO product (title, reference, availability,price,mark,image,url) VALUES (%s,%s,%s,%s,%s,%s,%s)',row)
        print(row)
    row_count += 1
print("do")
cnx.commit()
cursor.close()
cnx.close()
print("closed")