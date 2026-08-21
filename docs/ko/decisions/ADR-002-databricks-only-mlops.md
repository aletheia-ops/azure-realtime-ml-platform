# ADR-002: Databricks 단독 MLOps 사용

[English](../../en/decisions/ADR-002-databricks-only-mlops.md) | [한국어](../../ko/decisions/ADR-002-databricks-only-mlops.md)

> 영어 문서가 기준 문서입니다.

## 상태
승인됨

## 결정
특성 관리, 모델 학습, 실험 추적, 모델 등록, 거버넌스, 온라인 모델 서빙을 Azure Databricks에서 수행합니다. Databricks로 요구사항을 깔끔하게 충족할 수 없는 구체적인 필요가 생기기 전까지 Azure Machine Learning을 추가하지 않습니다.

## 근거
6인 단일 팀 환경에서 Azure ML을 추가하면 현재 명확한 이점 없이 플랫폼 경계만 늘어날 수 있습니다. Databricks는 MLflow, Unity Catalog, feature tooling, Jobs, Model Serving을 통해 필요한 MLOps 수명주기를 이미 제공합니다.

## 결과
- MLflow를 기본 실험 추적 도구로 사용합니다.
- Unity Catalog를 모델 레지스트리/거버넌스 계층으로 사용합니다.
- Databricks Model Serving을 운영 추론 endpoint로 사용합니다.
- Azure ML은 기본 의존성이 아니라 향후 선택 가능한 통합 요소로 남깁니다.
