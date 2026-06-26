"""OpenCV preview demo for eYs3D stereo cameras.

Displays color and depth streams in OpenCV windows with interactive controls.

Usage:
    Hot Keys:
        * Q/q/Esc: Quit
        * E/e: Enable/Disable Auto Exposure (AE)
        * W/w: Enable/Disable Auto White Balance (AWB)
        * F1: Perform snapshot (saves to ~/.eYs3D/snapshots/)
        * F2: Dump frame info (saves to ~/.eYs3D/frames/)
        * F3: Dump IMU data (saves to ~/.eYs3D/imu_log/)
        * F4: Dump eYs3D system info
        * F5: Save rectify log data as JSON
        * F6: Dump camera properties info
        * I/i: Enable/Disable extended maximum IR value
        * M/m: Increase IR level
        * N/n: Decrease IR level
        * L/l: Increase depth ROI size
        * K/k: Decrease depth ROI size
        * P/p: Enable/Disable Hardware Post-Processing (HWPP)
        * 0: Reset Z range to defaults
        * 1: Z range setting 1 (ZNear=1234, ZFar=5678)
        * 2: Z range setting 2 (ZNear=1200, ZFar=1600)

Note:
    pipe.reset() was removed - C++ LatestFrameBuffer design automatically
    keeps only the latest frame, making manual reset unnecessary.
"""

import sys
import time
import os
import cv2
import numpy as np

from eys3d import Device, Pipeline, Config, logger

# Global variables for mouse ROI tracking
x: int = 0
y: int = 0


def cv_sample(device: Device, config: Config) -> None:
    # For cv preview
    COLOR_ENABLE = DEPTH_ENABLE = False

    pipe = Pipeline(device=device)
    conf = config
    if conf.get_config()['colorHeight']:
        COLOR_ENABLE = True
    if conf.get_config()['depthHeight']:
        DEPTH_ENABLE = True
    pipe.start(conf)

    # Flag defined
    flag = dict({
        'exposure': True,
        'white_balance': True,
        'Extend_IR': True,
        'HW_pp': True,
    })

    camera_property = device.get_cameraProperty()
    ir_property = device.get_IRProperty()
    ir_value = ir_property.get_IR_value()
    status = 'play'

    depth_roi = 10  # default is 10

    # default value of z range
    z_range = device.get_z_range()
    ZNEAR_DEFAULT = z_range["Near"]
    ZFAR_DEFAULT = z_range["Far"]
    logger.info("Default ZNear: {}, ZFar: {}".format(ZNEAR_DEFAULT,
                                                     ZFAR_DEFAULT))

    while 1:
        try:
            # C++ outputs BGR directly (device.py EYS3DSystem could configure the RGB byte order)
            if COLOR_ENABLE:
                cret, cframe = pipe.wait_color_frame()
                if cret:
                    bgr_cframe = cframe.get_rgb_data().reshape(cframe.get_height(), cframe.get_width(), 3)
                    cv2.imshow("Color image", bgr_cframe)
            if DEPTH_ENABLE:
                dret, dframe = pipe.wait_depth_frame()
                if dret:
                    bgr_dframe = dframe.get_rgb_data().reshape(dframe.get_height(), dframe.get_width(), 3)
                    cv2.imshow("Depth image", bgr_dframe)
                    z_map = dframe.get_depth_ZD_value().reshape(
                        dframe.get_height(), dframe.get_width())
                    cv2.setMouseCallback("Depth image", depth_roi_callback)

                    z_value = calculate_roi(x, y, dframe.get_width(),
                                          dframe.get_height(), depth_roi,
                                          z_map)
                    text = " Z = {:.2f}, Z-ROI = {}".format(z_value, depth_roi)
                    if os.name == "posix":
                        cv2.displayStatusBar("Depth image", text, 1000)
                    else:
                        cv2.setWindowTitle("Depth image", "Depth image  {}".format(text))

            status = {
                -1: status,
                27: 'exit',  # Esc
                ord('q'): 'exit',
                ord('Q'): 'exit',
                ord('e'): 'exposure',
                ord('E'): 'exposure',
                ord('w'): 'white_balance',
                ord('W'): 'white_balance',
                65470: 'snapshot',  # F1
                65471: 'dump_frame_info',  # F2
                65472: 'dump_imu_data',  # F3
                65473: 'dump_system_info',  # F4
                65474: 'get_rectify_log',  # F5
                65475: 'dump_camera_properties',
                ord('i'): 'extend_IR',
                ord('I'): 'extend_IR',
                ord('m'): 'increased_IR',
                ord('M'): 'increased_IR',
                ord('n'): 'decreased_IR',
                ord('N'): 'decreased_IR',
                ord('L'): 'increased_depth_roi',
                ord('l'): 'increased_depth_roi',
                ord('K'): 'decreased_depth_roi',
                ord('k'): 'decreased_depth_roi',
                ord('0'): 'reset-z-range',
                ord('1'): 'z-range-setting-1',
                ord('2'): 'z-range-setting-2',
                65361: 'play',  # Left arrow
                ord('p'): 'HW_pp',
                ord('P'): 'HW_pp',
            }[cv2.waitKeyEx(1)]
            # pipe.reset() removed - C++ LatestFrameBuffer design handles frame freshness
            if status == 'exit':
                cv2.destroyAllWindows()
                pipe.pause()
                break
            if status == 'exposure':
                flag["exposure"] = not (flag["exposure"])
                if flag["exposure"]:
                    logger.info("Enable Auto Exposure (AE)")
                    camera_property.enable_AE()
                else:
                    logger.info("Disable Auto Exposure (AE)")
                    camera_property.disable_AE()
                status = 'play'
            if status == 'white_balance':
                flag["white_balance"] = not (flag["white_balance"])
                if flag["white_balance"]:
                    logger.info("Enable Auto White Balance (AWB)")
                    camera_property.enable_AWB()
                else:
                    logger.info("Disable Auto White Balance (AWB)")
                    camera_property.disable_AWB()
                status = 'play'
            if status == 'snapshot':
                device.do_snapshot()
                logger.info(status)
                status = 'play'
            if status == 'dump_frame_info':
                device.dump_frame_info()
                logger.info(status)
                status = 'play'
            if status == 'dump_imu_data':
                device.dump_IMU_data()
                logger.info(status)
                status = 'play'
            if status == 'dump_system_info':
                device.dump_system_info()
                logger.info(status)
                status = 'play'
            if status == 'get_rectify_log':
                rectify_log = device.get_rectify_mat_log_data()
                rectify_log.save_json()
                logger.info("Saved rectify log as json")
                status = 'play'
            if status == 'dump_camera_properties':
                device.dump_camera_device_properties()
                logger.info("Dump camera properties")
                status = 'play'
            if status == 'extend_IR':
                flag["Extend_IR"] = not (flag["Extend_IR"])
                if flag["Extend_IR"]:
                    logger.info("Enable extend IR")
                    ir_property.enable_extendIR()
                else:
                    logger.info("Disable extend IR")
                    ir_property.disable_extendIR()
                status = 'play'
            if status == 'increased_IR':
                ir_value = min(ir_value + 1, ir_property.get_IR_max())
                ir_property.set_IR_value(ir_value)
                time.sleep(0.1)
                logger.info("Increase IR, current value = {}".format(ir_value))
                status = 'play'
            if status == 'decreased_IR':
                ir_value = max(ir_value - 1, ir_property.get_IR_min())
                ir_property.set_IR_value(ir_value)
                time.sleep(0.1)
                logger.info("Decrease IR, current value = {}".format(ir_value))
                status = 'play'
            if status == 'HW_pp':
                flag['HW_pp'] = not (flag['HW_pp'])
                if flag["HW_pp"]:
                    device.enable_HWPP()
                    logger.info("Enable HW PP")
                else:
                    device.disable_HWPP()
                    logger.info("Disable HW PP")
                status = 'play'
            if status == 'increased_depth_roi':
                if depth_roi < 40:
                    depth_roi += 1
                    device.set_septh_roi_pixels(depth_roi)
                logger.info("[Python] ROI: {}".format(depth_roi))
                status = 'play'
            if status == 'decreased_depth_roi':
                if depth_roi > 1:
                    depth_roi -= 1
                    device.set_septh_roi_pixels(depth_roi)
                logger.info("[Python] ROI: {}".format(depth_roi))
                status = 'play'
            if status == 'reset-z-range':
                logger.info("Reset z range")
                device.set_z_range(ZNEAR_DEFAULT, ZFAR_DEFAULT)
                z_range = device.get_z_range()
                logger.info("ZNear: {}, ZFar:{}".format(
                    z_range["Near"], z_range["Far"]))
                status = 'play'
            if status == 'z-range-setting-1':
                device.set_z_range(1234, 5678)
                z_range = device.get_z_range()
                logger.info("ZNear: {}, ZFar:{}".format(
                    z_range["Near"], z_range["Far"]))
                status = 'play'
            if status == 'z-range-setting-2':
                device.set_z_range(1200, 1600)
                z_range = device.get_z_range()
                logger.info("ZNear: {}, ZFar:{}".format(
                    z_range["Near"], z_range["Far"]))
                status = 'play'

        except (TypeError, ValueError, cv2.error, KeyError) as e:
            pass
    pipe.stop()


def calculate_roi(
    x: int,
    y: int,
    w: int,
    h: int,
    depth_roi: int,
    z_map: np.ndarray
) -> float:
    """Calculate average Z value within ROI around cursor position.

    Args:
        x: Cursor X-coordinate.
        y: Cursor Y-coordinate.
        w: Frame width.
        h: Frame height.
        depth_roi: ROI size in pixels (square).
        z_map: Depth map array (H, W) with Z values in mm.

    Returns:
        Average Z value in mm within the ROI, excluding zero (invalid) pixels.
    """
    if depth_roi > 1:
        roi_x = max(x - depth_roi / 2.0, 0)
        roi_y = max(y - depth_roi / 2.0, 0)
        roi_x2 = roi_x + depth_roi
        roi_y2 = roi_y + depth_roi

        if roi_x2 > w:
            roi_x2 = w
            roi_x = roi_x2 - depth_roi
        if roi_y2 > h:
            roi_y2 = h
            roi_y = roi_y2 - depth_roi

        depth_roi_sum = 0
        depth_roi_count = 0

        for y_ in range(int(roi_y), int(roi_y2)):
            for x_ in range(int(roi_x), int(roi_x2)):
                z_value = z_map[y_][x_]
                if z_value:
                    depth_roi_sum += z_value
                    depth_roi_count += 1
        if depth_roi_count:
            z_value = depth_roi_sum / depth_roi_count
        else:
            z_value = 0
    else:
        z_value = z_map[y][x]

    return z_value


def depth_roi_callback(event: int, x_: int, y_: int, flag: int, param: object) -> None:
    """OpenCV mouse callback to update ROI center coordinates.

    Args:
        event: OpenCV mouse event type.
        x_: Mouse X-coordinate.
        y_: Mouse Y-coordinate.
        flag: OpenCV event flags.
        param: User data (unused).
    """
    global x, y
    x = x_
    y = y_
