---
date: 2018-05-07 06:15:00
title: HBase Visibility Labels
---

# HBase Visibility Labels

### Basic Terms

* Visibility label - one or more tokens that may be combined with boolean logic to define restrictions on data access.
* Authorizations - one or more tokens that can be provided to HBase to evaluate against a visibility label.

### Overview

Visibility labels are an expression that is stored on a cell that determines whether or not a scanner can see the cell. For example, consider the following row:

* patient-1:attr:name
* patient-1:attr:attending_physician
* patient-1:attr:diagnosis_1
* patient-1:attr:diagnosis_2
* patient-1:attr:medication_1
* patient-1:attr:medication_2
* patient-1:attr:billing_codes
* patient-1:attr:address

Some of that information is Personally Identifiable Information (PII), some Personal Health Information (PHI), some billing-related and some that doesn't need to restricted for anyone authorized to be in the system in the first place.

To restrict that information, you could establish four basic tokens that a user must have to see everything:

* OPEN
* BILLING
* PII
* PHI

The patient's name and attending physician aren't particularly sensitive, so we could assign them just `OPEN`. That way, any user in the system can at least figure out who the patient is and which doctor provided them care. A staff lawyer, for instance, might not need to know how patients were diagnosed or treated, but would need to be able to find out which doctor treated which patient in the event of malpractice claims.

The diagnosis and medication are `PHI` and so would be assigned that label. Likewise, billing codes would have `BILLING` assigned to them.

Now suppose you have a particularly sensitive field, such as one which details a medical report for patients who are victims of crime. You would need multiple restrictions on that, so you might add a new label called `LEGAL_RESTRICTED` and assign both `PHI` and `PII` because the field would be restricted and cover both health and personally identifiable information. The way you do that is with boolean logic. Instead of just assigning a single token, you would set `LEGAL_RESTRICTED&PII&PHI` to tell HBase that a scanner must have authorization to view all three of those labels.

In practice, the way that last scenario would work is that only a handful of vetted users would have access to `LEGAL_RESTRICTED`. The HBase user doing the scanning would have all of the tokens, but the application would provide the scanner with only the tokens for the current user. Dr. John Smith might only have `OPEN`, `PHI` and `PII`, but Dr. Jane Doe could have all of those, as well as `LEGAL_RESTRICTED` because she has been vetted by the administration to handle at-risk patients. When Dr. Smith views the record for `patient-1`, that lack of `LEGAL_RESTRICTED` will go into effect and the sensitive field(s) will not even exist as far as he is concerned (HBase won't even provide a key with a null value).

### Setup

Set the following values in `hbase-site.xml`:

```
  <property>
    <name>hbase.coprocessor.region.classes</name>
    <value>org.apache.hadoop.hbase.security.visibility.VisibilityController</value>
  </property>

  <property>
    <name>hbase.coprocessor.master.classes</name>
    <value>org.apache.hadoop.hbase.security.visibility.VisibilityController</value>
  </property>
```

Then restart HBase for that new configuration to take effect. Visibility labels will work with simple auth, so you don't need to have Kerberos configured to take advantage of this feature in a development environment.

To configure what labels are available do the following steps:

1. su - hbase (assuming `hbase` is the user running HBase)
2. hbase shell
3. add_labels ["OPEN", "BILLING", "PHI", "PII", "LEGAL_RESTRICTED"]
4. set_auths staff_user ["OPEN", "BILLING", "PHI", "PII", "LEGAL_RESTRICTED"]
5. set_auths external ["OPEN", "BILLING", "PII"]

The reason why there are two `set_auths` in the example is that with this feature you can deploy multiple instances of your application against the data lake and tweak the configuration to provide a HBase user that has only the right authorizations for the class(es) of users that will use that instance. So in this example, the hospital has two instances of the application, one for staff users and one for external users that only need to see billing and basic PII about their patients.

Each of the client objects in the HBase client API provides either a field for authorizations or labels. That tends fall along the lines of authorizations are for read operations and labels for write operations.