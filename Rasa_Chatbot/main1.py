# Tạo một file debug_rasa.py với nội dung sau
import glob
import json
import yaml
import os

def check_files():
    # Check all YAML files
    yaml_files = glob.glob('**/*.yml', recursive=True)
    for file_path in yaml_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                try:
                    data = yaml.safe_load(content)
                    print(f"✅ {file_path}: YAML format OK")
                    
                    # Check for integer values that might cause problems
                    if isinstance(data, dict):
                        for key, value in data.items():
                            if isinstance(value, int):
                                print(f"⚠️ {file_path}: Integer value found for key '{key}': {value}")
                except Exception as e:
                    print(f"❌ {file_path}: YAML error: {e}")
        except Exception as e:
            print(f"❌ {file_path}: File read error: {e}")
    
    # Check all JSON files
    json_files = glob.glob('**/*.json', recursive=True)
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                try:
                    data = json.loads(content)
                    print(f"✅ {file_path}: JSON format OK")
                except Exception as e:
                    print(f"❌ {file_path}: JSON error: {e}")
        except Exception as e:
            print(f"❌ {file_path}: File read error: {e}")

if __name__ == "__main__":
    check_files()