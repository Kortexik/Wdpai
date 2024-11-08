import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type
import os
import time
import psycopg2

DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_PORT = int(os.environ.get('DB_PORT', 5432))
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')


def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("Połączono z bazą danych")
            return conn
        except psycopg2.OperationalError:
            print("Błąd połączenia z bazą danych, ponawianie za 5 sekund...")
            time.sleep(5)

conn = connect_to_db()
cursor = conn.cursor()

def save_in_db(id: int, fname: str, lname: str, role: str):
    try:
        sql_query = "INSERT INTO users(id, first_name, last_name, role) VALUES(%s, %s, %s, %s);"
        cursor.execute(sql_query, (id, fname, lname, role))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")



def fetch_users_from_db():
    try:
        sql_query = "SELECT * FROM users;"
        cursor.execute(sql_query)
        users = cursor.fetchall()
        return [{'id': row[0], 'firstName': row[1], 'lastName': row[2], 'role': row[3]} for row in users]
    except Exception as error:
        print("Error fetching data from database:", error)
        return []

def delete_from_db(id: int):
    try:
        sql_query = "DELETE FROM users WHERE id = %s;"
        cursor.execute(sql_query, (id,))
        conn.commit()
        
    except Exception as error:
        conn.rollback()
        print("Error connecting to database:", error)


def close_connection():
    if cursor:
        cursor.close()
    if conn:
        conn.close()


class SimpleRequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        users = fetch_users_from_db()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(users).encode())


    def do_POST(self) -> None:
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        received_data = json.loads(post_data.decode())

        received_data['id'] = len(fetch_users_from_db()) + 1
        save_in_db(received_data['id'], received_data['firstName'], received_data['lastName'], received_data['role'])

        response = {
            "message": "User added successfully",
            "updated_list": fetch_users_from_db()
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())



    def do_DELETE(self) -> None:
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            received_data = json.loads(post_data.decode())
            item_id = received_data["id"]
            delete_from_db(item_id)

            response = {
                'message': f"User with ID {item_id} was deleted",
                'updated_list': fetch_users_from_db()
            }
            self.send_response(200)
        except ValueError:
            response = {
                'message': 'Invalid ID, deletion failed',
                'updated_list': fetch_users_from_db()
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
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    finally:
        close_connection()
        print("Database connection closed.")

if __name__ == '__main__':
    run()