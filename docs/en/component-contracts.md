# Component Contracts

[English](../en/component-contracts.md) | [한국어](../ko/component-contracts.md)

> English is the canonical documentation. If translations diverge, the English version is authoritative.

This document defines the responsibility and handoff contract of each major platform component. The purpose is to prevent overlapping ownership and to make integration points explicit before domain-specific implementation begins.

## Contract format

Each component is documented with:

- **Role** — the component's single primary responsibility.
- **Entry contract** — what it is allowed to receive.
- **End contract** — what it must produce before downstream consumers may depend on it.
- **Must not** — responsibilities that belong elsewhere.
- **Failure expectations** — what downstream systems may assume when the component fails.

---

## Azure Event Hubs

### Role
High-throughput ingestion and buffering of live event streams.

### Entry contract
An event must have, at minimum:

- a stable event identifier,
- an event timestamp,
- the entity key required by downstream processing,
- a versioned event schema,
- domain payload fields.

Example envelope:

```json
{
  "event_id": "...",
  "event_time": "2026-08-21T04:00:00Z",
  "entity_id": "...",
  "schema_version": "1",
  "payload": {}
}
```

### End contract
Consumers receive the original event payload and metadata required to identify ordering/partition context. Raw events are available independently to both the live-processing path and the historical-capture path.

### Must not
- perform business transformation,
- calculate ML features,
- become the system of record,
- train or serve models.

### Failure expectations
Producers and consumers must tolerate transient delivery/retry behavior. Durable historical reconstruction must not depend on Stream Analytics output; Event Hubs Capture/ADLS is the replay source.

---

## Event Hubs Capture

### Role
Persist the raw stream to ADLS independently of the real-time path.

### Entry contract
Events accepted by Event Hubs.

### End contract
Immutable/raw historical event files are available in the Bronze landing area with enough metadata to recover event time, entity identity, and schema version.

### Must not
- clean data,
- calculate features,
- depend on Stream Analytics results.

### Failure expectations
Capture lag may delay offline processing but must not change event semantics. Offline jobs should be restartable once files are present.

---

## Azure Stream Analytics

### Role
Compute low-latency event-time features and operational stream logic.

### Entry contract
Versioned live events from Event Hubs plus only lightweight reference data explicitly required by the stream query.

### End contract
A versioned live-feature payload containing:

- event/entity identifiers,
- prediction/event time,
- current-event fields required by the model,
- short-window/event-time features,
- feature-contract version.

Example:

```json
{
  "event_id": "...",
  "entity_id": "...",
  "event_time": "...",
  "feature_contract_version": "1",
  "live_features": {
    "event_count_5m": 7,
    "value_sum_10m": 3200.0
  }
}
```

### Must not
- perform large historical joins,
- calculate long-horizon features from the lake,
- create the canonical training dataset,
- own model training or model registry.

### Failure expectations
A Stream Analytics outage affects live inference availability but must not destroy the ability to reconstruct the same features later from captured raw events.

---

## ADLS Gen2 / Bronze

### Role
Durable source-of-truth storage for raw and batch-ingested data.

### Entry contract
- Event Hubs Capture output,
- Data Factory batch-copy output,
- source metadata needed for lineage.

### End contract
Data is durably addressable by downstream Databricks jobs and retains the information required to replay/reprocess historical records.

### Must not
- contain hidden business logic,
- be treated as a low-latency serving database,
- silently mutate source records.

### Failure expectations
Downstream Databricks pipelines should be rerunnable and idempotent against persisted data.

---

## Azure Data Factory

### Role
Batch data movement and high-level scheduled orchestration.

### Entry contract
A configured source, destination, credentials/managed identity, schedule/trigger, and explicit activity parameters.

### End contract
Either:

1. batch data has been copied to its agreed landing location, or
2. the downstream job has been triggered with explicit parameters and status is observable.

### Must not
- become the primary transformation engine when Databricks owns transformation,
- participate in the low-latency inference path,
- contain model-training business logic.

### Failure expectations
Activities must expose observable failure status and support safe reruns. Copy activities should avoid creating ambiguous duplicate batches.

---

## Databricks: Bronze to Silver

### Role
Validate, normalize, deduplicate, type, and standardize raw data into reusable clean event/entity tables.

### Entry contract
Bronze records with lineage metadata and recognized schema versions.

### End contract
Silver tables with:

- explicit schema,
- normalized data types,
- deduplication policy applied,
- invalid-data handling defined,
- event time preserved,
- stable keys suitable for point-in-time joins.

### Must not
- introduce future information into historical rows,
- calculate serving-only behavior that cannot be reproduced offline.

---

## Databricks: Feature Engineering

### Role
Create historical features, reconstruct real-time feature semantics for training, and materialize reusable feature tables.

### Entry contract
Point-in-time-addressable Silver data plus versioned feature contracts.

### End contract
Feature tables must contain:

- entity key(s),
- feature timestamp or validity timestamp,
- deterministic feature values,
- feature-contract/version metadata where appropriate,
- no information unavailable at the feature timestamp.

### Must not
- change feature semantics independently of the corresponding feature contract,
- use future label/outcome information in feature calculation.

### Failure expectations
Feature tables/backfills must be reproducible from retained historical data.

---

## Training Dataset Builder

### Role
Assemble one point-in-time-correct feature-and-label row per historical prediction event.

### Entry contract
- reconstructed short-window features,
- historical feature tables,
- prediction/event timestamp,
- labels/outcomes,
- join keys and feature contracts.

### End contract
A versioned training dataset where each row represents the information that would have been available at prediction time plus the later observed label.

Identifiers used for lineage may remain in the table but must be explicitly separated from model input features.

### Must not
- use future feature values,
- calculate different feature semantics from production,
- silently drop rows without recorded reason.

---

## Databricks Training / MLflow

### Role
Train candidate models and record reproducible experiments.

### Entry contract
A versioned training dataset, model configuration, code version, and deterministic split/evaluation policy.

### End contract
An MLflow run containing at minimum:

- parameters,
- metrics,
- model artifact,
- data/code version references,
- evaluation artifacts sufficient to compare the candidate with the current model.

### Must not
- deploy an unvalidated candidate directly,
- perform unrelated ETL inside the training routine.

---

## Model Evaluation / Promotion

### Role
Determine whether a candidate satisfies explicit promotion criteria.

### Entry contract
Candidate model/run, baseline/production model reference, agreed evaluation dataset, and promotion thresholds.

### End contract
A deterministic promotion decision with recorded metrics and rationale.

### Must not
- promote based on undocumented manual preference,
- evaluate on training data only.

---

## Unity Catalog / Model Registry

### Role
Govern approved model artifacts and versions.

### Entry contract
A model candidate that has passed the promotion policy and includes required lineage/metadata.

### End contract
A registered, versioned model reference suitable for deployment and rollback.

### Must not
- contain arbitrary unvalidated training outputs as production-ready versions.

---

## Databricks Model Serving

### Role
Provide low-latency inference from an approved model and required online features.

### Entry contract
A schema-valid inference request containing:

- entity key(s),
- current-event/live features,
- required request metadata,
- compatible feature/model contract version.

### End contract
A versioned prediction response containing at minimum:

- prediction/score,
- model version,
- prediction timestamp,
- request/event correlation identifier.

### Must not
- run large historical Spark transformations per request,
- query the raw lake for feature construction,
- retrain models.

---

## Azure Function / Inference Adapter

### Role
Provide lightweight integration between Stream Analytics and Databricks Model Serving.

### Entry contract
The Stream Analytics live-feature payload.

### End contract
Either:

- a schema-valid request has been sent to Model Serving and its response propagated, or
- a structured, observable failure has been produced.

The adapter may validate schemas, map fields, add correlation metadata, implement bounded retries, and apply lightweight routing.

### Must not
- perform heavy feature engineering,
- reproduce Databricks historical feature logic,
- become a second model-serving platform.

---

## Cross-component invariants

### Feature semantic parity
A feature implemented in both Stream Analytics and Databricks must follow one shared feature contract. Different implementations are allowed; different semantics are not.

### Point-in-time correctness
Training features must contain only information available at the historical prediction timestamp.

### Replayability
The offline training path must remain reconstructable from durable raw/Silver data even when the real-time processing layer experienced an outage.

### Versioned interfaces
Event schemas, feature contracts, training datasets, and model inference interfaces should be versioned whenever a breaking semantic change occurs.

### Idempotency
Batch and offline processing should be safe to retry without silently duplicating logical records.
