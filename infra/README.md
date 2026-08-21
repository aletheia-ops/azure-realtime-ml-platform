# Infrastructure as Code

[English](README.md) | [한국어](README.ko.md)

> English is the canonical documentation.

This directory is reserved for Azure infrastructure definitions. Bicep is the default recommendation for this Azure-focused project unless the team explicitly chooses Terraform.

Suggested structure:

```text
bicep/
  main.bicep
  modules/
parameters/
  dev.bicepparam
  prod.bicepparam
```

Resource definitions should be modular, parameterized by environment, and free of secrets. Deployment-specific credentials belong in managed identities, Key Vault, or CI/CD secret stores.
