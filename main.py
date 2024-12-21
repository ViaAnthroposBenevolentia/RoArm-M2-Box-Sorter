import serial
import time
import logging
import os
from arm import pick_box_from_conveyor, move_box_in_front_of_camera, place_box_in_color_bin, return_to_default
from arm import move_arm_to_position, ARM_DEFAULT_POSITION
from camera import detect_color_once
from web_interface import update_system_state

arduino_port = "COM3"
baud_rate = 9600

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('robot_arm.log'),
        logging.StreamHandler()
    ]
)

def initialize_system():
    try:
        # Create serial connection
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        logging.info("Connected to Arduino on %s", arduino_port)
        
        # Wait for Arduino to initialize
        time.sleep(2)
        
        # Move arm to default position
        move_arm_to_position(ARM_DEFAULT_POSITION, delay=3)
        update_system_state(status="System initialized", position="default")
        
        return ser
    except Exception as e:
        logging.error("Failed to initialize system: %s", str(e))
        raise

while True:
    try:
        ser = initialize_system()
        while True:
            try:
                # Listen for messages from Arduino
                if ser.in_waiting > 0:
                    message = ser.readline().decode("utf-8").strip()
                    print("From Arduino:", message)

                    if message == "box_detected":
                        update_system_state(status="Processing new box")
                        print("Box detected by Arduino. Handling with arm...")
                        time.sleep(1)

                        # Step 1: Arm picks the box from conveyor
                        update_system_state(position="picking")
                        pick_box_from_conveyor()
                        time.sleep(1)

                        # Step 2: Arm moves box in front of camera for color detection
                        update_system_state(position="camera")
                        move_box_in_front_of_camera()
                        time.sleep(1)

                        # Step 3: Detect color using laptop camera
                        color = detect_color_once()
                        if color:
                            print(f"Detected color: {color}")
                            update_system_state(color=color)
                        else:
                            print("No recognizable color detected. Defaulting to leaving it as is.")
                            color = None

                        # Step 4: Place box in corresponding bin
                        update_system_state(position=f"placing_{color.lower() if color else 'unknown'}")
                        place_box_in_color_bin(color)

                        # Step 5: Arm returns to default position
                        update_system_state(position="default", status="idle")
                        return_to_default()

                        # Step 6: Notify Arduino that arm is done
                        print("Sending 'arm_done' to Arduino...")
                        ser.write(b"arm_done\n")

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                logging.error("Error in main loop: %s", str(e))
                update_system_state(status="Error: " + str(e))
                time.sleep(5)  # Wait before retrying
    except Exception as e:
        logging.critical("Fatal error: %s", str(e))
        update_system_state(status="Fatal error - system stopped")
    finally:
        if 'ser' in locals():
            ser.close()
