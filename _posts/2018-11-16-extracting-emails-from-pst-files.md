---
title: Extracting emails from PST files with Apache NiFi
---

Why would you want to use NiFi to rip into Outlook PST files? Many reasons, ranging from helping with corporate legal compliance to forensics examinations. Perhaps even just to move email archives off the cloud and into an ElasticSearch cluster that is run by the local IT department to save money when really old emails need to be researched or recovered.

I tested the code against the Enron email set. You can grab a copy of it [here](http://info.nuix.com/Enron.html), and the license restrictions are almost non-existant for demo and research users.

A compiled binary can be downloaded [here](https://github.com/MikeThomsen/nifi-email-extraction-bundle/releases/tag/1.0.0). It requires Apache NiFi 1.8.0.