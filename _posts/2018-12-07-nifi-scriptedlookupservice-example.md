---
title: How to script a NiFi LookupService
---

## Overview

A while back, the concept of "lookup Services" was added to the Record API in Apache NiFi. The Record API was great, but it needed a clean way to enrich a record set that didn't involve parsing the entire record set and feeding it record-by-record to a script or custom processor. That's where the `LookupRecord` processor and lookup services come in. 

NiFi comes with a lot of built-in lookup services that can do things ranging from a simple lookup on a CSV file, to enriching from a REST call, to enriching from a database entry. However, there are a lot of cases where enrichment needs to be done based on custom business logic. That's where the `ScriptedLookupService` fits into the picture. It similar to `ExecuteScript` or `InvokeScriptedProcessor` in that it exposes a simple, programmable interface for writing scripts that implement your business logic.

The example below can be tested using `LookupRecord` with a configured `ScriptedLookupService`. It has a single mandatory key, `message`. To configure it, do the following:

1. Add a dynamic property to the `LookupRecord` processor named `message` and set it to a record path in your schema that points to a string field.
2. Configure the processor property for output path to point a string field's record path in your schema so that the result can be set.
3. Send a record set through the processor.

## Example Code

```
import org.apache.nifi.controller.ControllerServiceInitializationContext
import org.apache.nifi.reporting.InitializationException

class SampleScriptedService implements LookupService<String> {
   @Override
    Optional<String> lookup(Map<String,String> coords) {
      Optional.ofNullable("String received a message: \" + coords['message'] + "\"")
    }

    @Override
    Class<?> getValueType() {
        return String
    }

    @Override
    Set<String> getRequiredKeys() {
      return ['message'] as Set<String>
    }

    void setLogger(logger) {
        log = logger
    }

    void onEnabled(context) {

    }

    @Override
    void initialize(ControllerServiceInitializationContext context) throws InitializationException {

    }

    @Override
    Collection<ValidationResult> validate(ValidationContext context) {
        return null
    }

    @Override
    PropertyDescriptor getPropertyDescriptor(String name) {
        return null
    }

    @Override
    void onPropertyModified(PropertyDescriptor descriptor, String oldValue, String newValue) {

    }

    @Override
    List<PropertyDescriptor> getPropertyDescriptors() {
        return null
    }

    @Override
    String getIdentifier() {
        return null
    }
}

lookupService = new SampleScriptedService()
```