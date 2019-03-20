---
title: Announcing the Apache NiFi Test Harness
---

[Peter Horvath](https://github.com/peter-gergely-horvath/) provided us with a great new feature pull request that adds a test harness for running a live NiFi instance within a JUnit integration test. For now, the feature is only officially included in the unreleased 1.10.0-SNAPSHOT code on GitHub, but I put out a stable build as a separate project that targets NiFi 1.8.0 [here](https://github.com/MikeThomsen/nifi-testharness).

Right now, it is still a MVP/experimental API so some tweaking and experimentation in building integration tests around it will be necessary. That said, this is a code sample of what it looks like in use:

```
public class NiFiMockFlowTest {

    private static final InputStream DEMO_DATA_AS_STREAM =
            NiFiMockFlowTest.class.getResourceAsStream("/sample_technology_rss.xml");

    public static class MockedGetHTTP extends GetHTTPMock {
        public MockedGetHTTP() {
            super("text/xml; charset=utf-8", () -> DEMO_DATA_AS_STREAM);
        }
    }

    private static final SimpleNiFiFlowDefinitionEditor CONFIGURE_MOCKS_IN_NIFI_FLOW = SimpleNiFiFlowDefinitionEditor.builder()
            .updateFlowFileBuiltInNiFiProcessorVersionsToNiFiVersion()
            .setClassOfSingleProcessor("GetHTTP", MockedGetHTTP.class)
            .build();

    private TestNiFiInstance testNiFiInstance;

    @Before
    public void bootstrapNiFi() throws Exception {
        if (Constants.OUTPUT_DIR.exists()) {
            FileUtils.deleteDirectoryRecursive(Constants.OUTPUT_DIR.toPath());
        }

        File nifiZipFile = TestUtils.getBinaryDistributionZipFile(Constants.NIFI_ZIP_DIR);

        TestNiFiInstance testNiFi = TestNiFiInstance.builder()
                .setNiFiBinaryDistributionZip(nifiZipFile)
                .setFlowXmlToInstallForTesting(Constants.FLOW_XML_FILE)
                .modifyFlowXmlBeforeInstalling(CONFIGURE_MOCKS_IN_NIFI_FLOW)
                .build();

        testNiFi.install();
        testNiFi.start();
        testNiFiInstance = testNiFi;
    }

    @Test
    public void testFlowCreatesFilesInCorrectLocation() throws IOException {
        assertTrue("Output directory not found: " + Constants.OUTPUT_DIR, Constants.OUTPUT_DIR.exists());
        File outputFile = new File(Constants.OUTPUT_DIR, "bbc-world.rss.xml");
        assertTrue("Output file not found: " + outputFile, outputFile.exists());
        List<String> strings = Files.readAllLines(outputFile.toPath());
        boolean atLeastOneLineContainsNiFi = strings.stream().anyMatch(line -> line.toLowerCase().contains("nifi"));
        assertTrue("There was no line containing NiFi", atLeastOneLineContainsNiFi);
        boolean atLeastOneLineContainsNiFiVersion = strings.stream().anyMatch(line -> line.toLowerCase().contains("latest nifi version"));
        assertTrue("There was no line containing 'latest NiFi version'", atLeastOneLineContainsNiFiVersion);
    }

    @After
    public void shutdownNiFi() {
        if (testNiFiInstance != null) {
            testNiFiInstance.stopAndCleanup();
        }
    }
}
```