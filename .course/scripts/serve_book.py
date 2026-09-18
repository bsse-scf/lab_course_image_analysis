#!/usr/bin/env python
"""Serve the pre-built Jupyter Book for the Course Book launcher.

jupyter-app-launcher starts this as a local-server subprocess and provides
a free listening port through $PORT.

The Jupyter Book is built during postBuild and copied to:

    /home/jovyan/project/_build/html

This script only serves that pre-built static site. The RRP server ID and
public proxy URL are handled by Jupyter/server-proxy and are intentionally
not referenced here.
"""

from __future__ import annotations

import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


HOST = "127.0.0.1"


def find_repo_root() -> Path:
    """Find the runtime repository root."""

    here = Path(__file__).resolve()

    # Expected:
    #   /home/jovyan/project/.course/scripts/serve_book.py
    for parent in (here.parent, *here.parents):
        if (parent / "pixi.toml").is_file():
            return parent

    # Explicit RRP runtime fallback.
    runtime_project = Path("/home/jovyan/project")
    if (runtime_project / "pixi.toml").is_file():
        return runtime_project

    # Local-development fallback.
    cwd = Path.cwd()
    if (cwd / "pixi.toml").is_file():
        return cwd

    raise RuntimeError(
        "Could not find repository root containing pixi.toml"
    )


class BookHandler(SimpleHTTPRequestHandler):
    """HTTP handler for the pre-built Jupyter Book."""

    def log_message(self, format, *args):
        print(
            f"Course Book HTTP: {format % args}",
            flush=True,
        )


def main() -> int:
    port = int(os.environ.get("PORT", "8000"))

    repo_root = find_repo_root()
    html_dir = repo_root / "_build" / "html"
    index_html = html_dir / "index.html"

    print("=== Course Book server ===", flush=True)
    print(f"Course Book repo: {repo_root}", flush=True)
    print(f"Course Book HTML: {html_dir}", flush=True)
    print(f"Course Book port: {port}", flush=True)

    if not html_dir.is_dir():
        print(
            f"ERROR: Course Book directory does not exist: {html_dir}",
            file=sys.stderr,
            flush=True,
        )
        return 1

    if not index_html.is_file():
        print(
            f"ERROR: Course Book index does not exist: {index_html}",
            file=sys.stderr,
            flush=True,
        )
        return 1

    print(
        f"Serving Course Book from {html_dir}",
        flush=True,
    )

    httpd = ThreadingHTTPServer(
        (HOST, port),
        lambda *args, **kwargs: BookHandler(
            *args,
            directory=str(html_dir),
            **kwargs,
        ),
    )

    httpd.daemon_threads = True

    print(
        f"Course Book available locally at "
        f"http://{HOST}:{port}/",
        flush=True,
    )

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Course Book server.", flush=True)
    finally:
        httpd.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
