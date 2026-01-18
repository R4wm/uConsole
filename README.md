# uConsole
Configuration and documentation for my Clockwork uConsole

## Hardware Specifications

### Core Hardware
- **Device**: Clockwork uConsole
- **SBC**: Raspberry Pi Compute Module 4 Rev 1.1
- **CPU**: ARM Cortex-A72 (4 cores @ 1.5GHz max)
- **Architecture**: aarch64 (ARM64)
- **SoC**: BCM2835
- **Memory**: 3.7GB RAM
- **Storage**: 117GB

### Input Devices
All input devices use USB ID: **1eaf:0024** (Leaflabs uConsole, Serial: 20230713)

#### Keyboard
- **Model**: ClockworkPI uConsole Keyboard
- **Event Device**: `/dev/input/event4`
- **Layout**: US (pc105)
- **Custom Mapping**: Left Alt and Left Win swapped

#### Gamepad
- **Model**: ClockworkPI uConsole Gamepad
- **Event Device**: `/dev/input/event5`
- **Joystick Device**: `/dev/input/js0`
- **Controls**:
  - D-Pad: Up, Down, Left, Right
  - Face Buttons: Y, X, B, A
  - Shoulder Buttons: L, R
  - System Buttons: Start, Select
  - Analog Sticks: Left and Right

#### Mouse/Trackball
- **Event Device**: `/dev/input/event6`

## Configuration Backups

See the `keyboard-config/` directory for:
- Keyboard layout configuration
- XFCE keyboard shortcuts
- Gamepad button mappings
- Complete input device information

These files can be used to restore your custom configuration on a fresh Arch Linux ARM install.

## Operating System

**OS**: Arch Linux ARM
**Kernel**: 6.12.45-1-uconsole-rpi64

## USB GPS Antenna

### Hardware
- **Device**: USB-Serial Controller with GPS receiver
- **Chip**: Prolific PL2303 USB-to-Serial adapter
- **USB ID**: 067b:23a3
- **Manufacturer**: Prolific Technology Inc.
- **Serial Device**: `/dev/ttyUSB0`
- **Baud Rate**: 4800

### Software
- **Daemon**: gpsd 3.27.5
- **Protocol**: NMEA0183

### Installation

```bash
# Install gpsd
sudo pacman -S gpsd

# Add user to uucp group for serial access without sudo
sudo usermod -aG uucp $USER

# Configure gpsd (edit /etc/default/gpsd)
# Set DEVICES="/dev/ttyUSB0"

# Enable and start gpsd
sudo systemctl enable gpsd.socket gpsd.service
sudo systemctl start gpsd.socket gpsd.service
```

### Testing

```bash
# View raw NMEA data
sudo cat /dev/ttyUSB0

# View gpsd JSON output
gpspipe -w localhost

# Interactive GPS monitor
cgps

# GPS monitor with more detail
gpsmon
```

### Configuration Backup

See `gps-config/` directory for gpsd configuration files.
