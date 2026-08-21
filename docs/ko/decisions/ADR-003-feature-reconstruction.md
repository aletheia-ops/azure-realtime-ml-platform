# ADR-003: 학습을 위해 스트리밍 특성을 오프라인에서 재구성

[English](../../en/decisions/ADR-003-feature-reconstruction.md) | [한국어](../../ko/decisions/ADR-003-feature-reconstruction.md)

> 영어 문서가 기준 문서입니다.

## 상태
승인됨

## 결정
원시 이벤트는 Event Hubs Capture를 통해 보존하고, 과거 학습 데이터셋을 만들 때 Databricks에서 Stream Analytics 스타일의 단기 윈도우 특성을 재구성합니다. 저장된 Stream Analytics 출력을 기준 학습 소스로 사용하지 않습니다.

## 근거
이 방식은 특성 정의 변경, 과거 값 backfill, 실시간 파이프라인 장애 복구, point-in-time 정확성 보장을 가능하게 합니다. 또한 모델 학습을 운영 Stream Analytics 작업과 분리합니다.

## 결과
- 원시 이벤트 이력이 필수 source of truth가 됩니다.
- Databricks는 Stream Analytics와 동일한 Feature Contract 의미를 구현해야 합니다.
- 계산 비용이 큰 안정적 특성은 매 학습마다 전체 재계산하지 않고 materialize하여 증분 갱신합니다.
- 특성 정의가 크게 변경되면 backfill을 수행합니다.
