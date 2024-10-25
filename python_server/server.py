import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type


class SimpleRequestHandler(BaseHTTPRequestHandler):

    user_list = [{
        'id' : 1,
        'firstName' : "Konrad",
        'lastName' : "Kucab",
        'role' : 'Developer'
    }]

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(self.user_list).encode())


    def do_POST(self) -> None:
        content_length: int = int(self.headers['Content-Length'])
        post_data: bytes = self.rfile.read(content_length)
        received_data: dict = json.loads(post_data.decode())

        received_data['id'] = len(self.user_list) + 1
        self.user_list.append(received_data)

        response: dict = {
            "message": "Item added successfully",
            "updated_list": self.user_list
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())


    def do_DELETE(self) -> None:
        try:
            item_id = int(self.path.split('/')[-1]) 
            user_to_delete = next(user for user in self.user_list if user['id'] == item_id)
            self.user_list.remove(user_to_delete)

            response = {
                'message': f"Item with id {item_id} was deleted",
                'deleted_item': user_to_delete,
                'updated_list': self.user_list
            }
            self.send_response(200)

        except (StopIteration, ValueError):
            response = {
                'message': 'Invalid id, deletion failed',
                'current_list': self.user_list
            }
            self.send_response(400)

        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())


def run(
        server_class: Type[HTTPServer] = HTTPServer,
        handler_class: Type[BaseHTTPRequestHandler] = SimpleRequestHandler,
        port: int = 8000
) -> None:
    
    server_address: tuple = ('', port)
    httpd: HTTPServer = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()