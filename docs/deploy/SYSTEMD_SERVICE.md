# Systemd Service Guide

## Install dry-run

```bash
make systemd-install
```

## Install real

```bash
make systemd-install APPLY=1
```

## Safety

Review `deploy/systemd/zai-coder.service` before install.
