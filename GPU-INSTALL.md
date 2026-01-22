GPU vs CPU install

- CPU-only (recommended for macOS / no CUDA):

```bash
python -m pip install -r requirements.txt
```

- GPU (Linux with CUDA drivers and compatible NVIDIA hardware):

```bash
python -m pip install -r requirements.txt -r requirements-gpu.txt
```

Notes:
- `torch` wheels vary by platform and Python version. On macOS newer Python versions (3.13/3.14) prebuilt wheels may be unavailable. If `pip install torch` fails, follow the official instructions at https://pytorch.org/get-started/locally/ to install the correct wheel or use a compatible Python version (e.g., 3.11/3.12).
- Create and activate a virtual environment before installing.
- GPU packages require matching CUDA toolkit and drivers; install them via your system package manager or NVIDIA's installers.
- If a package in `requirements-gpu.txt` fails to install, verify your CUDA/toolkit versions and consult the package docs.
