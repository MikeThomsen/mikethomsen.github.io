---
title: Making NiFi components searchable
---

If you have a NiFi component that you work on for your business/team, you can make it searchable using the `Searchable` interface. The following code sample is taken from [NIFI-4406](https://issues.apache.org/jira/browse/NIFI-4406), which makes `ExecuteScript` searchable so that you can search for words inside of either the script body property or by loading the contents of the script file and searching that.

```
import org.apache.nifi.search.Searchable

    @Override
    public Collection<SearchResult> search(SearchContext context) {
        Collection<SearchResult> results = new ArrayList<>();

        String term = context.getSearchTerm();

        String scriptFile = context.getProperty(ScriptingComponentUtils.SCRIPT_FILE).evaluateAttributeExpressions().getValue();
        String script = context.getProperty(ScriptingComponentUtils.SCRIPT_BODY).getValue();

        if (StringUtils.isBlank(script)) {
            try {
                script = IOUtils.toString(new FileInputStream(scriptFile), "UTF-8");
            } catch (Exception e) {
                getLogger().error(String.format("Could not read from path %s", scriptFile), e);
                return results;
            }
        }

        Scanner scanner = new Scanner(script);
        int index = 1;

        while (scanner.hasNextLine()) {
            String line = scanner.nextLine();
            if (StringUtils.containsIgnoreCase(line, term)) {
                String text = String.format("Matched script at line %d: %s", index, line);
                results.add(new SearchResult.Builder().label(text).match(term).build());
            }
            index++;
        }

        return results;
    }
```

The pattern is pretty simple:

1. Figure out what should be searched within the component.
2. Build a collection of `SearchResult` objects if there are hits.
3. Return an empty collection if there are not hits.