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

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
os.environ["PYTHONPATH"] = str(PROJECT_ROOT)

if __name__ == "__main__":
    # Render passes PORT dynamically (defaults to 10000 on Render if unset)
    port = os.environ.get("PORT", "10000")
    
    cmd = [
        sys.executable,
        "-m",
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
        "--browser.gatherUsageStats",
        "false",
    ]
    
    print(f"Starting Streamlit app on 0.0.0.0:{port}...")
    subprocess.run(cmd)
