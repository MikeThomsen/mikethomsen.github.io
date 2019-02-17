---
title: Configuring OpenCypher and SSL on JanusGraph
---

OpenCypher is an implementation of the [Cypher Query Language](https://en.wikipedia.org/wiki/Cypher_Query_Language) for graph databases other than Neo4J. This tutorial explains how to set up OpenCypher and SSL support in [JanusGraph 0.3.1](https://github.com/JanusGraph/janusgraph/releases/tag/v0.3.1). Newer versions of JanusGraph will hopefully use the newer TinkerPop 3.3.5+ configuration options to allow you to specify keystores (JKS or P12) instead of having to split up the stores into PEM files.

The first step is obviously to download JanusGraph and explode the zip/tarball. [OpenCypher has two components](https://github.com/opencypher/cypher-for-gremlin) that are relevant for this blog post, a console plugin and a server plugin. The console plugin enables you to test Cypher queries against a JanusGraph instance instantiated within the console, and the server plugin enables the Gremlin Server to receive Cypher queries and transpile them into Gremlin code behind the scenes.

Once JanusGraph is downloaded, use its plugin loader to load the plugin. For the full documentation, go [here](https://github.com/opencypher/cypher-for-gremlin/tree/master/tinkerpop/cypher-gremlin-server-plugin). Otherwise, run this with 0.3.1 to install the server-side plugin:

```
bin/gremlin-server.sh install org.opencypher.gremlin cypher-gremlin-server-plugin 0.9.12
```

That should also update the YAML configuration file that JanusGraph bundles to include the proper updates to allow you to use the plugin.

Now install the console plugin by running `bin/gremlin.sh` to bring up the console, and then run this within the console (the `gremlin>` part signifies the gremlin console prompt; don't type it):

```
gremlin> :install org.opencypher.gremlin cypher-gremlin-console-plugin 0.9.12
```

Full documentation for that [here](https://github.com/opencypher/cypher-for-gremlin/tree/master/tinkerpop/cypher-gremlin-console-plugin).

To setup SSL, download my sample certificates [here](/post_assets/2019-02-17-configuring-opencypher-and-ssl-on-janusgraph/janus_ssl.zip). You'll need to update two files now to be able to do local testing: `gremlin-server-janusgraph.yml` and `remote-object.yml`. Add the following block to former YAML file to enable SSL on the server.

```
processors:
ssl: {
  enabled: true,
  keyFile: conf/localhost.key.pk8,
  keyCertChainFile: conf/localhost.pem,
  keyPassword: changeme,
  trustCertChainFile: conf/ca.pem
}
```

Now add this to `remote-objects.yml`:

```
connectionPool: {
  enableSsl: true,
  trustCertChainFile: conf/ca.pem
}
```

The configuration file I use for local testing uses the BerkeleyJE option for the database. It looks like this minus comments:

```
storage.backend=berkeleyje
storage.directory=../db/berkeley
gremlin.graph=org.janusgraph.core.JanusGraphFactory
```

For some reason, it seems to want ElasticSearch running when the indexer is not manually specified. That can be setup with this docker-compose example:

```
version: "3"
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:6.6.0
    container_name: elasticsearch
    hostname: elasticsearch
    ports:
      - 9200:9200
      - 9300:9300
  kibana:
    image: docker.elastic.co/kibana/kibana:6.6.0
    container_name: kibana
    environment:
      - "elasticsearch.username=elastic"
      - "elasticsearch.password=changeme"
    ports:
      - 5601:5601
    links:
      - elasticsearch
```