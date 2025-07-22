#!/bin/bash

echo "Starting deployment process..."

# 서비스 중지
echo "Stopping running service..."
sudo systemctl stop carebridges.service || true  # 에러 무시

# 배포 디렉토리로 이동
cd /home/ubuntu/carebridges-backend

# Poetry 설치 확인
if ! command -v poetry &> /dev/null; then
    echo "Poetry not found. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    export PATH="$HOME/.local/bin:$PATH"
    source ~/.bashrc
else
    echo "Poetry is already installed."
    export PATH="$HOME/.local/bin:$PATH"
fi

# Poetry 가상환경 설정
echo "Configuring Poetry virtual environment..."
poetry config virtualenvs.in-project true

# 의존성 설치
echo "Installing dependencies via Poetry..."
if [ -f "poetry.lock" ]; then
    poetry install --no-interaction --no-root
else
    echo "poetry.lock not found. Please check your project files."
    exit 1
fi

# systemd 서비스 파일 복사
echo "Copying systemd service file..."
sudo cp carebridges.service /etc/systemd/system/carebridges.service

# systemd 재로드
echo " Reloading systemd..."
sudo systemctl daemon-reload

# 서비스 시작
echo "Starting carebridges.service..."
sudo systemctl start carebridges.service

# 서비스 enable (부팅 시 자동 시작)
sudo systemctl enable carebridges.service

echo "Deployment script finished!"
