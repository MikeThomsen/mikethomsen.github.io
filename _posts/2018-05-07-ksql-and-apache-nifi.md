---
date: 2018-05-07 17:47:00
title: KSQL and Apache NiFi (Part I)
---

# KSQL and Apache NiFi (Part I)

If you haven't heard about KSQL, which is Confluent's new(ish) SQL engine built on top of Apache Kafka, check out some of these links:

* [KSQL Product Page](https://www.confluent.io/product/ksql/)
* [KSQL in Action](https://www.confluent.io/blog/ksql-in-action-real-time-streaming-etl-from-oracle-transactional-data)
* [Writing Streaming Queries against Kafka using KSQL](https://docs.confluent.io/current/ksql/docs/tutorials/basics-docker.html#ksql-quickstart-docker)

So let's say you want to track a bunch of messages published by your users using a simple JSON format that looks like this:

```
{
	"username": "john.smith",
	"msg": "Hello, world"
}
```

Using KSQL, you can define a Kafka Stream from the topic `input_messages` using the following KSQL statement:

```
CREATE STREAM messages (username varchar, msg varchar) WITH (kafka_topic='input_messages', value_format='JSON');
```

For now, that doesn't do much for you beyond create a topic and let you run SQL statements like SELECT operations on it. However, suppose you want to spy on `john.smith`. You can now do this:

```
CREATE STREAM from_john_smith WITH (kafka_topic='from_john_smith', value_format='JSON') AS SELECT username, msg FROM messages WHERE username = 'john.smith';
```

Now you've chained a new stream onto the `messages` stream and KSQL will examine incoming messages in the `messages` stream and put them into the topic that is the foundation for the `from_john_smith` stream. A traditional Kafka consumer client can just subscribe to `from_john_smith` (the topic) and be blissfully ignorant of the routing details that got the message there.

This is where Apache NiFi can come in. Apache NiFi is very high throughput for processing ETL operations, particularly from sources like Kafka. However, like all ETL and data orchestration systems it can get complicated if you have to put the data routing rules in NiFi as needs change. Whhat KSQL provides here is the ability to focus in NiFi purely on the business logic of what to actually do with the data once it is pulled from the Kafka topics. The management of data flow to Kafka and within Kafka can be turned over primarily to KSQL.