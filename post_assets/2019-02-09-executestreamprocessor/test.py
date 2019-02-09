#!/usr/bin/python3
#!/Users/michaelthomsen/anaconda3/bin/python

from openpyxl import load_workbook
import json
import sys

wb = load_workbook(sys.stdin.buffer)
ws = wb["Sheet1"]
records = []
found_header = False
for row in ws:
	if row[0].value == "Customer":
		found_header = True
	elif found_header and row[0].value and row[1].value and row[2].value:
		temp = { 
			"Customer": row[0].value,
			"Product": row[1].value,
			"Price": row[2].value
		}
		records.append(temp)
	elif found_header and not row[0]:
		found_header = False
	
sys.stdout.write("{0}\n".format(json.dumps(records, sort_keys=True, indent=5)))

