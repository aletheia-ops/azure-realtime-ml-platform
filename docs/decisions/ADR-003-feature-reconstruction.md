# ADR-003: Reconstruct Streaming Features Offline for Training

## Status
Accepted

## Decision
Persist raw events through Event Hubs Capture and reconstruct Stream Analytics-style short-window features in Databricks when building historical training datasets. Do not make persisted Stream Analytics output the canonical training source.

## Rationale
This preserves flexibility to change feature definitions, backfill historical values, recover from live-pipeline outages, and enforce point-in-time correctness. It also avoids coupling model training to the operational Stream Analytics job.

## Consequences
- Raw event history is a required source of truth.
- Databricks must implement the same semantic feature contracts as Stream Analytics.
- Expensive stable features should be materialized and updated incrementally rather than recomputed from raw history for every training run.
- Backfills are expected when feature definitions change materially.
