"""Behave environment: serves the mock UI and manages the Playwright browser."""

import http.server
import os
import socketserver
import threading
from functools import partial

from playwright.sync_api import sync_playwright

MOCK_UI_DIR = os.path.join(os.path.dirname(__file__), "..", "mock-ui")
PORT = int(os.environ.get("MOCK_UI_PORT", "8123"))


def before_all(context):
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=MOCK_UI_DIR)
    socketserver.TCPServer.allow_reuse_address = True
    context.httpd = socketserver.TCPServer(("", PORT), handler)
    threading.Thread(target=context.httpd.serve_forever, daemon=True).start()

    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(
        headless=os.environ.get("HEADED", "") != "1"
    )
    context.base_url = f"http://localhost:{PORT}"


def before_scenario(context, scenario):
    context.page = context.browser.new_page()


def after_scenario(context, scenario):
    context.page.close()


def after_all(context):
    context.browser.close()
    context.playwright.stop()
    context.httpd.shutdown()
