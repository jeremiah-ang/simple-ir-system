import csv
import os
import sys

csvfile = './data/csv/dataset.csv'
outputdir = './data/test_csv/'

csv.field_size_limit(sys.maxsize)
with open(csvfile, 'r') as csvin:
	csv_reader = csv.reader(csvin, quotechar='"')
	header = csv_reader.next()

	for row in csv_reader:
		docid = row[0]
		filename = os.path.join(outputdir, docid)
		with open(filename, 'w') as fdout:
			fdout.write(",".join(row))