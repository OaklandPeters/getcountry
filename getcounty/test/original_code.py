from mmap import mmap, ACCESS_READ
from xlrd import open_workbook, cellname, empty_cell
import os, sys, inspect

from pyzipcode import ZipCodeDatabase

fil = '/Users/pnichols/Desktop/current/dummy_data.xls'

wb = open_workbook(fil)

# for s in wb.sheets():
# 	print 'Sheet: ', s.name
# 	print "number of rows: {}".format(s.nrows)
# 	for row in range(8, s.nrows):
# 		values = []
# 		for col in range(s.ncols):
# 			values.append(str(s.cell(row, col).value))
# 		print ','.join(values)

sheet = wb.sheet_by_index(0)

city_index = 8
county_index = 9
state_index = 10
rows_with_missing_counties = []

def get_cell_value(row_index, col_index):
	return sheet.cell(row_index, col_index).value

for row_index in range(7, sheet.nrows):
	if sheet.cell(row_index, county_index).value == empty_cell.value:
		city = get_cell_value(row_index, city_index)
		state = get_cell_value(row_index, state_index)
		rows_with_missing_counties.append((row_index, city, state))

# print rows_with_missing_counties
zcdb = ZipCodeDatabase()

no_zip = []
locations_with_zip = []

# for location in rows_with_missing_counties:
# 	zipc = zcdb.find_zip(city=location[1], state=location[2])
# 	if zipc:
# 		locations_with_zip.append(location)
# 	else:
# 		no_zip.append(location)

zipc = zcdb.find_zip(city="Saginaw", state="MI")
print [z.zip for z in zipc]

print no_zip[:5]
print len(no_zip)
print len(locations_with_zip)