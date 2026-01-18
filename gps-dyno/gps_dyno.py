#!/usr/bin/env python3
"""
GPS Dyno - Measure acceleration time and calculate wheel horsepower
using GPS speed data from gpsd.
"""

import json
import sys
import time
import select
import termios
import tty
from enum import Enum
from pathlib import Path

try:
    import gpsd
except ImportError:
    print("Error: gpsd-py3 not installed. Run: pip install gpsd-py3")
    sys.exit(1)


class State(Enum):
    IDLE = "IDLE - Accelerate past start speed to begin"
    WAITING_FOR_START = "WAITING - Get below start speed, then accelerate"
    RECORDING = "RECORDING..."
    COMPLETE = "COMPLETE"


def load_config():
    """Load configuration from config.json."""
    config_path = Path(__file__).parent / "config.json"
    try:
        with open(config_path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {config_path} not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing config.json: {e}")
        sys.exit(1)


def calculate_wheel_hp(weight_lbs, start_mph, end_mph, time_sec):
    """
    Calculate wheel horsepower using kinetic energy formula.

    HP = (weight_lbs × (end_mph² - start_mph²)) / (time_sec × 750)

    The 750 constant accounts for unit conversions.
    """
    if time_sec <= 0:
        return 0
    return (weight_lbs * (end_mph**2 - start_mph**2)) / (time_sec * 750)


def get_key_nonblocking():
    """Check for keypress without blocking."""
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read(1)
    return None


def clear_screen():
    """Clear terminal screen."""
    print("\033[2J\033[H", end="")


# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def main():
    config = load_config()

    vehicle_name = config["vehicle"]["name"]
    weight_lbs = config["vehicle"]["weight_lbs"]
    start_speed = config["test"]["start_speed_mph"]
    end_speed = config["test"]["end_speed_mph"]

    # Connect to gpsd
    try:
        gpsd.connect()
    except Exception as e:
        print(f"Error connecting to gpsd: {e}")
        print("Make sure gpsd is running: sudo systemctl start gpsd")
        sys.exit(1)

    # Set up terminal for non-blocking input
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    state = State.IDLE
    start_time = None
    elapsed_time = 0
    last_result = None
    current_speed = 0
    max_speed = 0
    prev_speed = None  # None means no previous reading yet
    gps_mode = 0
    sats_visible = 0
    sats_used = 0
    latitude = 0.0
    longitude = 0.0
    altitude = 0.0

    try:
        while True:
            # Check for keypress
            key = get_key_nonblocking()
            if key == 'q':
                break
            elif key == 'r':
                state = State.IDLE
                start_time = None
                elapsed_time = 0
                last_result = None
                max_speed = 0
                prev_speed = None

            # Get GPS data
            try:
                packet = gpsd.get_current()
                gps_mode = packet.mode
                sats_visible = packet.sats
                sats_used = packet.sats_valid
                if packet.mode >= 2:  # 2D or 3D fix
                    # Speed comes in m/s, convert to mph
                    current_speed = packet.speed() * 2.237 if packet.speed() else 0
                    latitude = packet.lat
                    longitude = packet.lon
                    altitude = packet.alt if packet.mode == 3 else 0.0
                else:
                    current_speed = 0
                    latitude = 0.0
                    longitude = 0.0
                    altitude = 0.0
            except Exception:
                gps_mode = 0
                sats_visible = 0
                sats_used = 0
                current_speed = 0
                latitude = 0.0
                longitude = 0.0
                altitude = 0.0

            # Track max speed during recording
            if state == State.RECORDING:
                max_speed = max(max_speed, current_speed)

            # State machine
            if state == State.IDLE:
                if current_speed >= start_speed:
                    # Check if we crossed the threshold (had valid prev below start)
                    if prev_speed is not None and prev_speed < start_speed:
                        # Crossed start threshold - begin recording
                        state = State.RECORDING
                        start_time = time.time()
                        max_speed = current_speed
                    else:
                        # Already above start speed or no valid prev, slow down first
                        state = State.WAITING_FOR_START

            elif state == State.WAITING_FOR_START:
                # Dropped below start speed, now ready
                if current_speed < start_speed:
                    state = State.IDLE

            elif state == State.RECORDING:
                elapsed_time = time.time() - start_time
                # Crossed end threshold - complete
                if current_speed >= end_speed:
                    state = State.COMPLETE
                    hp = calculate_wheel_hp(weight_lbs, start_speed, end_speed, elapsed_time)
                    last_result = {
                        "time": elapsed_time,
                        "hp": hp,
                        "max_speed": max_speed
                    }

            prev_speed = current_speed

            # Update display
            clear_screen()
            print("═══ GPS DYNO ═══")
            print(f"Vehicle: {vehicle_name} ({weight_lbs} lbs)")
            print(f"Test: {start_speed} → {end_speed} mph")
            print()
            # GPS satellite status (red if no fix, green if fix)
            mode_str = {0: "No data", 1: "No fix", 2: "2D fix", 3: "3D fix"}.get(gps_mode, "Unknown")
            if gps_mode >= 2:
                gps_color = GREEN
                gps_status = f"GPS: {mode_str} | Sats: {sats_used}/{sats_visible}"
            else:
                gps_color = RED
                gps_status = f"GPS: {mode_str} | Sats: {sats_visible} visible (waiting for fix...)"
            print(f"{gps_color}{gps_status}{RESET}")
            if gps_mode >= 2:
                print(f"Lat: {latitude:.6f}  Lon: {longitude:.6f}")
                if gps_mode == 3:
                    alt_ft = altitude * 3.281  # meters to feet
                    print(f"Alt: {alt_ft:.0f} ft")
            print()
            # Speed color: yellow=moving, green=recording, blue=complete
            if state == State.COMPLETE:
                speed_color = BLUE
            elif state == State.RECORDING:
                speed_color = GREEN
            elif current_speed > 0:
                speed_color = YELLOW
            else:
                speed_color = RESET
            print(f"Speed: {speed_color}{current_speed:.1f} mph{RESET}")
            print(f"Status: {state.value}")

            if state == State.RECORDING:
                print(f"Elapsed: {elapsed_time:.2f}s")

            if state == State.COMPLETE and last_result:
                print()
                print("═══ RESULTS ═══")
                print(f"Time: {last_result['time']:.2f} seconds")
                print(f"Max Speed: {last_result['max_speed']:.1f} mph")
                print(f"Wheel HP: {last_result['hp']:.1f} hp")

            print()
            print("[Press 'q' to quit, 'r' to reset]")

            time.sleep(0.1)  # Update ~10Hz

    finally:
        # Restore terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
