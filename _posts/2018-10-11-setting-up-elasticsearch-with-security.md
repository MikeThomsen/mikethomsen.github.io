---
date: 2018-10-11 08:47:00
---

# Cheatsheet for Document-Level Security

## Docker Compose

```
version: "3"
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:6.4.2
    container_name: elasticsearch
    ports:
      - 9200:9200
      - 9300:9300
    environment:
      - "discovery.type=single-node"
      - "xpack.security.enabled=true"
  kibana:
    image: docker.elastic.co/kibana/kibana:6.4.2
    container_name: kibana
    environment:
      - "elasticsearch.username=elastic"
      - "elasticsearch.password=changeme"
    ports:
      - 5601:5601
    links:
      - elasticsearch
    volumes:
      - ./kibana.yml:/usr/share/kibana/config/kibana.yml:ro

```

## Setup Passwords

`docker exec -it elasticsearch bin/elasticsearch-setup-passwords interactive`

Set each one to `changeme`.

## Create Test Index

```
PUT documents
{
  "mappings": {
    "document": {
      "properties": {
        "category": {
          "type": "keyword"
        },
        "document_id": {
          "type": "keyword"
        },
        "title": {
          "type": "text"
        }
      }
    }
  }
}
```

## Create User Roles

```
POST /_xpack/security/role/restricted_role
{
  "indices": [
    {
      "names": [ "documents" ],
      "privileges": [ "read" ],
      "query": "{\"match\": {\"category\": \"restricted\"}}"
    }
  ]
}
```

```
POST /_xpack/security/role/unrestricted_role
{
  "indices" : [
    {
      "names" : [ "documents" ],
      "privileges" : [ "read" ],
      "query": "{\"bool\": {\"must_not\": [ { \"match\": { \"category\": \"restricted\"}} ] } }"
    }
  ]
}
```

Create two users in Kibana as `elastic` user:

* unrestricted_user
  * Roles: `kibana_user`, `restricted_role`, `unrestricted_role`
* restricted_user
  * Roles: `kibana_user`, `restricted_role`


## Add Sample Data

```
POST documents/document/1
{
  "category": "restricted",
  "document_id": "ABCDEFG",
  "title": "Hello, world"
}
```

```
POST documents/document/2
{
  "category": "unrestricted",
  "document_id": "IJKLMN",
  "title": "Goodbye, cruel world"
}
```

```
POST documents/document/3
{
  "category": "sensitive",
  "document_id": "OPQRS",
  "title": "Third category document"
}
```

## Testing

```
GET documents/_search
{
  "query": {
    "match_all": {}
  }
}
```

### Expected Results For Unrestricted User

```
{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": 3,
    "max_score": 1,
    "hits": [
      {
        "_index": "documents",
        "_type": "document",
        "_id": "2",
        "_score": 1,
        "_source": {
          "category": "unrestricted",
          "document_id": "IJKLMN",
          "title": "Goodbye, cruel world"
        }
      },
      {
        "_index": "documents",
        "_type": "document",
        "_id": "1",
        "_score": 1,
        "_source": {
          "category": "restricted",
          "document_id": "ABCDEFG",
          "title": "Hello, world"
        }
      },
      {
        "_index": "documents",
        "_type": "document",
        "_id": "3",
        "_score": 1,
        "_source": {
          "category": "sbu",
          "document_id": "OPQRS",
          "title": "Third category document"
        }
      }
    ]
  }
}
```

### Expected Results for Restricted User

```
{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": 2,
    "max_score": 1,
    "hits": [
      {
        "_index": "documents",
        "_type": "document",
        "_id": "2",
        "_score": 1,
        "_source": {
          "category": "unrestricted",
          "document_id": "IJKLMN",
          "title": "Goodbye, cruel world"
        }
      },
      {
        "_index": "documents",
        "_type": "document",
        "_id": "3",
        "_score": 1,
        "_source": {
          "category": "sbu",
          "document_id": "OPQRS",
          "title": "Third category document"
        }
      }
    ]
  }
}
```