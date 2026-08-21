# ADR-002: Use Databricks-Only MLOps

[English](../../en/decisions/ADR-002-databricks-only-mlops.md) | [한국어](../../ko/decisions/ADR-002-databricks-only-mlops.md)

> English is the canonical documentation.

## Status
Accepted

## Decision
Use Azure Databricks as the ML platform for feature management, model training, experiment tracking, model registration, governance, and online model serving. Do not introduce Azure Machine Learning unless a later requirement cannot be met cleanly within Databricks.

## Rationale
For one six-person team, adding Azure ML would create an additional platform boundary without a clear current need. Databricks already provides the required MLOps lifecycle through MLflow, Unity Catalog, feature tooling, jobs, and Model Serving.

## Consequences
- MLflow is the primary experiment-tracking mechanism.
- Unity Catalog is the model registry/governance layer.
- Databricks Model Serving is the production inference endpoint.
- Azure ML remains an optional future integration, not a baseline dependency.
