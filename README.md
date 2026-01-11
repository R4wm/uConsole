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

These files can be used to restore your custom configuration after installing Arch Linux.

## Operating System

**Current**: Debian GNU/Linux 11 (bullseye)
**Planned**: Arch Linux
