# webhook_stub.py
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length)
        with open('logs/webhook.log', 'a') as f:
            f.write(data.decode() + '\\n')
        self.send_response(200)
        self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 9000), Handler)
    print('Webhook stub listening on port 9000…')
    server.serve_forever()