# 원자적 작업 분해

[English](../../en/development/task-decomposition.md) | [한국어](../../ko/development/task-decomposition.md)

> 영어 문서가 기준 문서입니다. 번역본과 내용이 다를 경우 영어 문서를 우선합니다.

프로젝트 작업은 Azure 서비스 단위의 큰 과제가 아니라 작고 독립적으로 리뷰 가능한 변경 단위로 나눕니다.

## 원칙

좋은 작업은 일반적으로 다음을 만족해야 합니다.

- 하나의 주요 책임을 가진다.
- 변경 파일 범위가 작고 예측 가능하다.
- 완료 조건이 명확하다.
- 실행 동작이 바뀌면 테스트 또는 검증을 포함한다.
- 하나의 집중된 PR을 만든다.
- 명시적인 의존성이 아닌 이상 무관한 다른 작업의 선행 병합을 요구하지 않는다.

## 권장 Epic 및 원자 작업

### 저장소 기반
- R-01 `.gitignore` 추가
- R-02 editor 설정 추가
- R-03 Python tooling 설정
- R-04 환경 변수 템플릿 추가
- R-05 PR 템플릿 추가
- R-06 CI skeleton 추가
- R-07 컴포넌트 계약 문서화
- R-08 로컬 개발 환경 문서화

### 이벤트 수집 및 스트리밍
- S-01 기준 event envelope 정의
- S-02 샘플 이벤트 fixture 추가
- S-03 단기 윈도우 Feature Contract 하나 정의
- S-04 대응 Stream Analytics 쿼리 구현
- S-05 예상 출력 fixture 추가
- S-06 누락/잘못된 이벤트 필드 검증 추가

### Lakehouse 데이터 엔지니어링
- D-01 Bronze landing 규칙 정의
- D-02 Bronze ingestion/read 구현
- D-03 Silver schema 정의
- D-04 Bronze → Silver 정규화 구현
- D-05 중복 제거 구현
- D-06 invalid record 처리 추가
- D-07 Silver 출력 unit/integration test 추가

### Feature Engineering
- F-01 과거 특성 하나 구현
- F-02 live feature 하나의 Databricks 재구성 구현
- F-03 point-in-time join utility 추가
- F-04 feature parity test 추가
- F-05 feature materialization/backfill 구현

### MLOps
- M-01 첫 버전 관리 학습 데이터셋 구축
- M-02 baseline model 추가
- M-03 MLflow experiment logging 추가
- M-04 evaluation metric 추가
- M-05 candidate vs current 비교 추가
- M-06 model registration 추가
- M-07 serving deployment 설정 추가
- M-08 serving smoke test 추가

### Batch Orchestration
- A-01 외부 batch source contract 정의
- A-02 Data Factory copy pipeline 하나 추가
- A-03 Databricks job trigger activity 추가
- A-04 rerun/idempotency 검증 추가

### Inference Integration
- I-01 live-feature request schema 정의
- I-02 request validation 구현
- I-03 Model Serving client 구현
- I-04 correlation ID와 structured error 추가
- I-05 end-to-end inference smoke test 추가

## 6인 팀 역할 소유권

Primary ownership은 독점 구현 권한이 아니라 기본 reviewer/maintainer를 의미합니다.

| 영역 | 권장 주 담당 |
|---|---|
| Event Hubs + Stream Analytics | Member 1 |
| ADLS + Data Factory | Member 2 |
| Databricks ingestion + Silver | Member 3 |
| Feature engineering + parity | Member 4 |
| Training + MLflow + evaluation | Member 5 |
| Serving + Function + CI/observability | Member 6 |

## PR 크기

권장:

```text
하나의 작업
  -> 하나의 브랜치
  -> 하나의 집중된 PR
  -> 독립적으로 이해 가능한 리뷰
```

`Databricks pipeline 구축`, `MLOps 구현`과 같은 항목은 작업이 아니라 Epic으로 보고 더 작은 단위로 분해합니다.
