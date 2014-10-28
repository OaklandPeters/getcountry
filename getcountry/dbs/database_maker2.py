import csv
import MySQLdb



db = MySQLdb.connect(host='localhost',
	user='root',
	passwd='',)

cursor = db.cursor()

sql = 'CREATE DATABASE IF NOT EXISTS mydb'
cursor.execute(sql)

sql = '''
CREATE TABLE IF NOT EXISTS `mydb`.`national_county` (
  `state` VARCHAR(45) NULL,
  `state_ansi` VARCHAR(45) NULL,
  `county_ansi` VARCHAR(45) NULL,
  `county_name` VARCHAR(45) NULL,
  `ansi_ci` VARCHAR(45) NULL)
ENGINE = InnoDB
'''
cursor.execute(sql)

csv_data = csv.reader(file('/Users/pnichols/Desktop/current/national_county.csv'))
next(csv_data, None)

for row in csv_data:
	cursor.execute('INSERT INTO `mydb`.`national_county`(state, state_ansi, county_ansi, county_name, ansi_ci)' \
		'Values("%s", "%s", "%s", "%s", "%s")', row)

db.commit()
cursor.close()
print "Done"
