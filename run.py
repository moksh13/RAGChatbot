"""Runner script for launching the Streamlit app on Render or local servers.

Safely handles:
- Dynamic port assignment via Render's $PORT environment variable.
- Binding to 0.0.0.0 for external web routing.
- Disabling CORS and XSRF restrictions for stable WebSocket connections.
- Adding repository root to sys.path and PYTHONPATH.
"""

import os
import sys
import subprocess
from pathlib import Path

# Enforce strict memory-saving controls for Render (512MB RAM limit)
os.environ["MALLOC_ARENA_MAX"] = "2"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
os.environ["PYTHONPATH"] = str(PROJECT_ROOT)

if __name__ == "__main__":
    import streamlit.web.cli as stcli

    # Render passes PORT dynamically (defaults to 10000 on Render if unset)
    port = os.environ.get("PORT", "10000")
    print(f"Starting Streamlit app in-process on 0.0.0.0:{port}...")

    sys.argv = [
        "streamlit",
        "run",
        str(PROJECT_ROOT / "src" / "app.py"),
        "--server.port",
        str(port),
        "--server.address",
        "0.0.0.0",
        "--server.headless",
        "true",
        "--server.enableCORS",
        "false",
        "--server.enableXsrfProtection",
        "false",
        "--server.fileWatcherType",
        "none",
        "--browser.gatherUsageStats",
        "false",
    ]
    sys.exit(stcli.main())
