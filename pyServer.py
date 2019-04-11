from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        conn = sqlite3.connect('cardData.db')
        c = conn.cursor()
        c.execute('SELECT * FROM cards')
        r = c.fetchone()
        uuid = r[1];
        conn.close()
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'card': uuid,
        }).encode())
        print("GET: uuid", uuid)
        return

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), RequestHandler)
    print('Starting server at http://localhost:8000')
server.serve_forever()
