import subprocess
import os
import time
import socket

MODEL_PATH = "models/20250617-131828-equilateral-lodge.tar.gz"
RASA_PORT = 5005
ACTION_PORT = 5055
RASA_HOST = "0.0.0.0"

def is_port_open(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            return True
        except:
            return False

def start_action_server():
    return subprocess.Popen([
        "rasa", "run", "actions",
        "--port", str(ACTION_PORT)
    ])

def start_rasa_server():
    db_path = "tracker.db"
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except:
            print("[!] Không thể xóa tracker.db")

    return subprocess.Popen([
        "rasa", "run",
        "--model", MODEL_PATH,
        "--enable-api",
        "--endpoints", "endpoints.yml",
        "--credentials", "credentials.yml",
        "--cors", "*",
        "--debug",
        "--port", str(RASA_PORT),
        "--interface", RASA_HOST
    ])

if __name__ == "__main__":
    print("[+] Khởi động Action Server...")
    action_proc = start_action_server()

    print("[+] Khởi động Rasa Server...")
    rasa_proc = start_rasa_server()

    print(f"[✓] Chatbot đang chạy tại http://0.0.0.0:{RASA_PORT} (Fly.io sẽ tự ánh xạ tới domain)")

    try:
        rasa_proc.wait()
        action_proc.wait()
    except KeyboardInterrupt:
        print("\n[!] Dừng tiến trình...")
        rasa_proc.terminate()
        action_proc.terminate()
