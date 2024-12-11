import time
import requests

ARM_IP = "192.168.4.1"  # RoArm M2 IP
# Predefined positions (adjust these!)

ARM_DEFAULT_POSITION = '{"T":1041,"x":207.3101528,"y":3.816548582,"z":-11.10264946,"b":0.018407769,"s":0.147262156,"e":2.458971203,"t":2.339320702,"torB":0,"torS":248,"torE":0,"torH":0}'
ARM_PICK_POSITION = '{"T":1041,"x":180.8771986,"y":3.329921891,"z":-49.26879267,"b":0.018407769,"s":0.29299033,"e":2.544874127,"t":2.343922644,"torB":0,"torS":20,"torE":100,"torH":0}'
ARM_CLOSE = '{"T":1041,"x":182.8683398,"y":3.366578498,"z":-57.86460667,"b":0.018407769,"s":0.348213639,"e":2.526466358,"t":2.827126592,"torB":0,"torS":44,"torE":0,"torH":-104}'
ARM_CAMERA_POSITION = '{"T":1041,"x":235.1145047,"y":-276.8278692,"z":155.6695459,"b":-0.866699145,"s":0.269980619,"e":1.555456519,"t":2.837864458,"torB":0,"torS":36,"torE":140,"torH":0}'
ARM_GREEN_BOX_POSITION = '{"T":1041,"x":300.7472946,"y":243.7441219,"z":116.3700943,"b":0.68108747,"s":0.40803889,"e":1.486427383,"t":2.853204265,"torB":160,"torS":52,"torE":0,"torH":0}'
ARM_GREEN_BOX_RELEASE = '{"T":1041,"x":292.8469821,"y":257.3501947,"z":106.8347013,"b":0.72097097,"s":0.432582582,"e":1.486427383,"t":2.779573188,"torB":0,"torS":48,"torE":0,"torH":96}'
ARM_RED_BOX_POSITION = '{"T":1041,"x":220.490647,"y":326.72263,"z":87.38933145,"b":0.977145762,"s":0.480135987,"e":1.489495345,"t":2.847068342,"torB":160,"torS":44,"torE":0,"torH":0}'
ARM_RED_BOX_RELEASE = '{"T":1041,"x":209.8707528,"y":335.9653406,"z":76.69055091,"b":1.01242732,"s":0.50621366,"e":1.491029326,"t":2.728951822,"torB":0,"torS":48,"torE":0,"torH":100}'
ARM_YELLOW_BOX_POSITION = '{"T":1041,"x":65.12221849,"y":396.9649084,"z":27.87406259,"b":1.408194363,"s":0.627398142,"e":1.492563307,"t":2.8424664,"torB":80,"torS":48,"torE":0,"torH":0}'
ARM_YELLOW_BOX_RELEASE = '{"T":1041,"x":59.01991445,"y":397.8799442,"z":1.748610801,"b":1.423534171,"s":0.688757374,"e":1.49869923,"t":2.580155685,"torB":0,"torS":60,"torE":0,"torH":96}'


def send_arm_command(json_cmd):
    url = f"http://{ARM_IP}/js?json={json_cmd}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        print("Arm response:", response.text)
    except requests.RequestException as e:
        print("Error sending command to RoArm:", e)

def move_arm_to_position(position_json, delay=3):
    print("moving the arm to:", position_json)
    send_arm_command(position_json)
    time.sleep(delay)  # wait for the arm to move

def pick_box_from_conveyor():
    print("Picking box...")
    move_arm_to_position(ARM_PICK_POSITION, delay=3)
    move_arm_to_position(ARM_CLOSE, delay=2)
    # Here you could send a gripper close command if needed

def move_box_in_front_of_camera():
    print("Moving to the camera...")
    move_arm_to_position(ARM_CAMERA_POSITION, delay=3)

def place_box_in_color_bin(color):
    if color == "Red":
        print("moving to red")
        move_arm_to_position(ARM_RED_BOX_POSITION, delay=3)
        move_arm_to_position(ARM_RED_BOX_RELEASE, delay=2)
        
    elif color == "Yellow":
        print("moving to yellow")
        move_arm_to_position(ARM_YELLOW_BOX_POSITION, delay=3)
        move_arm_to_position(ARM_YELLOW_BOX_RELEASE, delay=2)
    elif color == "Green":
        print("moving to green")
        move_arm_to_position(ARM_GREEN_BOX_POSITION, delay=3)
        move_arm_to_position(ARM_GREEN_BOX_RELEASE)
    else:
        # If unrecognized, just move to default or do nothing
        print("Unrecognized color, no placement done.")

    # Here you could send a gripper open command if needed

def return_to_default():
    print("Returning to default...")
    move_arm_to_position(ARM_DEFAULT_POSITION, delay=3)
