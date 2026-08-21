# ADR-001: Use Stream Analytics and Databricks for Different Time Horizons

[English](../../en/decisions/ADR-001-stream-analytics-and-databricks.md) | [한국어](../../ko/decisions/ADR-001-stream-analytics-and-databricks.md)

> English is the canonical documentation.

## Status
Accepted

## Decision
Use Azure Stream Analytics for low-latency event-time filtering and short-window aggregation. Use Azure Databricks for heavy historical processing, cleansing, joins, long-window feature engineering, and offline reconstruction of live-feature semantics.

## Rationale
The two systems overlap technically, but they serve different operational goals. Stream Analytics answers what is happening now; Databricks answers what happened historically and prepares reusable analytical/ML state.

## Consequences
- Stream Analytics output is not the canonical historical training source.
- Raw Event Hub data must be retained independently through Event Hubs Capture.
- Shared feature semantics require explicit feature contracts and parity tests.
