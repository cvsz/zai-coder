# Security Policy

## Never commit

```text
.env
.env.*
*.pem
*.key
credentials.json
creds.json
service-account*.json
*.tfstate
terraform.tfvars
apps/zlms/**
```

## Safety model

ZAI Coder is dry-run-first. External integrations generate plans by default. Execution requires explicit operator approval.
