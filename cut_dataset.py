import csv
import sys
import random

percent = 10
filename = "./data/csv/dataset.csv"
output = "./data/csv/dataset_cut{}.csv".format(percent)
csv.field_size_limit(sys.maxsize)
required = ['6807771', '4001247', '3992148', '2211154', '2748529', '4273155', '3243674', '2702938']
num = 0
with open(filename, 'r') as fdin, open(output, 'w') as fdout:
	csv_reader = csv.reader(fdin)
	csv_writer = csv.writer(fdout, quoting=csv.QUOTE_ALL)
	csv_writer.writerow(csv_reader.next())
	for row in csv_reader:
		if row[0] in required or random.randint(0,99) < percent:
			num += 1
			csv_writer.writerow(row)

print "Number of documents:", num

