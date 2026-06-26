# CLI Diagnostics

## Purpose
The `zai-coder doctor` command provides environment and configuration diagnostics to assist operators in troubleshooting setup and runtime issues.

## Usage
```bash
zai-coder doctor
```

## Diagnostics Information
The doctor command checks and displays:
- **Config**: Current loaded configuration parameters.
- **Python**: Installed Python version.
- **Platform**: OS name and release.
- **Workspace**: Resolved workspace directory path.
- **Current Dir**: Current working directory of the CLI.
- **Workspace Status**: Writability of the workspace directory.
- **Ollama**: Location of the `ollama` executable and a list of available models if found.

## Troubleshooting
If `zai-coder doctor` indicates a problem:
- **Workspace Status NOT Writable**: Ensure the user has write permissions to the configured workspace directory.
- **Ollama not found**: If using local AI models, ensure Ollama is installed and in the system PATH.
