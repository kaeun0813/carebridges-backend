#!/bin/bash

echo "Stopping the FastAPI application using systemd..."
sudo systemctl stop carebridges.service

# 5초 후 상태 확인
sleep 5

if systemctl is-active --quiet carebridges.service; then
    echo "Service did not stop cleanly. Forcing shutdown..."
    pid=$(pgrep gunicorn)
    if [ -n "$pid" ]; then
        sudo kill -9 $pid
        echo "Gunicorn process forcefully killed."
    fi
fi

echo "FastAPI application stopped."
