import sys
import time

import eys3d

from eys3d import Pipeline, COLOR_RAW_DATA_TYPE, DEPTH_RAW_DATA_TYPE

DURATION = 100
count = 0
timestamp = 0


def color_frame_callback(frame):
    print("[Python][COLOR] The S/N in callback function: {}".format(
        frame.get_serial_number()))
    print("[Python][COLOR] The S/N in IMU Dataset: {}, count: {}".format(
        frame.get_sensor_dataset().get_serial_number(),
        frame.get_sensor_dataset().get_actual_data_count()))


def depth_frame_callback(frame):
    print("[Python][DEPTH] The S/N in callback function: {}".format(
        frame.get_serial_number()))

    # For calculating callback fps
    # global count, DURATION, timestamp
    # if (count % DURATION) == 0:
    #     if count != 0:
    #         temp = (frame.tsUs - timestamp) / 1000 / DURATION
    #         print("[FPS][DEPTH] {:.2f}".format(1000.0 / temp))
    #         timestamp = frame.tsUs
    # count += 1


def imu_data_callback(sensor_data):
    print("[Python][IMU] The S/N in callback function: {}".format(
        sensor_data.get_serial_number()))


def callback_sample(device, config):
    pipe = Pipeline(device=device)
    conf = config

    device.open_device(conf,
                       colorFrameCallback=color_frame_callback,
                       depthFrameCallback=depth_frame_callback,
                       IMUDataCallback=imu_data_callback)
    device.enable_stream()
    print(
        "\n\n\n********[Python][INFO] Start stream with callback function********"
    )
    time.sleep(10)
    device.pause_stream()
    print("\n\n\n********[Python][INFO] Pause stream********")
    time.sleep(1)
    device.enable_stream()
    print("\n\n\n********[Python][INFO] Start previous stream********")
    time.sleep(2)
    device.close_stream()
    print("\n\n\n********[Python][INFO] Stop stream********")
    device.open_device(conf)
    print(
        "\n\n\n********[Python][INFO] Start stream without callback function********"
    )
    device.enable_stream()
    time.sleep(2)
    device.close_stream()
    print("\n\n\n********[Python][INFO] Stop stream********")
