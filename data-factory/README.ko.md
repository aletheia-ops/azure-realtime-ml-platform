# Azure Data Factory

[English](README.md) | [한국어](README.ko.md)

> 영어 문서가 기준 문서입니다.

이 디렉터리는 배치 수집과 상위 수준 오케스트레이션에 사용되는 Data Factory 아티팩트를 버전 관리합니다.

예정된 하위 디렉터리:

```text
pipelines/
datasets/
linked-services/
triggers/
```

Data Factory는 배치 데이터를 이동하고 예약 작업을 조정하는 역할을 담당합니다. 대규모 변환은 Databricks가 담당하며, 저지연 추론 경로에는 ADF를 사용하지 않습니다.

비밀값이나 환경별 자격 증명 export 파일은 커밋하지 않습니다.
