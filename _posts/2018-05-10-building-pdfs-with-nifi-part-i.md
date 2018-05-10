---
title: Building PDFS with Apache Nifi
---

I just released a new NiFi processor that provides the ability to generate a PDF from flowfile contents, attributes or both. It can be downloaded from [here](https://github.com/MikeThomsen/nifi-pdf-generator-bundle). For right now, it references NiFi 1.7.0-SNAPSHOT as a requirement, but I might bump that down to 1.6.0 or even 1.5.0 later once I have time to test it.

It's powered by iText 7 community edition, so unfortunately all of the code in that repo I linked to is currently under the AGPL. (That also means it's not going to be ever merged into NiFi itself because the ASF prohibits the use of AGPL dependencies)

The processor uses Mustache templates to build HTML file, which are in turn converted to PDFs using iText. An example use case would be to set up a nightly aggregation to be run on MongoDB or ElasticSearch that is then fed to this process to provided statistics on a data set.