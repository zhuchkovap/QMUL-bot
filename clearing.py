import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
import csv
#Importing and clearing data-------------------------------------------------------------------------------------
punctuations = '''!()-[]{};:'"\,<>./?#$%^&*_~…1234567890”’“£'''
documents=list()

for i in range(0,20):
	name=str(i)+".xlsx"
	df = pd.read_excel(name, sheet_name='tweets')

	for i in df['Text']:
		i = str(i)
		no_punct = ""
		for char in i:
			if char not in punctuations:
				no_punct = no_punct + char

		no_http = ""
		for word in no_punct.split():
			if '@' and 'http' not in word:
					no_http = no_http+" "+word.lower()
		documents.append(no_http)
#Writing processed data to a file-----------------------------------------------------------------------------
alldata = dict.fromkeys(documents)
with open('dict.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in alldata.items():
       writer.writerow([key, value])