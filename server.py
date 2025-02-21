from http.server import HTTPServer, SimpleHTTPRequestHandler

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        if path.endswith(".bin"):
            return "application/octet-stream"
        return super().guess_type(path)

server_address = ('0.0.0.0', 25565)
httpd = HTTPServer(server_address, CustomHTTPRequestHandler)

print("Servidor HTTP rodando na porta 25565...")
httpd.serve_forever()