---
title: NiFi Data Generation Bundle 1.8.0 Released
---
Data generation bundle has been updated to support NiFi 1.8.0. The GenerateRecord processor now supports expression language, enabling scenarios like this:

```
{
  "name": "UserStatus",
  "type": "record",
  "fields": [
    {
      "name": "login_status",
      "type": {
        "name": "flag_enum",
        "type": "enum",
        "symbols": [ "LOGIN", "LOGOUT", "REJECTED" ]
      }
    },
    {
      "name": "timestamp",
      "type": {
        "type": "long",
        "logicalType": "timestamp-millis",
        "arg.properties": {
          "range": {
            "min": ${now():toNumber():minus(7776000000)},
            "max": ${now():toNumber()}
          }
        }
      }
    }
  ]
}
```

Binaries for NiFi 1.8.0 can be downloaded [here](https://github.com/MikeThomsen/nifi-datageneration-bundle/releases/tag/1.8.0)
