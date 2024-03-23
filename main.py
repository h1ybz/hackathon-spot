import os
import time
from spot_controller import SpotController
import cv2

ROBOT_IP = "10.0.0.3"#os.environ['ROBOT_IP']
SPOT_USERNAME = "admin"#os.environ['SPOT_USERNAME']
SPOT_PASSWORD = "2zqa8dgw7lor"#os.environ['SPOT_PASSWORD']


def capture_image():
    camera_capture = cv2.VideoCapture(0)
    rv, image = camera_capture.read()
    print(f"Image Dimensions: {image.shape}")
    camera_capture.release()
    cv2.imwrite(f'/merklebot/job_data/camera_{time.time()}.jpg', image)


def main():
    #example of using micro and speakers
    # print("Start recording audio")
    # sample_name = "aaaa.wav"
    # cmd = f'arecord -vv --format=cd --device={os.environ["AUDIO_INPUT_DEVICE"]} -r 48000 --duration=10 -c 1 {sample_name}'
    # print(cmd)
    # os.system(cmd)
    # print("Playing sound")
    # os.system(f"ffplay -nodisp -autoexit -loglevel quiet {sample_name}")
    
    # # Capture image

    # Use wrapper in context manager to lease control, turn on E-Stop, power on the robot and stand up at start
    # and to return lease + sit down at the end
    with SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP) as spot:
        # Give Spot a moment to initialize
        time.sleep(2)
        
        print("Approaching the chair...")
        # Step 1: Approach the Chair
        # Assuming 1 meter is approximately 3.28 feet
        spot.move_to_goal(goal_x=0.91)  # Move forward by 3 feet (0.91 meters)
        
        # Step 2: Stop and Look Up at the Chair
        print("Looking up at the chair...")
        spot.move_head_in_points(yaws=[0], pitches=[-0.2], rolls=[0], sleep_after_point_reached=1)
        time.sleep(2)
        
        # Step 3: Walk to the Side of the Chair
        print("Moving to the side of the chair...")
        spot.move_by_velocity_control(v_rot=-1.0472, cmd_duration=1)  # Rotate 60 degrees to the right
        time.sleep(1)  # Wait for rotation to complete
        spot.move_by_velocity_control(v_x=0.3, cmd_duration=1)  # Move forward by 1 foot (0.3 meters)
        time.sleep(1)  # Wait for movement to complete
        spot.move_by_velocity_control(v_rot=1.8326, cmd_duration=1.5)  # Rotate 105 degrees to the left
        time.sleep(1.5)  # Wait for rotation to complete
        
        # Push the Chair
        print("Pushing the chair...")
        spot.move_by_velocity_control(v_x=0.3, cmd_duration=2)  # Push forward 1 foot (0.3 meters)
        time.sleep(2)

        spot.move_head_in_points(yaws=[0.0, 0.0], pitches=[0.9, 0], rolls=[0, 0], sleep_after_point_reached=2)
        time.sleep(2)
        
        print("Task completed!")

if __name__ == '__main__':
    main()
