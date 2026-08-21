# Infrastructure as Code

[English](README.md) | [한국어](README.ko.md)

> 영어 문서가 기준 문서입니다.

이 디렉터리는 Azure 인프라 정의를 관리합니다. Azure 중심 프로젝트이므로 팀에서 Terraform을 명시적으로 선택하지 않는 한 Bicep을 기본 권장안으로 사용합니다.

권장 구조:

```text
bicep/
  main.bicep
  modules/
parameters/
  dev.bicepparam
  prod.bicepparam
```

리소스 정의는 모듈화하고 환경별 파라미터를 사용하며 비밀값을 포함하지 않아야 합니다. 배포 자격 증명은 Managed Identity, Key Vault 또는 CI/CD secret store에서 관리합니다.
