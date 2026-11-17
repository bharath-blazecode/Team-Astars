"""Start the dashboard on this computer; no Git, Node or cloud forwarding is needed."""

import argparse
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import webbrowser


ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / "backend"
ENVIRONMENT = ROOT / ".dashboard-venv"


def port_available(port):
    with socket.socket() as listener:
        try:
            listener.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def existing_dashboard(url):
    try:
        with urlopen(url, timeout=2) as response:
            html = response.read(200_000).decode("utf-8", errors="replace")
            return "Westpac SpeedQ" in html and bool(
                re.search(r'class="brand-mark"[^>]*>\s*<svg\b', html)
            )
    except (HTTPError, URLError, TimeoutError, OSError):
        return False


def prepare_python():
    python = ENVIRONMENT / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.is_file():
        if ENVIRONMENT.exists():
            raise RuntimeError(
                "The .dashboard-venv folder is incomplete or belongs to another system. "
                "Rename that folder and run again; your backend database is separate."
            )
        print("Creating a local Python environment...", flush=True)
        subprocess.run([sys.executable, "-m", "venv", str(ENVIRONMENT)], check=True)
    ready = subprocess.run(
        [str(python), "-c", "import fastapi, uvicorn, pydantic, httpx, retell; "
         "assert int(pydantic.__version__.split('.')[0]) >= 2"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0
    if not ready:
        print("Installing project dependencies. First setup needs internet access.", flush=True)
        subprocess.run(
            [str(python), "-m", "pip", "install", "--disable-pip-version-check", "-r",
             str(BACKEND / "requirements.txt")],
            check=True,
        )
    return python


def open_page(url, disabled):
    if not disabled:
        try:
            if not webbrowser.open(url, new=2):
                print("Open the address above in your browser.", flush=True)
        except (OSError, webbrowser.Error):
            print("Open the address above in your browser.", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, help="Local port; defaults to 8010 or the next free port")
    parser.add_argument("--demo", action="store_true", help="Open the scripted customer scenarios")
    parser.add_argument("--no-browser", action="store_true", help="Print addresses without opening a tab")
    parser.add_argument("--db", type=Path, help="Optional separate SQLite file for a rehearsal")
    args = parser.parse_args()
    explicit_port = args.port is not None
    if args.port is None:
        args.port = 8010
    if sys.version_info < (3, 12):
        parser.error("Python 3.12 or newer is required. Install it from https://www.python.org/downloads/windows/")
    if not 1 <= args.port <= 65535:
        parser.error("Choose a port between 1 and 65535.")
    if not (BACKEND / "main.py").is_file() or not (ROOT / "frontend/index.html").is_file():
        parser.error("Extract the entire ZIP first, then run START_WINDOWS.cmd inside the extracted folder.")

    base = f"http://127.0.0.1:{args.port}"
    chosen = base + ("/demo" if args.demo else "/")
    if not port_available(args.port):
        if not args.db and existing_dashboard(base + "/"):
            print(f"Dashboard: {base}/\nScripted scenarios: {base}/demo", flush=True)
            print("The dashboard is already running on this computer.", flush=True)
            open_page(chosen, args.no_browser)
            return 0
        if explicit_port:
            raise RuntimeError(f"Port {args.port} is already in use. Choose another --port.")
        available = next((port for port in range(8011, 8021) if port_available(port)), None)
        if available is None:
            raise RuntimeError("Ports 8010-8020 are busy. Choose a free port with --port.")
        print(f"Port 8010 is busy; starting this preview on {available} instead.", flush=True)
        args.port = available
        base = f"http://127.0.0.1:{args.port}"
        chosen = base + ("/demo" if args.demo else "/")
    print(f"Dashboard: {base}/\nScripted scenarios: {base}/demo", flush=True)

    python = prepare_python()
    environment = os.environ.copy()
    if args.db:
        environment["NRY_DB"] = str(args.db.resolve())
    print("Starting SpeedQ locally. Keep this window open while using it.", flush=True)
    server = subprocess.Popen(
        [str(python), "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port",
         str(args.port), "--timeout-graceful-shutdown", "5"],
        cwd=BACKEND,
        env=environment,
    )
    try:
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            if server.poll() is not None:
                raise RuntimeError("The server stopped during startup. Read the error above.")
            try:
                with urlopen(base + "/", timeout=1) as response:
                    if response.status == 200:
                        break
            except HTTPError as error:
                # Configured staff authentication is preserved; the browser can show its sign-in prompt.
                if error.code == 401 and error.headers.get("WWW-Authenticate"):
                    break
            except (URLError, TimeoutError, OSError):
                pass
            time.sleep(0.2)
        else:
            raise RuntimeError("The dashboard did not become ready. Check startup errors and NRY_ALLOWED_HOSTS.")
        print("Ready. Use Load sample cases for synthetic cases, or choose Sam/Maria on /demo.", flush=True)
        print("The scripted scenarios work without Retell credentials. Live voice/chat needs your private settings.", flush=True)
        open_page(chosen, args.no_browser)
        return server.wait()
    except KeyboardInterrupt:
        print("\nStopping the local dashboard...", flush=True)
        return 0
    finally:
        if server.poll() is None:
            server.terminate()
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"\nCould not start SpeedQ: {error}", file=sys.stderr, flush=True)
        sys.exit(1)
