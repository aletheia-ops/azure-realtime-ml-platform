# Azure Data Factory

[English](README.md) | [한국어](README.ko.md)

> English is the canonical documentation.

This directory stores version-controlled Data Factory artifacts used for batch ingestion and high-level orchestration.

Planned subdirectories:

```text
pipelines/
datasets/
linked-services/
triggers/
```

Data Factory should move batch data and coordinate scheduled work. Heavy transformations belong in Databricks, and low-latency inference does not belong in ADF.

Do not commit secrets or exported environment-specific credentials.
