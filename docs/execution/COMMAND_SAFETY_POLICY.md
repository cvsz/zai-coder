# Command Safety Policy

## Allowed executable examples

```text
python
python3
pytest
make
git
gh
cloudflared
docker
curl
echo
```

## Blocked patterns

```text
git add .
git add -A
--no-verify
push --force
docker system prune
rm -rf
sudo
su
```

## Working directory

Only safe relative working directories are accepted.
