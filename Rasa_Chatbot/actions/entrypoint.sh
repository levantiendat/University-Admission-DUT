#!/bin/bash

# Exit ngay khi có lỗi
set -e

# In thông báo log (tuỳ chọn)
echo "Starting Rasa Action Server..."

# Chạy action server
rasa run actions --port 5055 --debug
