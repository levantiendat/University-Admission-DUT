import subprocess
import os
import time
import socket
import requests

# Get port from Azure environment variable, or use default
RASA_PORT = int(os.environ.get('PORT', 5005))
ACTION_PORT = 5055
RASA_HOST = "0.0.0.0"
MODEL_PATH = "models/20250617-131828-equilateral-lodge.tar.gz"

# Remove ngrok related code for Azure deployment
# Azure provides its own public endpoint

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
    # 1. Reset database if exists
    db_path = "tracker.db"
    if os.path.exists(db_path):
        try:
            print("[*] Removing old tracker database...")
            os.remove(db_path)
        except:
            print("[!] Could not remove tracker database")
    
    # 2. Start Rasa server
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

if __name__ == "__main__":
    print("[+] Starting Action Server...")
    action_proc = start_action_server()

    print(f"[+] Starting Rasa Server with model: {MODEL_PATH}")
    rasa_proc = start_rasa_server(MODEL_PATH)

    print("[+] Waiting for Rasa to be ready...")
    while not is_port_open("localhost", RASA_PORT):
        time.sleep(1)

    print(f"[+] Chatbot running at port {RASA_PORT}")
    print("[*] Press Ctrl+C to exit.")

    try:
        # Keep the script running
        rasa_proc.wait()
        action_proc.wait()
    except KeyboardInterrupt:
        print("\n[!] Stopping processes...")
        rasa_proc.terminate()
        action_proc.terminate()