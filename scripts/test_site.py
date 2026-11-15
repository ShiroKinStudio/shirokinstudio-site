"""Smoke-test actual mobile/desktop storefront rendering using Chromium.

GitHub Actions builds optimized images first and publishes screenshots as artifacts.
Run locally after: python -m pip install playwright && python -m playwright install chromium
"""
from __future__ import annotations

import os
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'test-screenshots'
WIDTHS = [320, 375, 390, 768, 1366, 1920]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f'http://127.0.0.1:{server.server_port}/index.html'
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            for width in WIDTHS:
                height = 844 if width <= 390 else 900
                page = browser.new_page(viewport={'width': width, 'height': height}, device_scale_factor=1)
                try:
                    response = page.goto(url, wait_until='domcontentloaded', timeout=20000)
                    assert response and response.ok, f'{width}: HTTP response failed'
                    page.locator('h1').wait_for()
                    page.locator('.primary-cta').wait_for()
                    page.wait_for_function('''() => {
                        const img = document.querySelector('.featured-art img');
                        return img?.complete && img.naturalWidth > 0;
                    }''', timeout=15000)
                    page.evaluate('document.fonts.ready')
                    page.wait_for_timeout(150)
                    measures = page.evaluate('''() => ({
                        viewport: innerWidth,
                        scrollWidth: document.documentElement.scrollWidth,
                        pageHeight: document.documentElement.scrollHeight,
                        hero: document.querySelector('.featured-art img').currentSrc,
                        buttons: [...document.querySelectorAll('a[data-game]')].map(x => x.href),
                        visible: [...document.querySelectorAll('a[data-game]')].every(x => x.getBoundingClientRect().width >= 80)
                    })''')
                    assert measures['scrollWidth'] <= width + 2, f'{width}: horizontal overflow {measures}'
                    assert measures['hero'].endswith('.webp'), f'{width}: WebP not loaded {measures}'
                    assert len(measures['buttons']) == 2 and measures['visible'], f'{width}: CTA broken {measures}'
                    screenshot = OUT / f'site-{width}.png'
                    page.screenshot(path=str(screenshot), full_page=True, animations='disabled')
                    print(f'PASS {width}px, pageHeight={measures["pageHeight"]}, {screenshot.name}')
                finally:
                    page.close()
            browser.close()
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()