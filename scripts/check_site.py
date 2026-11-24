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
    if url.fragment and not url.path:
        assert url.fragment in page.ids, href
    elif url.fragment and url.path.lower().endswith('.pdf'):
        assert re.fullmatch(r'page=[1-9][0-9]*', url.fragment), href
    elif url.fragment:
        raise AssertionError(f'Unexpected fragment on local resource: {href}')
for img in page.images:
    assert img.get('alt') and img.get('width') and img.get('height'), img
    assert (ROOT / img['src']).is_file(), img['src']
for data in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
    json.loads(data)
# Keep the published profile consistent across formats.
products = ['consumer app', 'merchant portal', 'corporate portal', 'mobile wallet', 'bill payments', 'digital lending']
for product in products:
    assert product in html.lower() and product in llms.lower(), product
assert 'six banking products' in html and 'six products under one roadmap' in llms
assert 'Q1 to Q4 2018' in html and 'Q1 2018 to Q4 2018' in llms
assert '$50,000 in annual revenue after its first year' in html and '$50,000 in annual revenue after its first year' in llms
assert '$8M' not in html + llms
assert 'contactmohamedsameer@gmail.com' not in html + llms
for fact in ['357', '26', '8', 'HIMS', '2028', 'mohamedsameercontact@gmail.com']:
    assert fact in html and fact in llms, fact
assert 'IntersectionObserver' not in html and '.rv{opacity:0' not in html
assert 'fonts.googleapis.com' not in html
# Upwork profile figures were checked on 24 November 2026.
for proof in ['Top Rated', '100%', '22']:
    assert proof in html and proof in llms, proof
assert 'social-card-20261124.jpg' in html and (ROOT / 'social-card-20261124.jpg').is_file(), 'Social card missing'
assert 'companyReference' not in html, 'Use the clean Upwork profile URL'
print('PASS: profile consistency, local links, anchors, image metadata, structured data, and visible-by-default content')

for filename in ["Mohamed_Sameer_CV.pdf", "Mohamed-Sameer-Work-Samples.pdf"]:
    pdf = (ROOT / filename).read_bytes()
    assert pdf.startswith(b"%PDF-") and b"%%EOF" in pdf[-1024:] and len(pdf) > 1000, filename
    assert filename in html and filename in llms, filename
assert "Hire me on Upwork" in html and "Sep 2026 – present" in html and "Jul – Aug 2026" in html
print("PASS: consulting links, public downloads, and both Lahint roles")
