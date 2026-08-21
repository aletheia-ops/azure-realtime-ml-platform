# 컴포넌트 계약

[English](../en/component-contracts.md) | [한국어](../ko/component-contracts.md)

> 영어 문서가 기준 문서입니다. 번역본과 내용이 다를 경우 영어 문서를 우선합니다.

이 문서는 주요 플랫폼 컴포넌트 각각의 책임과 인수인계 계약을 정의합니다. 목적은 도메인 구현 전에 책임 중복을 방지하고 통합 지점을 명확히 하는 것입니다.

## 계약 형식

각 컴포넌트는 다음 항목으로 문서화합니다.

- **역할(Role)** — 단일한 주요 책임
- **입력 계약(Entry contract)** — 받을 수 있는 입력
- **출력 계약(End contract)** — 다운스트림이 의존하기 전에 보장해야 하는 출력
- **하면 안 되는 일(Must not)** — 다른 계층에 속하는 책임
- **실패 기대사항(Failure expectations)** — 실패 시 다른 컴포넌트가 가정할 수 있는 동작

---

## Azure Event Hubs

### 역할
실시간 이벤트 스트림의 고처리량 수집 및 버퍼링.

### 입력 계약
최소한 다음을 포함한 버전 관리 이벤트:
- 안정적인 이벤트 ID
- 이벤트 발생 시각
- 다운스트림 처리용 엔터티 키
- 스키마 버전
- 도메인 payload

### 출력 계약
원본 이벤트 payload와 파티션/순서 컨텍스트를 식별할 메타데이터를 소비자에게 제공합니다. 동일 원시 이벤트가 실시간 처리 경로와 과거 Capture 경로 양쪽에서 독립적으로 사용 가능해야 합니다.

### 하면 안 되는 일
- 비즈니스 변환
- ML 특성 계산
- 시스템 오브 레코드 역할
- 모델 학습 또는 서빙

### 실패 기대사항
일시적인 전달/재시도는 허용합니다. 과거 재구성은 Stream Analytics 출력에 의존하지 않으며 Event Hubs Capture/ADLS가 replay source가 됩니다.

---

## Event Hubs Capture

### 역할
실시간 경로와 독립적으로 원시 이벤트를 ADLS에 저장.

### 입력 계약
Event Hubs가 수용한 이벤트.

### 출력 계약
이벤트 시간, 엔터티 ID, 스키마 버전을 복원할 수 있는 메타데이터를 포함한 원시 이력 파일을 Bronze 영역에 저장합니다.

### 하면 안 되는 일
- 데이터 정제
- 특성 계산
- Stream Analytics 결과 의존

### 실패 기대사항
Capture 지연은 오프라인 처리를 늦출 수 있지만 이벤트 의미를 바꾸면 안 됩니다. 파일이 도착하면 오프라인 작업은 안전하게 재실행할 수 있어야 합니다.

---

## Azure Stream Analytics

### 역할
저지연 event-time 특성과 실시간 스트림 로직 계산.

### 입력 계약
Event Hubs의 버전 관리된 실시간 이벤트와 쿼리에 필요한 소규모 reference data.

### 출력 계약
다음을 포함하는 버전 관리 live-feature payload:
- 이벤트/엔터티 ID
- 이벤트 또는 예측 시각
- 모델에 필요한 현재 이벤트 필드
- 단기 윈도우/event-time 특성
- feature contract 버전

### 하면 안 되는 일
- 대규모 과거 조인
- 데이터 레이크 기반 장기 특성 계산
- 기준 학습 데이터셋 생성
- 모델 학습 및 레지스트리 소유

### 실패 기대사항
장애 시 실시간 추론 가용성은 영향을 받을 수 있지만 Capture된 원시 이벤트로 동일 특성을 나중에 재구성할 수 있어야 합니다.

---

## ADLS Gen2 / Bronze

### 역할
원시 이벤트와 배치 수집 데이터의 내구성 있는 기준 저장소.

### 입력 계약
- Event Hubs Capture 출력
- Data Factory batch copy 출력
- lineage에 필요한 소스 메타데이터

### 출력 계약
Databricks가 재처리할 수 있도록 원본 정보와 이력 데이터를 지속적으로 보존합니다.

### 하면 안 되는 일
- 숨겨진 비즈니스 로직 포함
- 저지연 서빙 DB처럼 사용
- 소스 레코드의 무음 변경

### 실패 기대사항
Databricks 파이프라인은 저장된 데이터를 기준으로 재실행 가능하고 idempotent해야 합니다.

---

## Azure Data Factory

### 역할
배치 데이터 이동과 상위 수준의 예약 오케스트레이션.

### 입력 계약
구성된 소스/대상, 인증 또는 Managed Identity, schedule/trigger, 명시적인 activity parameter.

### 출력 계약
다음 중 하나를 보장합니다.
1. 배치 데이터가 합의된 landing location으로 복사됨
2. 다운스트림 작업이 명시적 파라미터로 트리거되고 상태를 관측 가능함

### 하면 안 되는 일
- Databricks가 변환을 담당할 때 주요 변환 엔진이 되기
- 저지연 추론 경로에 참여
- 모델 학습 비즈니스 로직 포함

### 실패 기대사항
Activity 실패 상태를 관측할 수 있어야 하고 재실행이 안전해야 합니다.

---

## Databricks: Bronze → Silver

### 역할
원시 데이터를 검증, 정규화, 중복 제거, 타입 변환하여 재사용 가능한 정제 테이블로 변환.

### 입력 계약
lineage 메타데이터와 인식 가능한 스키마 버전을 가진 Bronze 레코드.

### 출력 계약
다음을 갖는 Silver 테이블:
- 명시적 스키마
- 정규화된 타입
- 중복 제거 정책 적용
- 잘못된 데이터 처리 정책
- event_time 보존
- point-in-time join용 안정적인 키

### 하면 안 되는 일
- 미래 정보를 과거 행에 유입
- 오프라인에서 재현 불가능한 서빙 전용 의미 생성

---

## Databricks: Feature Engineering

### 역할
과거 특성을 생성하고, 학습용으로 실시간 특성 의미를 재구성하며, 재사용 가능한 Feature Table을 materialize.

### 입력 계약
point-in-time 조회 가능한 Silver 데이터와 버전 관리 Feature Contract.

### 출력 계약
Feature Table은 다음을 포함해야 합니다.
- 엔터티 키
- feature timestamp 또는 validity timestamp
- 결정적인 특성 값
- 필요한 경우 feature contract/version 메타데이터
- 해당 시점 이후의 정보 미포함

### 하면 안 되는 일
- Feature Contract와 독립적으로 의미 변경
- 미래 label/outcome 정보를 특성 계산에 사용

### 실패 기대사항
Feature Table과 backfill은 보존된 과거 데이터에서 재현 가능해야 합니다.

---

## Training Dataset Builder

### 역할
각 과거 예측 이벤트당 point-in-time 정확성을 만족하는 하나의 feature-label 행을 생성.

### 입력 계약
- 재구성된 단기 윈도우 특성
- 과거 Feature Table
- 예측/event timestamp
- label/outcome
- join key와 Feature Contract

### 출력 계약
각 행이 과거 예측 시점에 사용 가능했던 정보와 이후 관측된 label을 표현하는 버전 관리 학습 데이터셋.

### 하면 안 되는 일
- 미래 특성 값 사용
- 운영 환경과 다른 특성 의미 계산
- 사유 기록 없이 행 삭제

---

## Databricks Training / MLflow

### 역할
후보 모델 학습 및 재현 가능한 실험 기록.

### 입력 계약
버전 관리 학습 데이터셋, 모델 설정, 코드 버전, 결정적인 split/evaluation 정책.

### 출력 계약
최소 다음을 포함하는 MLflow run:
- parameters
- metrics
- model artifact
- 데이터/코드 버전 참조
- 현재 모델과 비교 가능한 평가 artifact

### 하면 안 되는 일
- 검증되지 않은 후보 모델 직접 배포
- 학습 루틴 내부에서 무관한 ETL 수행

---

## Model Evaluation / Promotion

### 역할
후보 모델이 명시된 promotion 기준을 충족하는지 결정.

### 입력 계약
후보 모델/run, baseline 또는 production 모델, 합의된 평가 데이터셋, promotion threshold.

### 출력 계약
기록된 metric과 근거를 포함한 결정적인 승격 여부.

### 하면 안 되는 일
- 문서화되지 않은 수동 선호로 승격
- 학습 데이터만으로 평가

---

## Unity Catalog / Model Registry

### 역할
승인된 모델 artifact와 버전을 관리하고 거버넌스를 적용.

### 입력 계약
promotion policy를 통과하고 필요한 lineage/metadata를 가진 후보 모델.

### 출력 계약
배포와 rollback에 사용할 수 있는 등록 및 버전 관리 모델 참조.

---

## Databricks Model Serving

### 역할
승인된 모델과 필요한 온라인 특성을 사용해 저지연 추론 제공.

### 입력 계약
다음을 포함한 스키마 유효 inference request:
- 엔터티 키
- 현재 이벤트/실시간 특성
- 요청 메타데이터
- 호환되는 feature/model contract 버전

### 출력 계약
최소 다음을 포함한 버전 관리 예측 응답:
- prediction/score
- model version
- prediction timestamp
- request/event correlation ID

### 하면 안 되는 일
- 요청마다 대규모 Spark 과거 변환 실행
- 원시 레이크를 조회해 특성 생성
- 모델 재학습

---

## Azure Function / Inference Adapter

### 역할
Stream Analytics와 Databricks Model Serving 사이의 경량 통합.

### 입력 계약
Stream Analytics의 live-feature payload.

### 출력 계약
다음 중 하나:
- 유효한 요청이 Model Serving에 전달되고 응답이 전파됨
- 구조화되고 관측 가능한 실패가 생성됨

스키마 검증, 필드 매핑, correlation metadata, 제한된 재시도, 경량 라우팅은 수행할 수 있습니다.

### 하면 안 되는 일
- 대규모 feature engineering
- Databricks 과거 특성 로직 재구현
- 두 번째 모델 서빙 플랫폼 역할

---

## 컴포넌트 공통 불변조건

### Feature semantic parity
Stream Analytics와 Databricks 양쪽에서 구현되는 특성은 하나의 Feature Contract를 따라야 합니다. 구현 방식은 달라도 의미는 같아야 합니다.

### Point-in-time correctness
과거 학습 특성에는 해당 예측 시점에 사용 가능했던 정보만 포함해야 합니다.

### Replayability
실시간 처리 계층에 장애가 있었더라도 원시/Silver 데이터에서 오프라인 학습 경로를 재구성할 수 있어야 합니다.

### Versioned interfaces
이벤트 스키마, Feature Contract, 학습 데이터셋, 모델 inference interface의 의미가 깨지는 변경은 버전 관리해야 합니다.

### Idempotency
배치 및 오프라인 처리는 재실행해도 논리적으로 중복 레코드를 만들지 않아야 합니다.
