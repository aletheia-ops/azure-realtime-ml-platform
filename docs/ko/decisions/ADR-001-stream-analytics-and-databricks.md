# ADR-001: 서로 다른 시간 범위를 위해 Stream Analytics와 Databricks를 함께 사용

[English](../../en/decisions/ADR-001-stream-analytics-and-databricks.md) | [한국어](../../ko/decisions/ADR-001-stream-analytics-and-databricks.md)

> 영어 문서가 기준 문서입니다.

## 상태
승인됨

## 결정
Azure Stream Analytics는 저지연 event-time 필터링과 단기 윈도우 집계를 담당합니다. Azure Databricks는 대규모 과거 데이터 처리, 정제, 조인, 장기 특성 엔지니어링, 그리고 실시간 특성 의미의 오프라인 재구성을 담당합니다.

## 근거
두 시스템은 기술적으로 일부 겹치지만 운영 목적이 다릅니다. Stream Analytics는 "지금 무슨 일이 일어나는가"를 다루고, Databricks는 "과거에 무슨 일이 있었는가"를 분석하며 재사용 가능한 분석/ML 상태를 만듭니다.

## 결과
- Stream Analytics 출력은 기준 과거 학습 소스가 아닙니다.
- 원시 Event Hub 데이터는 Event Hubs Capture를 통해 별도로 보존해야 합니다.
- 공통 특성 의미는 명시적 Feature Contract와 parity test로 보호해야 합니다.
