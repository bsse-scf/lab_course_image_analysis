#!/usr/bin/env python
"""Serve the pre-built Jupyter Book for the "Course Book" launcher entry.

Started by jupyter-app-launcher (see .jupyter/jp_app_launcher.yml) as a
`local-server` subprocess. jupyter-app-launcher puts a free port in $PORT and
polls http://localhost:$PORT/ for up to 120 s, proxying it through
jupyter-server-proxy at <base_url>/proxy/<port>/.

Jupyter Book v1 (Sphinx) emits *relative* links, so serving _build/html behind
that /proxy/<port>/ prefix needs no base-url rewriting.

Uses only the standard library, so it runs in the default pixi env (which has
no jupyter-book). If the book is not built yet it is built on demand with the
`docs` pixi env; meanwhile an auto-refreshing placeholder is served so the
launcher's poll succeeds immediately.
"""
from __future__ import annotations

import functools
import os
import shutil
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST = "127.0.0.1"
STATE = {"phase": "building"}  # building | error


def find_repo_root() -> Path:
    here = Path(__file__).resolve()  # <repo>/.course/scripts/serve_book.py
    for parent in (here.parent, *here.parents):
        if (parent / "pixi.toml").exists() or (parent / "book" / "_toc.yml").exists():
            return parent
    for cand in (Path.cwd(), Path.home() / "project", Path.home()):
        if (cand / "pixi.toml").exists():
            return cand
    return here.parent


def docs_jupyter_book(repo_root: Path):
    """A jupyter-book from the `docs` env, found without needing pixi on PATH
    (RRP: the env lives at $PIXI_ROOT / ~/pixi-env, not under the repo)."""
    roots = []
    if os.environ.get("PIXI_ROOT"):
        roots.append(Path(os.environ["PIXI_ROOT"]))
    roots += [Path.home() / "pixi-env", repo_root]
    for root in roots:
        base = root / ".pixi" / "envs" / "docs"
        for exe in (base / "bin" / "jupyter-book",
                    base / "Scripts" / "jupyter-book.exe"):
            if exe.exists():
                return [str(exe)]
        for py in (base / "bin" / "python", base / "python.exe"):
            if py.exists():
                return [str(py), "-m", "jupyter_book"]
    return None


def build_book(repo_root: Path) -> bool:
    cfg = repo_root / "book" / "_config.yml"
    toc = repo_root / "book" / "_toc.yml"
    build_args = ["build", str(repo_root), "--config", str(cfg),
                  "--toc", str(toc), "--all"]

    jb = docs_jupyter_book(repo_root)
    if jb is not None:
        cmd = jb + build_args
    elif shutil.which("pixi") is not None:
        cmd = ["pixi", "run", "-e", "docs", "book"]      # local clone
    elif shutil.which("jupyter-book") is not None:
        cmd = ["jupyter-book"] + build_args
    else:
        sys.stderr.write("Course Book: jupyter-book not found. "
                         "Build it once with `pixi run book`.\n")
        return False

    print("Building the Course Book (can take a minute)...", flush=True)
    print("  " + " ".join(cmd), flush=True)
    try:
        subprocess.run(cmd, cwd=str(repo_root), check=True)
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(f"Course Book build failed: {exc}\n")
        return False
    return True


class PlaceholderHandler(BaseHTTPRequestHandler):
    def _page(self) -> bytes:
        if STATE["phase"] == "error":
            body = ("<h1>Course Book could not be built</h1>"
                    "<p>Run <code>pixi run book</code> in a terminal and "
                    "check the log, then reopen this entry.</p>")
            refresh = ""
        else:
            body = ("<h1>Building the Course Book&hellip;</h1>"
                    "<p>This page refreshes automatically.</p>")
            refresh = '<meta http-equiv="refresh" content="2">'
        return (f"<!doctype html><html><head><meta charset='utf-8'>{refresh}"
                f"<title>Course Book</title>"
                f"<style>body{{font-family:sans-serif;margin:4rem;color:#333}}</style>"
                f"</head><body>{body}</body></html>").encode()

    def do_GET(self):
        page = self._page()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, *a):
        pass


def main() -> int:
    port = int(os.environ.get("PORT", "8000"))
    repo_root = find_repo_root()
    html_dir = repo_root / "_build" / "html"

    httpd = ThreadingHTTPServer((HOST, port), PlaceholderHandler)
    httpd.daemon_threads = True

    def serve_static():
        httpd.RequestHandlerClass = functools.partial(
            SimpleHTTPRequestHandler, directory=str(html_dir))

    if (html_dir / "index.html").exists():
        serve_static()
        print(f"Serving Course Book from {html_dir} on {HOST}:{port}", flush=True)
    else:
        def worker():
            if build_book(repo_root) and (html_dir / "index.html").exists():
                serve_static()
                print(f"Course Book ready; serving {html_dir}", flush=True)
            else:
                STATE["phase"] = "error"
        threading.Thread(target=worker, daemon=True).start()
        print(f"Building Course Book; placeholder on {HOST}:{port}", flush=True)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())