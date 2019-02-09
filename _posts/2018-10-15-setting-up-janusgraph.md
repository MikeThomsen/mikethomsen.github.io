---
title: Setting Up JanusGraph Locally (with HBase)
---
# Setting Up JanusGraph Locally

## Setup HBase

* [Download HBase](https://www.apache.org/dyn/closer.lua/hbase/1.2.7/hbase-1.2.7-bin.tar.gz)
* `tar -zxvf hbase-1.2.7-bin.tar.gz`
* `cd hbase-1.2.7-bin`
* `./bin/hbase master` (and wait about 5-12 seconds for it to finish starting)

## Setup ElasticSearch

`docker run --name es-janus -p 9200:9200 docker.elastic.co/elasticsearch/elasticsearch:6.4.2`

## Setup JanusGraph

* [Download the latest release](https://github.com/JanusGraph/janusgraph/releases/)
* Expand archive
* Drop in the database configuration into `$JANUS_ROOT/conf/janusgraph-hbase-es.properties`
* Drop in the gremlin-server-janusgraph.yaml configuration into `$JANUS_ROOT/conf/gremlin-server-janusgraph.yaml`
* `bin/gremlin-server.sh conf/gremlin-server-janusgraph.yaml`

### Database Configuration

```
storage.backend=hbase

storage.hostname=127.0.0.1

cache.db-cache = true

cache.db-cache-clean-wait = 20

cache.db-cache-time = 180000

cache.db-cache-size = 0.5

index.search.backend=elasticsearch

index.search.hostname=127.0.0.1

gremlin.graph=org.janusgraph.core.JanusGraphFactory

host=0.0.0.0
```

### JanusGraph Gremlin Server Configuration

```
host: localhost
port: 8182
channelizer: org.apache.tinkerpop.gremlin.server.channel.HttpChannelizer
graphs: {
  graph: conf/janusgraph-hbase-es.properties}
scriptEngines: {
  gremlin-groovy: {
    plugins: { org.janusgraph.graphdb.tinkerpop.plugin.JanusGraphGremlinPlugin: {},
               org.apache.tinkerpop.gremlin.server.jsr223.GremlinServerGremlinPlugin: {},
               org.apache.tinkerpop.gremlin.tinkergraph.jsr223.TinkerGraphGremlinPlugin: {},
               org.apache.tinkerpop.gremlin.jsr223.ImportGremlinPlugin: {classImports: [java.lang.Math], methodImports: [java.lang.Math#*]},
               org.apache.tinkerpop.gremlin.jsr223.ScriptFileGremlinPlugin: {files: [scripts/janusgraph.groovy]}}}}
serializers:
  - { className: org.apache.tinkerpop.gremlin.driver.ser.GryoMessageSerializerV3d0, config: { ioRegistries: [org.janusgraph.graphdb.tinkerpop.JanusGraphIoRegistry] }}
  - { className: org.apache.tinkerpop.gremlin.driver.ser.GryoMessageSerializerV3d0, config: { serializeResultToString: true }}
  - { className: org.apache.tinkerpop.gremlin.driver.ser.GraphSONMessageSerializerV3d0, config: { ioRegistries: [org.janusgraph.graphdb.tinkerpop.JanusGraphIoRegistry] }}
metrics: {
  slf4jReporter: {enabled: true, interval: 180000}}
```

## Setup Test Data

Full steps [here](https://docs.janusgraph.org/latest/getting-started.html)

* `bin/gremlin.sh`
* ```graph = JanusGraphFactory.open('conf/janusgraph-hbase-es.properties')```
* ```GraphOfTheGodsFactory.load(graph)```

`curl -XPOST -H "Content-Type: application/json" -d '{"gremlin":"g.V().has(\"name\", \"saturn\").valueMap()"}' -v http://127.0.0.1:8182`

Should result in:

```
{
	"requestId": "9d6e4363-2d50-4971-a1aa-cb946a25e59d",
	"status": {
		"message": "",
		"code": 200,
		"attributes": {
			"@type": "g:Map",
			"@value": []
		}
	},
	"result": {
		"data": {
			"@type": "g:List",
			"@value": [{
				"@type": "g:Map",
				"@value": ["name", {
					"@type": "g:List",
					"@value": ["saturn"]
				}, "age", {
					"@type": "g:List",
					"@value": [{
						"@type": "g:Int32",
						"@value": 10000
					}]
				}]
			}]
		},
		"meta": {
			"@type": "g:Map",
			"@value": []
		}
	}
}
```