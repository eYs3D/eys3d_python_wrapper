import os 
import time

import cv2

def print_and_save(pipe, term1, term2, term3, comment, val, save_img=False, color=True):
    print("[TEST][{}][{}] {}: {}".format(term1, term2, comment, val))
    path = os.path.join("test", "save_test_img", term1, term2)
    if save_img:
        if not os.path.isdir(path):
            try:
                os.makedirs(path)
            except OSError:
                print(OSError)
        time.sleep(0.035) # It need to wait for 2 frames.
        if color:
            ret, frame = pipe.wait_color_frame(3500)
        else:
            ret, frame = pipe.wait_depth_frame(3500)
        frame_data = frame.get_rgb_data().reshape(frame.get_height(), frame.get_width(), 3)
        cv2.imwrite("{}/{}:{}.jpg".format(path, term3, val), cv2.cvtColor(frame_data, cv2.COLOR_RGB2BGR))

