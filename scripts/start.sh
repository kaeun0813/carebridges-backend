#!/bin/bash

# 애플리케이션을 시작하는 명령어
echo "Starting the FastAPI application using systemd..."
sudo systemctl start carebridges.service  # carebridges.service 실행
echo "FastAPI application started."
