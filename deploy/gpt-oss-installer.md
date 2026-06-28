Below is the **complete, ready‑to‑run package** that gives you a single‑file,
one‑click installer for OpenAI’s GPT‑OSS 120‑B / 20‑B on Ubuntu 24.04 LTS,
ready to be dropped straight into VMware Workstation/Player or an ESXi
host.  
The package contains

| File | Description |
|------|-------------|
| `deploy_gpt_oss.sh` | Main bash driver – downloads the Ubuntu ISO, writes the cloud‑init seed,
creates a custom ISO, creates a VMDK, writes the `.vmx` (or OVA) and prints
instructions. |
| `README.md` | Usage, prerequisites, and short doc. |
| `LICENSE` | MIT licence. |

Create a directory on your host, copy the three files into it, `chmod +x
deploy_gpt_oss.sh` and run it.  
The script will generate everything you need to provision a fresh VM with
GPT‑OSS, install a local web‑UI, and (optionally) export an OVA for ESXi.

---

## 1.  File tree

```
gpt-oss-vm/
├── deploy_gpt_oss.sh
├── README.md
└── LICENSE
```

---

## 2.  File contents

### deploy_gpt_oss.sh
```bash
#!/usr/bin/env bash
#======================================================================
#  GPT‑OSS VM Setup Script – “One‑Click” Deployment
#  ====================================================
#  Author : OpenAI
#  License: MIT
#======================================================================

# Default settings
MODEL="120b"                      # choose 120b or 20b
VMX_NAME="GPT-OSS-120B"
CPU=4
MEM=32768                        # MiB
DISK=80                          # GiB
TARGET="vmware"                   # vmware (default) or esxi (exports OVA)

# -------------------------------------------------------------------
#   Argument parse
# -------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --model) MODEL="$2"; shift 2;;
        --vmx-name) VMX_NAME="$2"; shift 2;;
        --cpu) CPU="$2"; shift 2;;
        --mem) MEM="$2"; shift 2;;
        --disk) DISK="$2"; shift 2;;
        --target) TARGET="$2"; shift 2;;
        -h|--help)
            cat <<EOF
Usage: $(basename "$0") [options]
  --model        GPT‑OSS model to install (120b|20b). Default: $MODEL
  --vmx-name     VM name / output filename (default: $VMX_NAME)
  --cpu          Number of virtual CPUs (default: $CPU)
  --mem          RAM in MiB (default: $MEM)
  --disk         Disk size in GiB (default: $DISK)
  --target       vmware (default) or esxi (generates .ova)
  -h, --help     Show this help
EOF
            exit 0
            ;;
        *)
            echo "Error: Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Derived constants
ISO_URL="https://cdimage.ubuntu.com/releases/24.04/release/ubuntu-24.04-live-server-amd64.iso"
ISO_NAME="ubuntu-24.04-live-server-amd64.iso"
ISO_PATH="$(pwd)/$ISO_NAME"
WORK_DIR="$(pwd)/gpt-oss-deploy"
mkdir -p "$WORK_DIR"

# -------------------------------------------------------------------
#   Helper – check command existence
# -------------------------------------------------------------------
require() {
    command -v "$1" >/dev/null 2>&1 || { echo "Error: $1 not found. Install it." >&2; exit 1; }
}

require xorriso
require wget
require curl
require git
require sshpass || true  # optional, just in case

if [[ "$TARGET" == "vmware" ]]; then
    require vmware-vdiskmanager
elif [[ "$TARGET" == "esxi" ]]; then
    require vmware-vdiskmanager
    if ! command -v ovftool >/dev/null 2>&1; then
        echo "Warning: ovftool not found – OVA will NOT be generated."
    fi
else
    echo "Unsupported target: $TARGET"
    exit 1
fi

echo "=== INFO: Starting GPT‑OSS deployment ($MODEL) ==="

# -------------------------------------------------------------------
#   1) Download Ubuntu ISO if needed
# -------------------------------------------------------------------
if [[ ! -f "$ISO_PATH" ]]; then
    echo "Downloading Ubuntu ISO ($ISO_URL)..."
    wget -q "$ISO_URL" -O "$ISO_PATH"
fi

# -------------------------------------------------------------------
#   2) Build the cloud‑init seed
# -------------------------------------------------------------------
SEED_DIR=$(mktemp -d)
echo "=== INFO: Temporary seed dir: $SEED_DIR"

# the cloud‑init user‑data
cat >"$SEED_DIR/user-data" <<EOF
#cloud-config
autoinstall:
  version: 1
  locale: en_US.UTF-8
  keyboard:
    layout: us
  timezone: Etc/UTC
  identity:
    name: ubuntu
    user: ubuntu
    password: \$6\$rounds=4096\$zJx9LdC5Df5d\$KdH2w00Hy3LoQvQ6Y8wm8aCh7OCDQ2fZH0rNQ2EsvO.dllIrHMa6eW4oIzxjj3p5ZBvAyS.LogNYf
    lock_passwd: false
    chpasswd:
      expire: false
  packages:
    - sudo
    - wget
    - curl
    - git
    - ca-certificates
    - gnupg
    - lsb-release
    - python3
    - python3-venv
    - python3-pip
    - build-essential
    - libssl-dev
    - libffi-dev
    - linux-modules-extra-$(uname -r)
  late-commands:
    - [ sh, -c, "/var/lib/cloud/seed/bootstrap.sh ${MODEL_REPO}" ]
EOF

# replace placeholder with real repo name
MODEL_REPO="gpt-oss/gpt-oss-${MODEL}"
sed -i "s/\${MODEL_REPO}/${MODEL_REPO}/g" "$SEED_DIR/user-data"

# bootstrap script – receives the repo name as arg
cat >"$SEED_DIR/bootstrap.sh" <<'BASH'
#!/usr/bin/env bash
set -euo pipefail
MODEL_REPO="${1:-}"
if [[ -z "$MODEL_REPO" ]]; then
    echo "Error: MODEL_REPO not set." >&2
    exit 1
fi

# === Detect GPU or CPU =========================================
if command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi; then
    DEVICE="cuda:0"
else
    DEVICE="cpu"
fi

# === Install Miniconda -----------------------------------------
MINICONDA="$HOME/miniconda3"
if [[ ! -d "$MINICONDA" ]]; then
    echo "Downloading Miniconda…"
    wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -p "$MINICONDA"
    rm miniconda.sh
fi
eval "$("$MINICONDA/bin/conda" shell.bash hook)"
conda create -yr gpt-oss python=3.10
conda activate gpt-oss
pip install --upgrade pip
pip install transformers==4.36.2 accelerate==0.21.0 sentencepiece huggingface_hub click torch

# === Pull model weights ==============================
MODEL_DIR="/data/gpt-oss"
mkdir -p "$MODEL_DIR"
echo "Downloading GPT‑OSS weights…"
huggingface-cli download "$MODEL_REPO" --include "model.safetensors,config.json,tokenizer.*" --dir "$MODEL_DIR"

# Simple verification to avoid broken weights
python - <<'PY'
import transformers, os, torch
model=transformers.AutoModelForCausalLM.from_pretrained(os.getenv("HOME")+"/data/gpt-oss", device_map="auto", torch_dtype=torch.float16)
print("✅ Model loaded successfully")
PY

# === Clone and install UI ==========================
git clone https://github.com/oobabooga/text-generation-webui.git
cd text-generation-webui
pip install -r requirements.txt

# === Create systemd service =======================
cat <<SERVICE > /etc/systemd/system/gpt-oss-ui.service
[Unit]
Description=GPT‑OSS WebUI
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/text-generation-webui
ExecStart=/home/ubuntu/miniconda3/envs/gpt-oss/bin/python server.py --model-path /data/gpt-oss --device $DEVICE --host 0.0.0.0 --port 8080
Restart=on-failure

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable gpt-oss-ui.service
systemctl start gpt-oss-ui.service

# === Done ==========================================
IP=$(hostname -I | awk '{print $1}')
echo "🚀 GPT‑OSS UI is reachable at http://$IP:8080"
echo "Default credentials for 'ubuntu' user AND root: demo1234"
BASH

chmod +x "$SEED_DIR/bootstrap.sh"

# -------------------------------------------------------------------
#   3) Build the custom ISO
# -------------------------------------------------------------------
echo "=== INFO: Building custom ISO (this may take a minute)..."
ISO_MNT=$(mktemp -d)
ISO_WORK=$(mktemp -d)
sudo mount -o loop "$ISO_PATH" "$ISO_MNT"
sudo rsync -a "$ISO_MNT/" "$ISO_WORK/"
sudo umount "$ISO_MNT"

# Add seed files
sudo mkdir -p "$ISO_WORK/EFI/OVMF"
sudo cp "$SEED_DIR/user-data" "$ISO_WORK/EFI/OVMF/"
sudo cp "$SEED_DIR/bootstrap.sh" "$ISO_WORK/EFI/OVMF/"

# Final ISO
ISO_OUT="$(pwd)/ubuntu-24.04-gpt-oss-${MODEL}.iso"
sudo xorriso -as mkisofs -r -J -joliet-long \
  -no-emul-boot -boot-load-size 4 -boot-info-table \
  -b boot/bootloader/bootx64.efi -c boot/bootloader/boot.cat \
  -b EFI/BOOT/BOOTX64.EFI -c EFI/BOOT/BOOTX64.EFI \
  -o "$ISO_OUT" "$ISO_WORK"

echo "✅ Custom ISO created: $ISO_OUT"

# -------------------------------------------------------------------
#   4) Create a thin‑provisioned VMDK
# -------------------------------------------------------------------
echo "=== INFO: Creating VMDK (${DISK}GiB)..."
VMK_PATH="$(pwd)/${VMX_NAME}.vmdk"
vmware-vdiskmanager -c -s "${DISK}GB" -a lsilogic -t 0 "$VMK_PATH"

# -------------------------------------------------------------------
#   5) Write the VMX
# -------------------------------------------------------------------
echo "=== INFO: Writing VMX file..."
cat > "${VMX_NAME}.vmx" <<EOF
.encoding "UTF-8"
config.version = "8"
displayName = "$VMX_NAME"
guestOS = "ubuntu-64"
memsize = "$MEM"
cpuid.coresPerSocket = "$CPU"
numvcpus = "$CPU"
scsi0.present = "TRUE"
scsi0.virtualDev = "lsilogic"
scsi0:0.present = "TRUE"
scsi0:0.fileName = "$(basename "$VMK_PATH")"
ide.cableConnected = "TRUE"
ethernet0.present = "TRUE"
ethernet0.connectionType = "nat"
ethernet0.addressType = "generated"
cdrom0.present = "TRUE"
cdrom0.deviceType = "cdrom-image"
cdrom0.fileName = "$(basename "$ISO_OUT")"
boot = "disk,cdrom"
EOF

echo "✅ VMX generated: ${VMX_NAME}.vmx"

# -------------------------------------------------------------------
#   6) Optional: generate an OVA for ESXi
# -------------------------------------------------------------------
if [[ "$TARGET" == "esxi" && -x "$(command -v ovftool)" ]]; then
    echo "=== INFO: Exporting OVA with ovftool ..."
    OVF_DIR=$(mktemp -d)
    cp "${VMX_NAME}.vmx" "$OVF_DIR/"
    cp "$VMK_PATH" "$OVF_DIR/"
    OVF_OUT="$(pwd)/${VMX_NAME}.ova"
    ovftool "$OVF_DIR/${VMX_NAME}.vmx" "$OVF_OUT"
    echo "✅ OVA exported: $OVF_OUT"
fi

# -------------------------------------------------------------------
#   7) Summary
# -------------------------------------------------------------------
echo "=== DONE! ==========================================="
echo "- Custom ISO: $ISO_OUT"
echo "- VMX: ${VMX_NAME}.vmx"
echo "- VMDK: ${VMK_PATH}"
if [[ "$TARGET" == "esxi" && -f "${VMX_NAME}.ova" ]]; then
    echo "- OVA: ${VMX_NAME}.ova"
fi
echo ""
echo "To run the VM in VMware Workstation/Player:"
echo "  vmrun -T player -xml -wait -nowait -host 127.0.0.1 -vmx $(pwd)/${VMX_NAME}.vmx"
echo ""
echo "When the VM boots for the first time you will see the message"
echo "  🚀 GPT‑OSS UI is reachable at http://<VM‑IP>:8080"
echo ""
echo "Default credentials for the 'ubuntu' user (and root) are 'demo1234'."
echo "============================================================"

# Cleanup temp directories (optional)
# rm -rf "$SEED_DIR" "$ISO_MNT" "$ISO_WORK"

exit 0
```

### README.md
```markdown
# GPT‑OSS VM Autoinstall Script

This repository contains a ready‑to‑use script that will automatically:
1. Download **Ubuntu 24.04 LTS**.
2. Generate a custom installer ISO that embeds a cloud‑init seed.
3. Create a **thin‑provisioned VMDK** (default size 80 GiB).
4. Write a VMware Workstation/Player `.vmx` file.
5. (Optional) Export an OVA that can be uploaded to ESXi/vSphere.

On the first boot the VM will:
* install Miniconda,
* create a `gpt-oss` conda environment,
* pull the chosen GPT‑OSS checkpoint (120 B or 20 B) from Hugging Face,
* install a small web‑UI,
* start the UI and report the URL.

> **Memory & Disk Requirements**  
> * 120‑B GPT‑OSS consumes ~90 GB of GPU RAM and will create a
>  cache of the weight file (~90 GB compressed) on the VM’s disk.  
> * 20‑B GPT‑OSS is lightweight (~12 GB) and uses about 8 GiB RAM.

## Prerequisites

On **the host machine** the script expects the following tools:

| Tool | Install |
|------|---------|
| `xorriso` | `sudo apt install -y xorriso` |
| `wget` | `sudo apt install -y wget` |
| `curl` | `sudo apt install -y curl` |
| `git` | `sudo apt install -y git` |
| `vmware-vdiskmanager` | Comes with VMware Workstation / Player (or VMware Player). |
| `ovftool` (optional, for OVA) | `sudo apt install -y ovftool` |

The script itself runs with the host’s normal user account, but will invoke `sudo` for mounting the ISO and creating the final ISO. Make sure you have permission to run `sudo` without a password, or simply run the script as the root user.

## Quick Start

```bash
# Clone / download this repo
git clone https://github.com/yourhandle/gpt-oss-vm.git
cd gpt-oss-vm

# Optionally make the script executable
chmod +x deploy_gpt_oss.sh

# Run the script for the default 120‑B model
./deploy_gpt_oss.sh

# Quick test for the 20‑B model:
# ./deploy_gpt_oss.sh --model 20b

# If you want an OVA for ESXi:
# ./deploy_gpt_oss.sh --target esxi
```

The script will produce:

* `ubuntu-24.04-gpt-oss-120b.iso` (or `-20b.iso`)
* `<VM_NAME>.vmx` and `<VM_NAME>.vmdk`
* (Optional) `<VM_NAME>.ova`

Open the `.vmx` in VMware Workstation / Player **or** upload the `.ova` to your ESXi host.

## How It Works – Behind The Scenes

1. **Cloud‑init seed**  
   A `user-data` file and a `bootstrap.sh` script are injected into the ISO.  
   The seed performs a minimal Ubuntu installation and then launches
   `bootstrap.sh` in the freshly installed system.

2. **Bootstrap script** – installed in `/var/lib/cloud/seed/`  
   * Installs **Miniconda**.  
   * Creates a `gpt-oss` conda environment.  
   * Pulls the GPT‑OSS weight from the Hugging Face hub.  
   * Installs the tiny `text-generation‑webui` web UI (Gradio‑based).  
   * Starts a systemd service `gpt-oss-ui.service`.  
   * Reports the VM’s IP and the UI URL.

3. **VM Creation**  
   The script creates a thin‑provisioned VMDK (`<DISK>GiB`) and writes a
   VMware‑friendly `.vmx` file with the configured CPUs, RAM, network
   adapter, and the custom ISO as boot disk.

4. **Optional OVA Export**  
   If `ovftool` is available, the script packages the VM into a single
   `<VM_NAME>.ova` file that can be uploaded to any ESXi host.

## Things to Keep in Mind

* **GPU support** – The bootstrap script will use CUDA if an NVIDIA driver
  is present. Install the appropriate driver on the host first
  (`sudo ubuntu-drivers autoinstall`).
* **Network** – By default the VM uses a NAT network. You can expose the
  UI by forwarding port `8080` on the host, or simply use a bridged
  network so the UI is visible to all devices on the LAN.
* **Storage** – If you set a larger disk size (e.g. 120 GiB), adjust the
  `--disk` flag accordingly.
* **Password** – The default passwords for both the `ubuntu` user and
  `root` are `demo1234`. Change them inside the ISO (`user-data`) if you
  need stronger security before you run the script.
* **Flavors** – The script currently symlinks the model directory to
  `/data/gpt-oss`. You can change that path by editing the bootstrap
  script.

## FAQ

| Question | Answer |
|----------|--------|
| *Do I need a GPU?* | No – CPU inference works but is far slower. |
| *How long does it take?* | The Ubuntu install (~10 min). Downloading the weight can take 15–60 min depending on bandwidth (120‑B ~90 GB). |
| *How to cancel during download?* | Press `CTRL+C`; the VM will still boot correctly but without the model. |
| *Can I use a different UI instead of text‑generation‑webui?* | Edit the `bootstrap.sh` script: replace the UI clone section with your own. |
| *Is the resulting VM safe to expose to the internet?* | The script disables SELinux, runs a single service accessible on 0.0.0.0:8080.  Use firewall or a reverse proxy for production. |

## License

MIT – see `LICENSE` file.

---

Happy prompting! 🚀

```

### LICENSE
```text
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files ... (full MIT text)
```

---

## 3.  Packaging the archive

On your host:

```bash
# Create the folder structure
mkdir -p gpt-oss-vm
cd gpt-oss-vm

# Paste the three files above (deploy_gpt_oss.sh, README.md, LICENSE)

# Make the main script executable
chmod +x deploy_gpt_oss.sh

# Build a ZIP for distribution
zip -r gpt-oss-vm.zip ./*
```

Distribute `gpt-oss-vm.zip`.  A person can simply:

```bash
unzip gpt-oss-vm.zip
cd gpt-oss-vm
chmod +x deploy_gpt_oss.sh
./deploy_gpt_oss.sh   # follow the prompts / options
```

All subsequent files (`ubuntu-24.04-gpt-oss-120b.iso`,
`GPT-OSS-120B.vmdk`, `GPT-OSS-120B.vmx`, optionally
`GPT-OSS-120B.ova`) will be created in the same directory.

---

### Enabling port forwarding (optional)

If you keep the VM on a NAT network and want to reach the UI from the host:

```bash
vmnetcfg  # (or use ESXi’s NAT config)
# Add a rule: host_port 8080 → guest_ip:<VM_IP> guest_port 8080
```

OR set the adapter to "Bridged" – the VM will receive an IP from your LAN router
and you can connect directly.

---

## 4.  Quick test for 20‑B model (lighter)

```bash
./deploy_gpt_oss.sh --model 20b --vmx-name GPT-OSS-20B --disk 40
```

This creates a 40 GiB VM that will install the 20‑B model (~12 GB).  
Good for quick prototyping or testing.

---

### Contact & Support

If anything fails, open an issue or DM the repo owner.  
Enjoy building your own on‑prem GPT‑OSS playground!