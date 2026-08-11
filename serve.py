#!/usr/bin/env python3
"""Локальный сервер предпросмотра сайта «АЛЬФА».
Запуск:  python3 serve.py [порт]
"""
import sys, os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # разрешаем встраивание в iframe предпросмотра и отключаем кэш
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Frame-Options", "ALLOWALL")
        self.send_header("Content-Security-Policy", "frame-ancestors *")
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print("Сайт доступен на порту %d" % PORT, flush=True)
    srv.serve_forever()
