# Online Inference Pipeline

[English](../en/online-inference.md) | [한국어](../ko/online-inference.md)

> English is the canonical documentation. If translations diverge, the English version is authoritative.

The online path is optimized for low latency. Stream Analytics computes only short-lived event-time features; historical features are served from Databricks-managed feature tables.

```mermaid
flowchart LR
    EVENT[Incoming Event\nuser_id / amount / merchant_id / event_time]
    EH[Azure Event Hubs]
    ASA[Stream Analytics\nshort-window features]
    FUNC[Azure Function\nvalidate + map schema]
    ONLINE[Online Historical Features\navg_tx_30d / tx_std_90d / merchant_risk]
    SERVE[Databricks Model Serving]
    RESULT[Prediction]

    EVENT --> EH
    EH --> ASA
    ASA -->|tx_count_5m\nspend_10m\nfailed_tx_2m| FUNC
    FUNC -->|entity keys + live features| SERVE
    ONLINE -. feature lookup .-> SERVE
    SERVE --> RESULT
```

## Example model input

| Feature | Source at inference time |
|---|---|
| `amount` | Current event |
| `tx_count_5m` | Stream Analytics |
| `spend_10m` | Stream Analytics |
| `failed_tx_2m` | Stream Analytics |
| `avg_tx_30d` | Databricks feature table |
| `tx_std_90d` | Databricks feature table |
| `merchant_risk` | Databricks feature table |

## Boundary rules

- Stream Analytics does not perform long historical joins or heavy data cleansing.
- Azure Function does not calculate large-scale features; it handles lightweight integration concerns.
- Databricks Model Serving receives the complete serving context and performs inference.
- ADLS is not queried synchronously on the inference path.
