# Cloudflare Go-Live Guide

## 1. Validate hostname

```bash
make cloudflare-hostname-validate HOSTNAME=zai.zeaz.dev
```

## 2. Verify local service

```bash
make healthcheck
make production-smoke-plan
```

## 3. Generate tunnel plan/config

```bash
make cloudflare-tunnel-plan HOSTNAME=zai.zeaz.dev TUNNEL_NAME=zai-coder-control-plane
```

## 4. Configure Access

```bash
make cloudflare-access-checklist HOSTNAME=zai.zeaz.dev
```

Create a Cloudflare Access application and allow policy before DNS route.

## 5. DNS route plan

```bash
make cloudflare-dns-plan HOSTNAME=zai.zeaz.dev
```

## 6. Public verification plan

```bash
make cloudflare-public-health-plan HOSTNAME=zai.zeaz.dev
```

## 7. Rollback plan

```bash
make cloudflare-dns-rollback-plan HOSTNAME=zai.zeaz.dev
```
