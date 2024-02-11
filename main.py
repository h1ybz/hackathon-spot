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

        # Move head to specified positions with intermediate time.sleep
        spot.move_head_in_points(yaws=[0.2, 0],
                                 pitches=[0.3, 0],
                                 rolls=[0.4, 0],
                                 sleep_after_point_reached=1)
        time.sleep(1)
        
        spot.move_by_velocity_control(v_x=0, v_y=0, v_rot=0.7, cmd_duration=1.5)  # A sharp spin
        spot.bow(pitch=0.6)  # A quick, sassy head dip 
        time.sleep(0.5)
        spot.move_by_velocity_control(v_x=0, v_y=0, v_rot=-0.7, cmd_duration=1.5)  # Spin back 
        
        for _ in range(3):
            spot.move_to_goal(goal_x=0, goal_y=0.2)   # Shift left
            spot.move_to_goal(goal_x=0.15, goal_y=0)  # Small kick forward
            spot.move_to_goal(goal_x=0, goal_y=-0.2)  # Shift right
            spot.move_to_goal(goal_x=0.15, goal_y=0)  # Another kick

if __name__ == '__main__':
    main()
