import csv
import MySQLdb



db = MySQLdb.connect(host='localhost',
	user='root',
	passwd='',)

cursor = db.cursor()

sql = 'CREATE DATABASE IF NOT EXISTS mydb'
cursor.execute(sql)

sql = '''
CREATE TABLE IF NOT EXISTS `mydb`.`zcta_county` (
  `zcta5` VARCHAR(45) NULL,
  `state` VARCHAR(45) NULL,
  `county` VARCHAR(45) NULL)
ENGINE = InnoDB
'''
cursor.execute(sql)

csv_data = csv.reader(file('/Users/pnichols/Desktop/current/missing_county/zcta_county_rel_11.csv'))
next(csv_data, None)

for row in csv_data:
	cursor.execute('INSERT INTO `mydb`.`zcta_county`(zcta5, state, county)' \
		'Values("%s", "%s", "%s")', row)

db.commit()
cursor.close()
print "Done"
