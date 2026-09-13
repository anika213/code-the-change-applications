#!/usr/bin/env python3
"""Serve the app and its local CSV without copying responses into tracked files."""
import argparse
import csv
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser

ROOT = Path(__file__).resolve().parent

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = self.path.split('?', 1)[0]
        if route == '/api/responses':
            files = sorted(p for p in ROOT.iterdir() if p.suffix.lower() == '.csv')
            applications = []
            for path in files:
                with path.open(encoding='utf-8-sig', newline='') as source:
                    rows = list(csv.reader(source))
                if any('Name' in [c.strip() for c in row] and 'School' in [c.strip() for c in row] for row in rows):
                    applications.append((path, rows))
            if len(applications) != 1:
                self.send_json({'error': 'No application CSV found in this folder. Use Import CSV.' if not applications else 'Multiple application CSVs found. Use Import CSV to choose one.'}, 409)
                return
            path, rows = applications[0]
            self.send_json({'filename': path.name, 'rows': rows})
        elif route in ('/', '/index.html'):
            body = (ROOT / 'index.html').read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

    def send_json(self, value, status=200):
        body = json.dumps(value).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--open', action='store_true', help='Open the app in your browser')
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    url = f'http://127.0.0.1:{server.server_port}'
    print(f'Application viewer: {url}', flush=True)
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
