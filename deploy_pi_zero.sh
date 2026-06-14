#!/bin/bash
# Deploy Sovereign Vedic AGI to Raspberry Pi Zero
# Run on Pi Zero after cloning repo

echo "🕉 Deploying to Raspberry Pi Zero..."

# Install minimal dependencies
sudo apt-get update
sudo apt-get install -y clang make git --no-install-recommends

# Clone and build
cd ~
git clone https://github.com/divineearthly/sovereign-vedic-agi.git
cd sovereign-vedic-agi

# Compile for ARMv6 (Pi Zero)
clang++ -O3 -march=armv6 -pthread vedic_agi.cpp -o vedic_agi -lm
clang++ -O3 -march=armv6 chitta_memory.cpp -o chitta_memory -lm

# Create systemd service for auto-start
sudo cat > /etc/systemd/system/vedic-agi.service << 'SERVEOF'
[Unit]
Description=Sovereign Vedic AGI
After=network.target

[Service]
ExecStart=/home/pi/sovereign-vedic-agi/vedic_agi --daemon
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
SERVEOF

sudo systemctl enable vedic-agi
sudo systemctl start vedic-agi

echo "✅ Deployed! Access at http://[pi-ip]:8000"
