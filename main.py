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

        time.sleep(0.5)

        # Gentle head nods
        spot.move_head_in_points(yaws=[0.2, 0.0], pitches=[0.2, 0], rolls=[0, 0], sleep_after_point_reached=1)
        time.sleep(0.5)
        spot.move_head_in_points(yaws=[-0.2, 0.0], pitches=[-0.2, 0], rolls=[0, 0], sleep_after_point_reached=1)
        time.sleep(0.5)

        # Side Shuffle (adjust distances and timing as desired)
        #for _ in range(4):
        spot.move_by_velocity_control(v_y=0.3, cmd_duration=1)
        time.sleep(1)
        spot.move_by_velocity_control(v_y=-0.3, cmd_duration=1)
        time.sleep(1)
        spot.move_by_velocity_control(v_y=0.3, cmd_duration=1)
        time.sleep(1)
        spot.move_by_velocity_control(v_y=-0.3, cmd_duration=1)
        time.sleep(1)

        # Up/Down
        spot.stand_at_height(0)
        time.sleep(0.15)
        spot.stand_at_height(-0.5)
        time.sleep(0.15) 
        spot.stand_at_height(0.1) 
        time.sleep(0.15) 
        spot.stand_at_height(-0.1) 
        time.sleep(0.15)
        spot.stand_at_height(0.1) 
        time.sleep(0.15)
        spot.stand_at_height(-0.1) 
        time.sleep(0.15)
        spot.stand_at_height(0.1) 
        time.sleep(0.15) 
        spot.stand_at_height(-0.1) 
        time.sleep(0.15)
        spot.stand_at_height(0.1) 
        time.sleep(0.15) 
        
        # Spin 
        spot.move_by_velocity_control(v_rot=1.0, cmd_duration=5.0)
        time.sleep(5)
        spot.move_by_velocity_control(v_rot=-1.0, cmd_duration=5.0)
        time.sleep(5)
            
if __name__ == '__main__':
    main()
