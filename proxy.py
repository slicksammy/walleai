import http.server
import socketserver
import urllib.request
import urllib.parse

class Proxy(http.server.SimpleHTTPRequestHandler):
    def handle_request(self):
        # Breakpoint for debugging
        if self.path.startswith("http://payments.braintree.com"):
            self.path = "http://localhost:8080" + self.path[len("http://payments.braintree.com"):]
        
        # Log the request path for debugging
        print(f"Requested path: {self.path}")
        
        # Prepare the request to be forwarded
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length else None
            req = urllib.request.Request(self.path, data=body, headers=dict(self.headers))
            req.get_method = lambda: self.command  # Set the request method
            
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                self.send_headers(response.headers)
                self.wfile.write(response.read())
        except Exception as e:
            self.send_error(500, f"Error fetching the URL: {e}")
    
    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_PUT(self):
        self.handle_request()

    def do_DELETE(self):
        self.handle_request()

    def do_HEAD(self):
        self.handle_request()

    def do_OPTIONS(self):
        self.handle_request()

    def do_PATCH(self):
        self.handle_request()

    def do_TRACE(self):
        self.handle_request()
    
    def send_headers(self, headers):
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()

if __name__ == "__main__":
    PORT = 8000
    with socketserver.TCPServer(("", PORT), Proxy) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()