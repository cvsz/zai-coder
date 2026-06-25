# Deploy Installer Guide

## 1. Validate source

```bash
python3 -m pytest -q
make verify-source-package
```

## 2. Dry-run install

```bash
./install.sh
make deploy-installer
make install-plan
```

## 3. Apply install

```bash
APPLY=1 ./install.sh
```

## 4. Local deployment

```bash
make deploy-local
make deploy-local APPLY=1
```

## 5. Docker deployment

```bash
make deploy-docker
make deploy-docker APPLY=1
```

## 6. Systemd deployment

```bash
make deploy-systemd
make deploy-systemd APPLY=1
```

## 7. Cloudflare

```bash
make deploy-cloudflare-plan DOMAIN=zai.zeaz.dev
```

Do not expose public DNS until Cloudflare Access is enabled.
