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
        time.sleep(2)  # Give Spot a moment to initialize

        # Start the dance routine
        print("Starting dance routine...")
        
        # Stand up and adjust body height for the starting position
        spot.stand_at_height(body_height=0.5)
        time.sleep(2)
        capture_image()

        # Move in a small circle
        for _ in range(4):
            spot.move_by_velocity_control(v_x=0.2, v_y=0, v_rot=0.5, cmd_duration=1.5)
            time.sleep(2)
            capture_image()

        # Stand at different heights
        height = 0.05
        for _ in range(4):
            height += 0.1
            spot.stand_at_height(body_height=height)
            time.sleep(2)
            capture_image()

        # Bow as a final gesture
        spot.bow(pitch=0.3, body_height=0, sleep_after_point_reached=2)

        print("Dance routine completed!")


if __name__ == '__main__':
    main()
