# System Architecture

[English](../en/architecture.md) | [한국어](../ko/architecture.md)

> English is the canonical documentation. If translations diverge, the English version is authoritative.

## Service boundaries

| Component | Primary responsibility |
|---|---|
| Azure Event Hubs | Real-time event ingestion and buffering |
| Event Hubs Capture | Persist raw event history to ADLS |
| Azure Stream Analytics | Low-latency event-time filtering and window features |
| ADLS Gen2 | Durable lake storage / source of truth |
| Azure Databricks | Heavy transformation, historical feature engineering, training and MLOps |
| Azure Data Factory | Batch ingestion and high-level orchestration |
| Azure Function | Lightweight inference integration and schema validation |
| Databricks Model Serving | Production model inference |
| MLflow + Unity Catalog | Experiment tracking, model registry and governance |

## End-to-end view

```mermaid
flowchart LR
    subgraph SRC[Data Sources]
        EVT[Event Producers]
        BATCH[SQL / API / Files]
    end

    subgraph INGEST[Ingestion]
        EH[Azure Event Hubs]
        ADF[Azure Data Factory]
    end

    subgraph LIVE[Real-Time Path]
        ASA[Azure Stream Analytics]
        FUNC[Azure Function\nInference Adapter]
    end

    subgraph DATA[Lakehouse]
        BRONZE[ADLS Gen2\nBronze]
        DBX[Azure Databricks]
        SILVER[Silver Delta]
        GOLD[Gold / BI]
        FEATURES[Feature Tables]
    end

    subgraph ML[Databricks MLOps]
        TRAIN[Training]
        MLFLOW[MLflow]
        UC[Unity Catalog\nModel Registry]
        SERVE[Databricks\nModel Serving]
    end

    EVT --> EH
    EH -->|live events| ASA
    EH -. Event Hubs Capture .-> BRONZE

    BATCH --> ADF
    ADF -->|batch ingestion| BRONZE
    ADF -. schedule / trigger .-> DBX

    ASA -->|short-window features| FUNC

    BRONZE --> DBX
    DBX --> SILVER
    SILVER --> GOLD
    SILVER --> FEATURES

    FEATURES --> TRAIN
    TRAIN --> MLFLOW
    MLFLOW --> UC
    UC --> SERVE
    FEATURES -. online historical features .-> SERVE

    FUNC -->|event + live features| SERVE
    SERVE --> PRED[Prediction]
```

## Why the architecture forks after Event Hubs

The live and historical paths have different goals:

```mermaid
flowchart TD
    EH[Event Hubs]
    EH --> LIVE[Stream Analytics\nWhat is happening now?]
    EH -. Capture .-> HIST[ADLS + Databricks\nWhat happened historically?]

    LIVE --> INF[Online inference]
    HIST --> FEAT[Historical features + training data]
    FEAT --> MODEL[Model lifecycle]
    MODEL --> INF
```

Stream Analytics is therefore not the permanent source of ML training features. Raw events are retained independently so historical features can be reconstructed, backfilled and redefined later.

## Data-layer rule

Gold tables and ML feature tables are separate concepts:

```mermaid
flowchart LR
    S[Silver Delta Tables] --> G[Gold\nBusiness / BI]
    S --> F[ML Feature Tables]
    G --> BI[Power BI / Analytics]
    F --> ML[Training + Serving]
```

This prevents business-facing aggregates from becoming an accidental ML contract.
