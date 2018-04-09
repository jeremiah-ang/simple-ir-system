import os
import csv

fields = ['document_id', 'title', 'content', 'date_posted', 'court']
data_dir = './data/test/'
output_csv = './data/csv/test.csv'


date_posted = "1997-10-13 00:00:00"
court = "SG High Court"
with open (output_csv, 'w') as csvout:
	csv_writer = csv.writer(csvout, delimiter=',', quoting=csv.QUOTE_MINIMAL)
	csv_writer.writerow(fields)
	for file in os.listdir(data_dir):
		path =  os.path.join(data_dir, file)
		with open(path, 'r') as fdin:
			docid = file 
			title = fdin.readline().strip()
			fdin.seek(0)
			content = fdin.read()
			csv_writer.writerow((docid, title, content, date_posted, court))
