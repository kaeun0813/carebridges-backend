#!/bin/bash

# 애플리케이션 중지 명령어
echo "Stopping the FastAPI application using systemd..."
sudo systemctl stop carebridges  # carebridges.service 중지
echo "FastAPI application stopped."
