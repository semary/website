"""Run with python3 scripts/check_site.py; no dependencies required."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / 'index.html').read_text()
llms = (ROOT / 'llms.txt').read_text()

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.images, self.headings = [], [], [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.links.append(attrs['href'])
        if tag == 'img':
            self.images.append(attrs)
        if tag == 'h1':
            self.headings.append(tag)

page = Page()
page.feed(html)
assert len(page.headings) == 1, 'Expected one primary heading'
assert len(page.ids) == len(set(page.ids)), 'Duplicate IDs'
for href in page.links:
    url = urlsplit(href)
    if url.scheme or url.netloc:
        continue
    if url.path:
        assert (ROOT / unquote(url.path.lstrip('/'))).is_file(), href
    if url.fragment:
        assert url.fragment in page.ids, href
for img in page.images:
    assert img.get('alt') and img.get('width') and img.get('height'), img
    assert (ROOT / img['src']).is_file(), img['src']
for data in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
    json.loads(data)
# Keep the published profile consistent across formats.
products = ['consumer app', 'merchant portal', 'corporate portal', 'mobile wallet', 'bill payments', 'digital lending']
for product in products:
    assert product in html.lower() and product in llms.lower(), product
assert 'products under one roadmap' in html and 'six products under one roadmap' in llms
assert 'growth, Q1 2018 to Q4 2018' in html and 'Q1 2018 to Q4 2018' in llms
assert 'in opportunities identified' in html and '$8M in opportunities identified' in llms
assert 'IntersectionObserver' not in html and '.rv{opacity:0' not in html
assert 'fonts.googleapis.com' not in html
# Upwork proof must match across the page, structured data, and llms.txt.
for proof in ['Top Rated', '100% Job Success', '18+']:
    assert proof in html and proof in llms, proof
assert 'social-card.jpg' in html and (ROOT / 'social-card.jpg').is_file(), 'Social card missing'
assert 'companyReference' not in html, 'Use the clean Upwork profile URL'
print('PASS: profile consistency, local links, anchors, image metadata, structured data, and visible-by-default content')

cv = (ROOT / "Mohamed_Sameer_CV.pdf").read_bytes()
assert cv.startswith(b"%PDF-"), "CV must be a valid PDF file"
assert b"%%EOF" in cv[-1024:] and len(cv) > 1000, "CV is incomplete"
print("PASS: CV signature and completeness")
