# Atomic Task Decomposition

The project should be planned as small, independently reviewable changes rather than one large task per Azure service.

## Rules

A good task should normally:

- have one primary responsibility,
- touch a small and predictable file set,
- have a clear completion condition,
- include tests or validation when executable behavior changes,
- produce one focused pull request,
- avoid requiring unrelated work to merge first unless the dependency is explicit.

## Suggested epics and atomic tasks

### Repository foundation

- R-01 Add repository ignore rules.
- R-02 Add editor configuration.
- R-03 Add Python tooling configuration.
- R-04 Add environment-variable template.
- R-05 Add pull-request template.
- R-06 Add CI skeleton.
- R-07 Document component contracts.
- R-08 Document local development setup.

### Event ingestion and streaming

- S-01 Define the canonical event envelope.
- S-02 Add sample event fixtures.
- S-03 Define one short-window feature contract.
- S-04 Implement the corresponding Stream Analytics query.
- S-05 Add expected-output fixtures for that query.
- S-06 Add validation for missing/invalid event fields.

### Lakehouse data engineering

- D-01 Define Bronze landing conventions.
- D-02 Implement Bronze ingestion/read logic.
- D-03 Define the Silver schema.
- D-04 Implement Bronze-to-Silver normalization.
- D-05 Implement deduplication.
- D-06 Add invalid-record handling.
- D-07 Add unit/integration tests for Silver output.

### Feature engineering

- F-01 Implement one historical feature.
- F-02 Implement Databricks reconstruction of one live feature.
- F-03 Add a point-in-time join utility.
- F-04 Add a feature-parity test.
- F-05 Add feature materialization/backfill logic.

### MLOps

- M-01 Build the first versioned training dataset.
- M-02 Add a baseline model.
- M-03 Add MLflow experiment logging.
- M-04 Add evaluation metrics.
- M-05 Add candidate-versus-current comparison.
- M-06 Add model registration.
- M-07 Add serving deployment configuration.
- M-08 Add serving smoke tests.

### Batch orchestration

- A-01 Define one external batch source contract.
- A-02 Add one Data Factory copy pipeline.
- A-03 Add one Databricks-job trigger activity.
- A-04 Add rerun/idempotency validation.

### Inference integration

- I-01 Define the live-feature request schema.
- I-02 Implement request validation.
- I-03 Implement the Model Serving client.
- I-04 Add correlation IDs and structured errors.
- I-05 Add an end-to-end inference smoke test.

## Team ownership

Primary ownership means "default reviewer and maintainer", not exclusive authorship.

| Area | Suggested primary ownership |
|---|---|
| Event Hubs + Stream Analytics | Member 1 |
| ADLS + Data Factory | Member 2 |
| Databricks ingestion + Silver | Member 3 |
| Feature engineering + parity | Member 4 |
| Training + MLflow + evaluation | Member 5 |
| Serving + Function + CI/observability | Member 6 |

## Pull-request sizing

Prefer:

```text
one task
  -> one branch
  -> one focused PR
  -> one independently understandable review
```

Avoid tasks such as "build Databricks pipeline" or "implement MLOps". Those are epics and should be decomposed before work begins.
