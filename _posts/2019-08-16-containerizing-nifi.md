---
title: Containerizing NiFi ETL processes
---

## Disclaimer

The preferred approach to managing NiFi in most cases is through the [NiFi Registry](https://nifi.apache.org/registry.html). It's an awesome tool that puts a lot of really powerful change management tools into your hands for developing, snapshotting and promoting flows between environments. The purpose of this blog post isn't to recommend an official alternative to that, but to give you an idea of how you can directly containerize a flow for when that makes sense (which is probably a lot rarer than the official, preferred approach to managing NiFi flows!)

## Now then...

When you build a NiFi flow, it gets stored in a file called `flow.xml.gz`. Think of that file as the main storage area for the state of what you see on the canvas. While there is an in-memory representation, `flow.xml.gz` is the official backup that allows you to start back up after a restart. This is the first file that you need to backup and copy over to a container if you want a dockerized NiFi to be able to pick up the exact state of your flow and go without any configuration on your part.

Any custom NAR files, Python scripts, etc. will need to be factored in. The following is an example project structure that a DevOps team could use to manage this:

* $PROJECT_ROOT
  * Dockerfile
  * flow.xml.gz
  * custom-nar-1.0.0.nar
  * our-python-package.tar.gz
  * build.sh

The `Dockerfile` would look something like this:

```
FROM apache/nifi:1.9.2

COPY flow.xml.gz /opt/nifi/nifi-${NIFI_VERSION}/conf
COPY custom-nar-1.0.0.nar /opt/nifi/nifi-${NIFI_VERSION}/lib
COPY our-python-package.tar.gz /tmp/our-python-package.tar.gz
RUN pip install /tmp/our-python-package.tar.gz
```

Then that can be built using the command `docker build -t ourcompany/nifi:flow_name_here-1.0 .`

As I said, there aren't many situations where this approach is better than the NiFi Registry. However, there are a few areas where it can be a lot better and more efficient:

1. Quickly rebuilding a shared development environment.
2. Working with closed networks in production where synchronizing with a development and integration version of the NiFi Registry is impossible for security reasons.
3. Demos and simulating another environment.

The third one can be a very interesting use of NiFi. I spent a few months on a project that used NiFi to generate a large volume of test data and pipe it out to different queues and outputs ranging from Kafka, to pushing it out over raw sockets (don't ask). The custom bundle we created on that project was the inspiration for [my data generation bundle](https://github.com/MikeThomsen/nifi-datageneration-bundle).