"""eYs3D Python SDK Demo Application.

Interactive demo for eYs3D stereo cameras. Allows selecting camera mode
and running various sample applications.

Usage:
    python demo.py -m 0x0202 -i 1 --depth-bit 14

Arguments:
    --module_pid/-m: Product ID (hex string, e.g., "0x0202" for G120C)
    --index/-i: Mode index from ModeConfig.db (default: 1)
    --depth-bit: Depth precision (8, 11, or 14 bits)

Supported Cameras:
    - G120C (PID 0x0202): eSP936 series chip, interleave mode
    - G120IR (PID 0x0211): eSP936 series chip IR variant
    - 8062 (PID 0x181): G100i
    - 8052 (PID 0x137): G50
    - And more - see ModeConfig.db for full list
"""

import os
import sys
import argparse
from typing import Dict, List, Optional

from eys3d import EYS3DSystem, Device, Config, COLOR_RAW_DATA_TYPE, DEPTH_RAW_DATA_TYPE, DEPTH_TRANSFER_CTRL, USB_PORT_TYPE

from cv_demo import cv_sample
from pc_demo import pc_sample
from accuracy_demo import accuracy_sample
from callback_demo import callback_sample
from record_playback import record_playback_sample


def preview_config(config: Config, product_id: int) -> None:
    """Print current configuration to console.

    Displays stream resolutions, format, depth bits, FPS, and mode settings.
    Handles both G120 (eSP936 series chip) and traditional camera formats.

    Args:
        config: Current Config object.
        product_id: Camera PID for device-specific formatting.
    """
    config_dict = config.get_config()
    print("\n\tConfig information")
    if config_dict['colorWidth'] != 0:
        print("\tColor Stream:[{}x{}]\t{}".format(
            config_dict['colorWidth'], config_dict['colorHeight'],
            "YUV" if config_dict['colorFormat']
            == COLOR_RAW_DATA_TYPE.COLOR_RAW_DATA_YUY2 else "MJPG"))
    if config_dict['depthWidth'] != 0:
        print("\tDepth Stream:[{}x{}]\tYUV".format(
            config_dict['depthWidth'], config_dict['depthHeight'],
            config_dict['depthStreamFormat']))
    # Determine depth bits based on device type
    is_G120 = (product_id == 0x0202 or product_id == 0x0211)
    if is_G120:
        # eSP936 series chip (G120) depth format values:
        # 0x00 = Color Only (Non-rectified)
        # 0x18 = 11-bit non-ILM or Color Only (Rectified)
        # 0x19 = 14-bit non-ILM
        # 0x1a = 11-bit ILM
        # 0x1b = 14-bit ILM
        depth_value = config_dict['depthFormat'].value
        if depth_value == 0x00:  # Color Only (Non-rectified)
            depth_format_bit = None
        elif depth_value == 0x18:  # 11-bit or Color Only (Rectified)
            # Check if depth stream exists to distinguish
            depth_format_bit = 11 if config_dict['depthWidth'] > 0 else None
        elif depth_value == 0x1a:  # 11-bit ILM
            depth_format_bit = 11
        elif depth_value in (0x19, 0x1b):  # 14-bit non-ILM, 14-bit ILM
            depth_format_bit = 14
        else:
            depth_format_bit = None
    else:
        # Other devices (PUMA, etc.)
        if config_dict['depthFormat'] in (
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_8_BITS,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_8_BITS_RAW,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_ILM_8_BITS,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_ILM_8_BITS_RAW,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_SCALE_DOWN_8_BITS,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_SCALE_DOWN_8_BITS_RAW,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_SCALE_DOWN_ILM_8_BITS,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_SCALE_DOWN_ILM_8_BITS_RAW):
            depth_format_bit = 8
        elif config_dict['depthFormat'] in (
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_11_BITS,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_11_BITS_RAW,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_ILM_11_BITS,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_ILM_11_BITS_RAW,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_SCALE_DOWN_11_BITS,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_SCALE_DOWN_11_BITS_RAW,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_SCALE_DOWN_ILM_11_BITS,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_SCALE_DOWN_ILM_11_BITS_RAW):
            depth_format_bit = 11
        elif config_dict['depthFormat'] in (
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_14_BITS,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_14_BITS_RAW,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_ILM_14_BITS,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_ILM_14_BITS_RAW,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_SCALE_DOWN_14_BITS,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_SCALE_DOWN_14_BITS_RAW,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_SCALE_DOWN_ILM_14_BITS,
                DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_SCALE_DOWN_ILM_14_BITS_RAW):
            depth_format_bit = 14
        else:
            depth_format_bit = None

    print("\tDepthmap Bits: {}".format(depth_format_bit))
    print("\tFps: {}".format(config_dict["actualFps"]))
    print("\tRectify: {}".format(config_dict['rectify']))
    print("\tVideo Mode: {}".format(config_dict['depthFormat']))
    print("\tInterleave mode: {}\n\n".format(
        True if config_dict["ILM"] == config_dict["actualFps"] else False))


def determine_device(camera_list: List[Device]) -> Device:
    """Prompt user to select a camera if multiple are connected.

    Args:
        camera_list: List of Device objects matching the requested PID.

    Returns:
        Selected Device instance.

    Raises:
        NameError: If camera_list is empty.
    """
    if len(camera_list) == 0:
        raise NameError("Module input is not plugged on host.")
    if len(camera_list) > 1:
        while True:
            print("\n\n\teYs3D depth camera list")
            for idx, d in enumerate(camera_list):
                dev_info = d.get_device_info()
                print("\t{}. {}({})".format(idx, dev_info['firmware_version'],
                                            dev_info['dev_info']['dev_name']))
            camera_index = input(
                "\tPlease input which camera should be chosen? ")
            try:
                if int(camera_index) in range(len(camera_list)):
                    device = camera_list[int(camera_index)]
                    break
                else:
                    print("\tPlease input correct index!")
            except (TypeError, ValueError) as e:
                print("\tError: {}.Please input correct index!".format(e))
    else:
        device = camera_list[0]

    return device


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--module_pid",
                        "-m",
                        default="0x204",
                        type=str,
                        help="Module product ID. Execute $ lsusb")
    parser.add_argument(
        "--index",
        "-i",
        default=1,
        type=int,
        help="mode index for config setting. Default index is 1.")
    parser.add_argument(
        "--depth-bit",
        type=int,
        help=
        "eYs3D DepthDataType for setting.options are 8, 11 and 14 to choose")
    args = parser.parse_args()

    camera_list = []
    camera_device_count = EYS3DSystem().get_camera_device_count()

    if args.module_pid:
        pid = int(args.module_pid, 16)  # Convert string to hexadecimal int
        print(f"User assigned product id {pid}")
    else:
        print(f"Unable to detect product id for module, could you specify it in the command ?")
        sys.exit(1)

    for idx in range(camera_device_count):
        device = Device(camera_index=idx)
        dev_info = device.get_device_info()
        detected_pid = dev_info['dev_info']["PID"]
        if pid == detected_pid:
            camera_list.append(device)

    device = determine_device(camera_list)

    conf = Config()
    conf.set_preset_mode_config(pid, args.index, device.get_usb_type(), args.depth_bit)

    # Manual set fps and depth bit (for non-G120 cameras only, G120 handles depth_bits in set_preset_mode_config)
    is_G120 = (pid == 0x0202 or pid == 0x0211)
    if args.depth_bit and not is_G120:
        conf.set_depth_data_type(args.depth_bit)

    if conf.get_config()['colorHeight'] and conf.get_config()['depthHeight']:
        sample_list = {
            "cv_demo": cv_sample,
            "pc_demo": pc_sample,
            "callback_demo": callback_sample,
            "accuracy_demo": accuracy_sample,
            # "record_playback_demo": record_playback_sample
        }
    elif conf.get_config()['depthHeight']:  # Depth only
        sample_list = {
            "cv_demo": cv_sample,
            "callback_demo": callback_sample,
            "accuracy_demo": accuracy_sample
        }
    elif conf.get_config()['colorHeight']:  # Color only
        sample_list = {
            "cv_demo": cv_sample,
            "callback_demo": callback_sample,
        }
    else:
        print("Parameter wrong ? Please check or contact eYs3D FAE.")
        sys.exit()

    while True:
        print("\n\n\n\tCamera pid: {}, mode index: {}. USB: {}".format(
            args.module_pid, args.index, device.get_usb_type()))
        preview_config(conf, detected_pid)
        print("\tSample code: ")
        for idx, term in enumerate(sample_list):
            print("\t{}. {}".format(idx + 1, term))
        print("\t{}. Exit".format(len(sample_list) + 1))
        sample_index = input(
            "\tPlease input the index of sample you would like to execute(1~{})? \t"
            .format(len(sample_list) + 1))
        try:
            if int(sample_index) in range(1, len(sample_list) + 2):
                sample_index = int(sample_index)
                break
        except ValueError:
            print("\t******Please input again*******")

    if sample_index == len(sample_list) + 1:
        print("Exit sample code")
        sys.exit()
    else:
        list(sample_list.values())[(sample_index) - 1](device, conf)
