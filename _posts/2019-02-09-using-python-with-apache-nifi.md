---
title: Using Python to process data from Apache NiFi
---

The scripting bundle that ships with the standard distribution of Apache NiFi is great for developers comfortable with the Java Virtual Machine, but doesn't provide much for people that want to use something like Python 3.X to process data in their flows. While you could write a REST service in Python or some other language and call it that way, there are definite advantages to being able to call an external Python script directly from NiFi and pass the data to it.

The processor that enables this is called `ExecuteStreamCommand`. The first thing you do is write a Python script that is built around reading from `stdin` and writing all output to be sent back to NiFi to `stdout`. This is an example of one that will read a simple Excel spreadsheet, weed out bad fields and return a JSON array of its contents:

```
#!/usr/bin/python3

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
```

The sample data for it can be found [here](/post_assets/2019-02-09-executestreamprocessor/WorkBook Sample.xlsx).

Now, add an `ExecuteStreamCommand` processor to the NiFi canvas along with a `GetFile` processor and some `LogAttribute` processors and connect all of them. Configure `ExecuteStreamCommand` similar to what is shown below:

![ExecuteStreamCommand configuration](/post_assets/2019-02-09-executestreamprocessor/ExecuteStreamCommand.png)

If you load the spreadsheet with `GetFile`, you'll see output that looks like this now:

![Flow view](/post_assets/2019-02-09-executestreamprocessor/Flow View.png)

![JSON data](/post_assets/2019-02-09-executestreamprocessor/Data View.png)

Download flow template [here](/post_assets/2019-02-09-executestreamprocessor/Excel_Example.xml)