"""
It's a demo to preview 2D frame with opencv.

Usage:
    Hot Keys:
        * Q/q/Esc: Quit
        * E/e: Enable/Disable AE
        * <F1>: Perform snapshot
        * <F2>: Dump frame info
        * <F3>: Dump IMU data
        * <F4>: Dump eYs3D system info
        * <F5>: Save rectify log data
        * <F6>: Dump camera properties info
        * I/i: Enable/Disable extend maximum IR value
        * M/m: Increase IR level
        * N/n: Decrease IR level
        * L/l: Increase z-roi
        * K/k: Decrease z-roi
        * P/p: Enabel/Disable HW PP
        * 0: Reset Z range
        * 1: Z range setting 1 with ZNear=1234 and ZFar=5678
        * 2: Z range setting 2 with ZNear=1200 and ZFar=1600
"""

import sys
import time

import cv2

from eys3d import Pipeline, logger

# For depth-roi calculated
x = y = 0


def cv_sample(device, config):
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
            if COLOR_ENABLE:
                cret, cframe = pipe.wait_color_frame()
                if cret:
                    bgr_cframe = cv2.cvtColor(
                        cframe.get_rgb_data().reshape(cframe.get_height(),
                                                      cframe.get_width(), 3),
                        cv2.COLOR_RGB2BGR)
                    cv2.imshow("Color image", bgr_cframe)
            if DEPTH_ENABLE:
                dret, dframe = pipe.wait_depth_frame()
                if dret:
                    bgr_dframe = cv2.cvtColor(
                        dframe.get_rgb_data().reshape(dframe.get_height(),
                                                      dframe.get_width(), 3),
                        cv2.COLOR_RGB2BGR)
                    cv2.imshow("Depth image", bgr_dframe)
                    z_map = dframe.get_depth_ZD_value().reshape(
                        dframe.get_height(), dframe.get_width())
                    cv2.setMouseCallback("Depth image", depth_roi_callback)
                    cv2.displayStatusBar(
                        "Depth image", " Z = {:.2f}, Z-ROI = {}".format(
                            calculate_roi(x, y, dframe.get_width(),
                                          dframe.get_height(), depth_roi,
                                          z_map), depth_roi), 1000)
            status = {
                -1: status,
                27: 'exit',  # Esc
                ord('q'): 'exit',
                ord('Q'): 'exit',
                ord('e'): 'exposure',
                ord('E'): 'exposure',
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
            }[cv2.waitKeyEx(10)]
            if status == 'play':
                pipe.reset()  # Clean the queue buffer before retrieving frame
                continue
            if status == 'exit':
                cv2.destroyAllWindows()
                pipe.pause()
                break
            if status == 'exposure':
                flag["exposure"] = not (flag["exposure"])
                if flag["exposure"]:
                    logger.info("Enable exposure")
                    camera_property.enable_AE()
                else:
                    logger.info("Disable exposure")
                    camera_property.disable_AE()
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


def calculate_roi(x, y, w, h, depth_roi, z_map):
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


def depth_roi_callback(event, x_, y_, flag, param):
    # Update coord x and y
    global x, y
    x = x_
    y = y_
