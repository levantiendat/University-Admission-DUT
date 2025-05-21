import subprocess
import os
import time
import socket
import requests

MODEL_PATH = "models/20250521-232311-booming-quetzal.tar.gz"
NGROK_AUTH_TOKEN = "2vn6H02jcPXaZY8MnH7ziimHO0v_4eyF1uzWGLXHCCKod2ceG"
NGROK_DOMAIN = "cockatoo-cheerful-factually.ngrok-free.app"
RASA_PORT = 5005
ACTION_PORT = 5055
RASA_HOST = "0.0.0.0"

NGROK_BIN = "ngrok"  # giả định đã cài CLI và có trong PATH


def is_port_open(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.close()
        return True
    except:
        return False


def start_action_server():
    command = ["rasa", "run", "actions", "--port", str(ACTION_PORT)]
    print("[DEBUG] Action command:", " ".join(command))
    return subprocess.Popen(command)


def start_rasa_server(model_path):
    command = [
        "rasa", "run",
        "--model", model_path,
        "--enable-api",
        "--endpoints", "endpoints.yml",
        "--credentials", "credentials.yml",
        "--cors", "*",
        "--debug",
        "--port", str(RASA_PORT),
        "--interface", RASA_HOST,
    ]
    print("[DEBUG] Rasa command:", " ".join(command))
    return subprocess.Popen(command)


def setup_ngrok_with_domain(auth_token, domain, port):
    # Đăng nhập bằng token nếu chưa login
    subprocess.run([NGROK_BIN, "config", "add-authtoken", auth_token], check=True)

    # Tạo tunnel tới Rasa port với domain custom
    ngrok_cmd = [
        NGROK_BIN, "http", str(port),
        "--domain", domain
    ]

    try:
        ngrok_proc = subprocess.Popen(ngrok_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Đợi ngrok khởi động và phản hồi
        for _ in range(10):
            try:
                response = requests.get("http://127.0.0.1:4040/api/tunnels")
                tunnels = response.json().get("tunnels", [])
                for t in tunnels:
                    if t["public_url"].startswith("https://" + domain):
                        return f"https://{domain}", ngrok_proc
            except Exception:
                pass
            time.sleep(1)
    except Exception as e:
        print(f"[!] Lỗi khởi tạo ngrok: {e}")

    return None, None


if __name__ == "__main__":
    print("[+] Khởi động Action Server...")
    action_proc = start_action_server()

    print(f"[+] Khởi động Rasa Server với model: {MODEL_PATH}")
    rasa_proc = start_rasa_server(MODEL_PATH)

    print("[+] Đợi Rasa sẵn sàng...")
    while not is_port_open("localhost", RASA_PORT):
        time.sleep(1)

    print(f"[+] Cố gắng khởi động ngrok với domain: {NGROK_DOMAIN}")
    public_url, ngrok_proc = setup_ngrok_with_domain(NGROK_AUTH_TOKEN, NGROK_DOMAIN, RASA_PORT)

    if public_url:
        print(f"[✓] Ngrok tunnel tại: {public_url}")
    else:
        print("[!] Không dùng được ngrok. Sử dụng localhost.")
        public_url = f"http://localhost:{RASA_PORT}"
        ngrok_proc = None

    print(f"[+] Chatbot đang chạy tại: {public_url}")
    print("[*] Nhấn Ctrl+C để thoát.")

    try:
        rasa_proc.wait()
        action_proc.wait()
    except KeyboardInterrupt:
        print("\n[!] Dừng tiến trình...")
        rasa_proc.terminate()
        action_proc.terminate()
        if ngrok_proc:
            ngrok_proc.terminate()
