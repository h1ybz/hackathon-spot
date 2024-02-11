import os
import time
from spot_controller import SpotController

ROBOT_IP = "192.168.50.3"#os.environ['ROBOT_IP']
SPOT_USERNAME = "admin"#os.environ['SPOT_USERNAME']
SPOT_PASSWORD = "2zqa8dgw7lor"#os.environ['SPOT_PASSWORD']


def main():
    #example of using micro and speakers
    print("Start recording audio")
    sample_name = "aaaa.wav"
    cmd = f'arecord -vv --format=cd --device={os.environ["AUDIO_INPUT_DEVICE"]} -r 48000 --duration=10 -c 1 {sample_name}'
    print(cmd)
    os.system(cmd)
    print("Playing sound")
    os.system(f"ffplay -nodisp -autoexit -loglevel quiet {sample_name}")
    
    # Capture image
    import cv2
    camera_capture = cv2.VideoCapture(0)
    rv, image = camera_capture.read()
    print(f"Image Dimensions: {image.shape}")
    camera_capture.release()

    # Use wrapper in context manager to lease control, turn on E-Stop, power on the robot and stand up at start
    # and to return lease + sit down at the end
    with SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP) as spot:

        time.sleep(2)

        for _ in range(12):  # Do this 12 times for a longer intro
            spot.stand_at_height(0.2)  # Up with some extra lift 
            time.sleep(0.15) 
            spot.stand_at_height(0) 
            time.sleep(0.15) 
            
        for _ in range(4): 
            spot.move_by_velocity_control(v_x=0, v_y=0.3, v_rot=0.2, cmd_duration=0.6)  # Left sway with turn
            spot.move_to_goal(goal_x=0.1, goal_y=0) 
            spot.move_by_velocity_control(v_x=0, v_y=-0.3, v_rot=-0.2, cmd_duration=0.6)  # Right sway, opposite turn
            spot.move_to_goal(goal_x=0.1, goal_y=0) 
        
        for _ in range(3):
            spot.move_to_goal(goal_x=0.2, goal_y=0.1) # Forward with a side angle
            time.sleep(0.4)
            spot.move_to_goal(goal_x=0.2, goal_y=-0.1) # Same, other direction
            time.sleep(0.4)

if __name__ == '__main__':
    main()
