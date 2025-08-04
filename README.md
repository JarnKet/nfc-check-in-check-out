
chat-gpt link: https://chatgpt.com/c/684afd37-53e8-8002-9f09-c71bc2c77757

# NFC Card Reader - Door Check-in/Check-out System

## Overview

This project implements an automated door check-in/check-out system using an ACR122U NFC card reader connected to a Raspberry Pi. The system reads NFC card UIDs and sends them to a remote API for processing employee entry/exit data.

## Hardware Requirements

- Raspberry Pi (4 or newer recommended)
- ACR122U NFC Card Reader
- USB Cable for NFC Reader
- MicroSD Card (16GB+)
- Power Supply for Raspberry Pi
- Network Connection (WiFi or Ethernet)

## Software Requirements

- Raspberry Pi OS (Debian-based)
- Python 3.11+
- PC/SC Smart Card Daemon
- Required Python packages: `pyscard`, `requests`

## Project Structure

```
nfc-check-in-check-out/
├── main.py                 # Main application script
├── test.py                 # Test script for development
├── test-reader.py          # Hardware testing script
├── hello-world.py          # Basic test file
├── requirements.txt        # Python dependencies (if using venv)
├── README.md              # This file
└── logs/                  # Log files (created automatically)
    └── nfc-reader.log
```

## Installation Guide

### 1. Prepare Raspberry Pi OS

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install python3-dev python3-pip libpcsclite-dev swig pcscd pcsc-tools libacsccid1 -y
```

### 2. Install PC/SC Smart Card Services

```bash
# Start and enable PC/SC daemon
sudo systemctl start pcscd
sudo systemctl enable pcscd

# Verify service is running
sudo systemctl status pcscd
```

### 3. Clone and Setup Project

```bash
# Navigate to home directory
cd /home/lailaolabdev

# Clone or create project directory
mkdir nfc-check-in-check-out
cd nfc-check-in-check-out

# Copy your project files here
# main.py, test.py, etc.
```

### 4. Install Python Dependencies

#### Option A: Global Installation (Recommended for production)
```bash
# Install packages globally
pip install --break-system-packages pyscard requests

# Or using apt
sudo apt install python3-pyscard python3-requests
```

#### Option B: Virtual Environment (For development)
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install pyscard requests
```

### 5. Hardware Setup

1. Connect ACR122U NFC reader to Raspberry Pi via USB
2. Verify hardware detection:

```bash
# Check USB device detection
lsusb | grep "Advanced Card Systems"

# Test reader detection
pcsc_scan
```

### 6. Test the System

```bash
# Navigate to project directory
cd /home/lailaolabdev/nfc-check-in-check-out

# Test reader detection
python3 test-reader.py

# Test main application
python3 main.py
```

## Configuration

### API Configuration

Edit the `main.py` file to configure your API endpoint:

```python
API_URL = "https://hr-api.lailaolab.com/v1/api/entry-exit/nfc"
```

### Service Configuration

The system runs as a systemd service for automatic startup. Service file location:
```
/etc/systemd/system/nfc-reader.service
```

## Running the Application

### Manual Execution (for testing)

```bash
cd /home/lailaolabdev/nfc-check-in-check-out
python3 main.py
```

### Production Service (automatic startup)

```bash
# Start service
sudo systemctl start nfc-reader.service

# Enable auto-start on boot
sudo systemctl enable nfc-reader.service

# Check service status
sudo systemctl status nfc-reader.service
```

## Service Management

### Systemd Service Installation

1. Create service file:

```bash
sudo nano /etc/systemd/system/nfc-reader.service
```

2. Service configuration:

```ini
[Unit]
Description=NFC Card Reader Service
After=network.target pcscd.service
Wants=network.target
Requires=pcscd.service

[Service]
Type=simple
User=lailaolabdev
Group=lailaolabdev
WorkingDirectory=/home/lailaolabdev/nfc-check-in-check-out
ExecStart=/usr/bin/python3 /home/lailaolabdev/nfc-check-in-check-out/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

3. Enable and start service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable nfc-reader.service
sudo systemctl start nfc-reader.service
```

### Service Commands

```bash
# Start service
sudo systemctl start nfc-reader.service

# Stop service
sudo systemctl stop nfc-reader.service

# Restart service
sudo systemctl restart nfc-reader.service

# Check status
sudo systemctl status nfc-reader.service

# View logs
sudo journalctl -u nfc-reader.service -f

# View recent logs
sudo journalctl -u nfc-reader.service -n 50
```

## Monitoring and Logging

### Real-time Monitoring

```bash
# Watch live service logs
sudo journalctl -u nfc-reader.service -f

# Monitor with timestamps
sudo journalctl -u nfc-reader.service -f --since "1 hour ago"

# Check service status
sudo systemctl status nfc-reader.service
```

### Log Files

- **System logs**: Available via `journalctl`
- **Application logs**: `/home/lailaolabdev/nfc-check-in-check-out/logs/nfc-reader.log` (if file logging is enabled)

### Monitoring Script

Create a monitoring script for easier debugging:

```bash
nano ~/monitor-nfc.sh
```

```bash
#!/bin/bash
echo "=== NFC Reader Service Monitor ==="
while true; do
    clear
    echo "=== Service Status ==="
    sudo systemctl status nfc-reader.service --no-pager -l
    echo ""
    echo "=== Last 10 Log Entries ==="
    sudo journalctl -u nfc-reader.service -n 10 --no-pager
    sleep 5
done
```

```bash
chmod +x ~/monitor-nfc.sh
./monitor-nfc.sh
```

## Troubleshooting

### Common Issues

#### 1. NFC Reader Not Detected

```bash
# Check USB connection
lsusb

# Restart PC/SC daemon
sudo systemctl restart pcscd

# Check reader status
pcsc_scan
```

#### 2. Service Won't Start

```bash
# Check service logs
sudo journalctl -u nfc-reader.service -n 20

# Verify file permissions
ls -la /home/lailaolabdev/nfc-check-in-check-out/main.py

# Test manual execution
cd /home/lailaolabdev/nfc-check-in-check-out
python3 main.py
```

#### 3. Python Module Not Found

```bash
# Reinstall packages
pip install --break-system-packages pyscard requests

# Or use apt
sudo apt install python3-pyscard python3-requests
```

#### 4. Permission Issues

```bash
# Add user to dialout group
sudo usermod -a -G dialout lailaolabdev

# Restart system or log out/in
sudo reboot
```

### Hardware Troubleshooting

1. **No LED on reader**: Normal behavior on Linux (different from Windows)
2. **Reader not responding**: Try different USB ports
3. **Intermittent connection**: Check USB cable quality

### Software Troubleshooting

1. **Service keeps restarting**: Check logs for Python errors
2. **API connection fails**: Verify network connectivity and API URL
3. **Cards not reading**: Ensure cards are compatible NFC/RFID cards

## API Integration

### Endpoint Configuration

```python
API_URL = "https://hr-api.lailaolab.com/v1/api/entry-exit/nfc"
```

### Request Format

```json
{
    "serialNumber": "CARD_UID_HEX"
}
```

### Response Handling

- **Success (200)**: Card processed successfully
- **Error (4xx/5xx)**: Log error and continue operation

## Development Guidelines

### Code Structure

- `main.py`: Primary application logic
- `test-reader.py`: Hardware testing utilities
- `test.py`: Development testing script

### Adding Features

1. **Enhanced Logging**: Modify logging configuration in `main.py`
2. **API Changes**: Update API_URL and request format
3. **Card Validation**: Add UID format validation
4. **Local Storage**: Implement offline mode with local database

### Testing

```bash
# Test hardware connection
python3 test-reader.py

# Test API connectivity
curl -X POST https://hr-api.lailaolab.com/v1/api/entry-exit/nfc \
  -H "Content-Type: application/json" \
  -d '{"serialNumber":"TEST123"}'
```

## Maintenance

### Regular Maintenance Tasks

1. **Monitor disk space**: Log files can grow over time
2. **Update system packages**: `sudo apt update && sudo apt upgrade`
3. **Check service health**: `sudo systemctl status nfc-reader.service`
4. **Backup configuration**: Save service files and main.py

### System Updates

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Restart services after updates
sudo systemctl restart pcscd
sudo systemctl restart nfc-reader.service
```

## Security Considerations

1. **Network Security**: Ensure API endpoint uses HTTPS
2. **Access Control**: Limit physical access to Raspberry Pi
3. **User Permissions**: Run service as non-root user when possible
4. **Regular Updates**: Keep system and packages updated

## Deployment Checklist

- [ ] Raspberry Pi OS installed and updated
- [ ] Hardware connected and tested
- [ ] PC/SC daemon installed and running
- [ ] Python dependencies installed
- [ ] Project files copied to correct location
- [ ] Service file created and configured
- [ ] Service enabled for auto-start
- [ ] System tested with actual NFC cards
- [ ] Monitoring tools configured
- [ ] Documentation handed over to team

## Support Information

### Hardware Specifications
- **NFC Reader**: ACR122U
- **Supported Cards**: ISO14443 Type A/B, MIFARE Classic, NTAG, etc.
- **Read Range**: Up to 5cm
- **Interface**: USB 2.0

### Contact Information
- **Project Handover**: [Development Team]
- **Hardware Vendor**: Advanced Card Systems Ltd.
- **API Documentation**: Contact backend team

---

## Quick Reference Commands

```bash
# Service management
sudo systemctl {start|stop|restart|status} nfc-reader.service

# View logs
sudo journalctl -u nfc-reader.service -f

# Test hardware
pcsc_scan

# Manual run
cd /home/lailaolabdev/nfc-check-in-check-out && python3 main.py
```

This documentation should provide your development team with everything they need to maintain and extend the NFC card reader system.