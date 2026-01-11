# uConsole Keyboard & Gamepad Configuration Backup

This directory contains backup files for the uConsole keyboard layout and gamepad configuration. Use these files to restore your custom configuration after installing Arch Linux.

## Files

### Keyboard Configuration
- **keyboard-layout.conf** - System keyboard layout settings (`/etc/default/keyboard`)
  - Layout: US
  - Model: pc105
  - Options: altwin:swap_lalt_lwin (swaps Left Alt and Left Win)

- **xfce4-keyboard-shortcuts.xml** - XFCE desktop keyboard shortcuts

### Input Devices
- **input-devices.txt** - Complete list of all input devices from `/proc/bus/input/devices`
- **gamepad-buttons.txt** - Gamepad button mappings from evtest

## Device Information

### Keyboard
- **Device**: ClockworkPI uConsole Keyboard
- **USB ID**: 1eaf:0024 (Leaflabs uConsole)
- **Serial**: 20230713
- **Event Device**: /dev/input/event4

### Gamepad
- **Device**: ClockworkPI uConsole (Gamepad)
- **USB ID**: 1eaf:0024 (Leaflabs uConsole)
- **Serial**: 20230713
- **Event Device**: /dev/input/event5
- **Joystick Device**: /dev/input/js0

#### Gamepad Controls
- **D-Pad**: ABS_HAT0X / ABS_HAT0Y (Up, Down, Left, Right)
- **Left Analog**: ABS_X / ABS_Y
- **Right Analog**: ABS_RX / ABS_RY
- **Buttons**:
  - Y, X, B, A buttons
  - L, R shoulder buttons
  - Start, Select buttons
  - Various trigger buttons (BTN_TRIGGER through BTN_TRIGGER_HAPPY16)

## Restoring on Arch Linux

### 1. Keyboard Layout
```bash
# Copy the keyboard layout config
sudo cp keyboard-layout.conf /etc/default/keyboard

# Apply the layout
sudo dpkg-reconfigure keyboard-configuration
# Or on Arch:
sudo localectl set-x11-keymap us pc105 '' altwin:swap_lalt_lwin
```

### 2. XFCE Keyboard Shortcuts (if using XFCE)
```bash
# Copy to your user config
mkdir -p ~/.config/xfce4/xfconf/xfce-perchannel-xml/
cp xfce4-keyboard-shortcuts.xml ~/.config/xfce4/xfconf/xfce-perchannel-xml/
```

### 3. Gamepad Configuration
The gamepad should be auto-detected. For SDL-based applications, you may need to add a gamepad mapping.

Check device detection:
```bash
ls -la /dev/input/by-id/ | grep uConsole
```

Test gamepad:
```bash
# Install jstest if needed
sudo pacman -S joyutils

# Test the gamepad
jstest /dev/input/js0
```

## Notes
- The uConsole uses a custom USB HID device that presents as multiple input devices
- All controls (keyboard, mouse, gamepad) use the same USB device (1eaf:0024)
- The Left Alt and Left Win keys are swapped by default (altwin:swap_lalt_lwin)
