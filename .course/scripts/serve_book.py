#!/usr/bin/env python
"""Serve the pre-built Jupyter Book for the Course Book launcher.

The jupyter-app-launcher starts this as a local-server subprocess and provides
a free listening port through $PORT.

If the book has already been built, it is served immediately.

If it has not been built, a lightweight placeholder is served immediately
while the Jupyter Book is built in the Pixi `docs` environment. Once the build
finishes, subsequent requests are served from book/_build/html.
"""

from __future__ import annotations

import functools
import os
import subprocess
import sys
import threading
from http.server import (
    BaseHTTPRequestHandler,
    SimpleHTTPRequestHandler,
    ThreadingHTTPServer,
)
from pathlib import Path


HOST = "127.0.0.1"

STATE = {
    "phase": "building",  # building | ready | error
}


def find_repo_root() -> Path:
    """Find the repository root from this script's location."""

    here = Path(__file__).resolve()

    # Expected:
    #   <repo>/.course/scripts/serve_book.py
    for parent in (here.parent, *here.parents):
        if (parent / "pixi.toml").exists():
            return parent

    # Runtime fallbacks.
    for candidate in (
        Path.cwd(),
        Path("/home/jovyan/project"),
        Path.home() / "project",
    ):
        if (candidate / "pixi.toml").exists():
            return candidate

    raise RuntimeError(
        "Could not find repository root containing pixi.toml"
    )


def docs_jupyter_book(repo_root: Path) -> list[str] | None:
    """Find jupyter-book inside the Pixi docs environment."""

    pixi_root = Path(
        os.environ.get("PIXI_ROOT", str(Path.home() / "pixi-env"))
    )

    env = pixi_root / ".pixi" / "envs" / "docs"

    candidates = [
        env / "bin" / "jupyter-book",
        env / "bin" / "jb",
        env / "Scripts" / "jupyter-book.exe",
        env / "Scripts" / "jb.exe",
    ]

    for executable in candidates:
        if executable.exists():
            return [str(executable)]

    python_candidates = [
        env / "bin" / "python",
        env / "python.exe",
    ]

    for python in python_candidates:
        if python.exists():
            return [str(python), "-m", "jupyter_book"]

    return None


def build_book(repo_root: Path) -> bool:
    """Build the Jupyter Book using the Pixi docs environment."""

    book_dir = repo_root / "book"
    config = book_dir / "_config.yml"
    toc = book_dir / "_toc.yml"

    if not config.exists():
        print(f"Course Book: missing {config}", file=sys.stderr, flush=True)
        return False

    if not toc.exists():
        print(f"Course Book: missing {toc}", file=sys.stderr, flush=True)
        return False

    jupyter_book = docs_jupyter_book(repo_root)

    if jupyter_book is None:
        print(
            "Course Book: jupyter-book was not found in the Pixi docs "
            "environment.",
            file=sys.stderr,
            flush=True,
        )
        print(
            "Expected environment: "
            f"{os.environ.get('PIXI_ROOT', str(Path.home() / 'pixi-env'))}"
            "/.pixi/envs/docs",
            file=sys.stderr,
            flush=True,
        )
        return False

    cmd = jupyter_book + [
        "build",
        str(book_dir),
        "--config",
        str(config),
        "--toc",
        str(toc),
        "--all",
    ]

    print(
        "Building the Course Book (this can take a minute)...",
        flush=True,
    )
    print("  " + " ".join(cmd), flush=True)

    try:
        subprocess.run(
            cmd,
            cwd=str(repo_root),
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(
            f"Course Book build failed with exit code {exc.returncode}",
            file=sys.stderr,
            flush=True,
        )
        return False

    return True


class PlaceholderHandler(BaseHTTPRequestHandler):
    """Respond immediately while the book is being built."""

    def _page(self) -> bytes:
        phase = STATE["phase"]

        if phase == "error":
            body = """
                <h1>Course Book could not be built</h1>
                <p>
                  Run <code>pixi run book</code> in a terminal and inspect
                  the build output.
                </p>
            """
            refresh = ""

        elif phase == "ready":
            # This normally won't be reached because the server swaps its
            # request handler, but it makes the state safe.
            body = """
                <h1>Course Book ready</h1>
            """
            refresh = ""

        else:
            body = """
                <h1>Building the Course Book&hellip;</h1>
                <p>This page will refresh automatically.</p>
            """
            refresh = '<meta http-equiv="refresh" content="2">'

        return f"""
            <!doctype html>
            <html>
              <head>
                <meta charset="utf-8">
                {refresh}
                <title>Course Book</title>
                <style>
                  body {{
                    font-family: sans-serif;
                    margin: 4rem;
                    color: #333;
                  }}
                </style>
              </head>
              <body>
                {body}
              </body>
            </html>
        """.encode()

    def do_GET(self):
        page = self._page()

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8",
        )
        self.send_header(
            "Content-Length",
            str(len(page)),
        )
        self.end_headers()

        self.wfile.write(page)

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, *_args):
        pass


def main() -> int:
    port = int(os.environ.get("PORT", "8000"))

    repo_root = find_repo_root()

    book_dir = repo_root / "book"
    html_dir = book_dir / "_build" / "html"
    index_html = html_dir / "index.html"

    print(f"Course Book repo: {repo_root}", flush=True)
    print(f"Course Book source: {book_dir}", flush=True)
    print(f"Course Book HTML: {html_dir}", flush=True)
    print(f"Course Book port: {port}", flush=True)

    httpd = ThreadingHTTPServer(
        (HOST, port),
        PlaceholderHandler,
    )
    httpd.daemon_threads = True

    def use_static_handler():
        httpd.RequestHandlerClass = functools.partial(
            SimpleHTTPRequestHandler,
            directory=str(html_dir),
        )

    if index_html.exists():
        STATE["phase"] = "ready"
        use_static_handler()

        print(
            f"Serving existing Course Book from {html_dir} "
            f"on {HOST}:{port}",
            flush=True,
        )

    else:

        def worker():
            try:
                success = build_book(repo_root)

                if success and index_html.exists():
                    STATE["phase"] = "ready"
                    use_static_handler()

                    print(
                        f"Course Book ready; serving {html_dir}",
                        flush=True,
                    )
                else:
                    STATE["phase"] = "error"

                    print(
                        "Course Book build completed but "
                        f"{index_html} was not created.",
                        file=sys.stderr,
                        flush=True,
                    )

            except Exception as exc:
                STATE["phase"] = "error"

                print(
                    f"Course Book worker failed: {exc}",
                    file=sys.stderr,
                    flush=True,
                )

        threading.Thread(
            target=worker,
            daemon=True,
            name="course-book-builder",
        ).start()

        print(
            f"Building Course Book; placeholder available "
            f"on {HOST}:{port}",
            flush=True,
        )

    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        pass

    finally:
        httpd.shutdown()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())