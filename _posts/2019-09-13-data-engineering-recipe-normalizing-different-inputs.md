---
date: 2019-09-13 08:50:00
title: "Data Engineering Recipe: Normalizing different input files with minimal code"
---

> Scenario: you get CSV files that relate to the same problem domain, but they have different headers.

One of the problems that we've faced in the past where I work is that our clients can get data that falls in the same problem domain from different sources, but they need to normalize it into a common format. It's fairly common problem, so the purpose of this post is to explain some easy strategies that will keep you from slinging too much Groovy or Python in favor of leveraging the features that NiFi has (partly due to the awesome capabilities of Apache Avro) to do a lot of the work for you.

The NiFi Record API, fundamentally, is built on Apache Avro. The structure and capabilities it has are built on and extensions to what Apache Avro gives you out of the box. One of those features is the ability to define one or more aliases for a field name. Now, aliases are one-way, which is really helpful when you're using NiFi to do ETL tasks like normalizing data. Wrong header comes in, the right field name/header goes out. It also doesn't care if you give one field one alias or several hundred. The only real restriction is that you cannot have aliases and field names colliding. That means that field names must be unique amongst each other and there cannot be any overlap between aliases that one have one alias resolving to two or more fields.

Consider these CSV files:

```
fname,lname,failed_logins
John,Smith,2
Jane,Doe,1
```

```
first_name,last_name,failed_login_attempts
John,Brown,3
Jane,Smith,2
```

This is the only Avro needed to resolve that into a single input:

```
{
	"name": "UserRecord",
	"type": "record",
	"fields": [
		{
			"name": "firstName", "type": "string", "aliases": [ "fname", "first_name" ]
		},
		{
			"name": "lastName", "type": "string", "aliases": [ "lname", "last_name" ]
		},
		{
			"name": "failedLoginCount", "type": "int", "aliases": [ "failed_logins", "failed_login_attempts" ]
		}
	]
}
```

If your data sources are following good practices like not putting multi-line headers (ex. top row is meant to categorize the real headers below it) and not repeating header names, you can almost always stop at that point. If not, you might have to write some Groovy code for `ExecuteScript` to peek at the CSV file and inspect the top few lines with a Java `Scanner` object to see what you're getting. Event that is not that difficult. For example, this is one way to handle repeated headers if they're repeated consistently (never underestimate the ability of people to get things like this amazingly inconsistent).

```
def is = session.read(flowFile)
def scanner = new Scanner(is)
def topThree = [
	scanner.nextLine(),
	scanner.nextLine(),
	scanner.nextLine()
]
def correctHeader = null
def savedLines = []
topThree.each { line ->
	if (correctHeader) {
		savedLines << line
		return
	}

	line?.with {
		def parts = it.split(",")
		if (parts.find("SOME_HEADER_FIELD")) {
			//Found likely header line
			def duplicates = []
			def headerLine = it
			parts.each { part ->
				if (parts.findAll { it == part }.size() > 1) {
					duplicates << part
				}
			}
			if (duplicates) {
				def handledDuplicates = [:]
				def newHeaderTokens = []
				parts.each { part ->
					def newToken = part
					if ((part in duplicates) && !(part in handledDuplicates.keySet())) {
						handledDuplicates[part] = 2
					} else if ((part in duplicates) && (part in handledDuplicates.keySet())) {
						newToken = "${part}_${handledDuplicates[part]}"
						handledDuplicates[part] = handledDuplicates[part] + 1
					}

					newHeaderTokens << newToken
				}
				headerLine = newHeaderTokens.join(",")
			}

			correctHeader = headerLine
		}
	}
}

while (scanner.hasNextLine()) {
	savedLines << scanner.nextLine()
}
//Finish processing
```