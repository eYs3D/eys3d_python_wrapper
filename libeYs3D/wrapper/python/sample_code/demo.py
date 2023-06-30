import os
import sys

import argparse

from eys3d import EYS3DSystem, Device, Config, COLOR_RAW_DATA_TYPE, DEPTH_RAW_DATA_TYPE, DEPTH_TRANSFER_CTRL, USB_PORT_TYPE

from cv_demo import cv_sample
from pc_demo import pc_sample
from accuracy_demo import accuracy_sample
from callback_demo import callback_sample
from record_playback import record_playback_sample


def preview_config(config):
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


def determine_device(camera_list, input_module):
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
    parser.add_argument("--module",
                        "-m",
                        default="8062",
                        type=str,
                        help="module name. Default module is 8062.")
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
    #pipe = Pipeline(args.device_index)
    camera_list = []
    camera_device_count = EYS3DSystem().get_camera_device_count()
    for idx in range(camera_device_count):
        device = Device(camera_index=idx)
        if args.module in device.get_device_info()['firmware_version'].split(
                '-')[0]:
            camera_list.append(device)
    device = determine_device(
        camera_list, args.module
    )  # To determine the module input is same as selected device.

    conf = Config()

    if "8053" == args.module:
        # conf.set_color_stream(
        #     COLOR_RAW_DATA_TYPE.COLOR_RAW_DATA_MJPG,
        #     1280,
        #     720,
        #     fps=30,
        # )
        # conf.set_depth_stream(
        #     DEPTH_TRANSFER_CTRL.DEPTH_IMG_COLORFUL_TRANSFER,
        #     640,
        #     360,
        #     fps=30,
        # )
        # conf.set_depth_data_type_with_advanced_setting(11, is_rectify=True, is_interleave_mode=True)

        conf.set_preset_mode_config(0x138, args.index, device.get_usb_type())

    elif "8052" == args.module:
        # conf.set_color_stream(
        #     COLOR_RAW_DATA_TYPE.COLOR_RAW_DATA_YUY2,
        #     1280,
        #     720,
        #     fps=60,
        # )
        # conf.set_depth_stream(
        #     DEPTH_TRANSFER_CTRL.DEPTH_IMG_COLORFUL_TRANSFER,
        #     1280,
        #     720,
        #     fps=60,
        # )
        # conf.set_depth_data_type_with_advanced_setting(11, is_rectify=True, is_interleave_mode=False)
        conf.set_preset_mode_config(0x137, args.index, device.get_usb_type())

    elif "8059" == args.module:
        conf.set_preset_mode_config(0x146, args.index, device.get_usb_type())
    elif "8067" == args.module:
        conf.set_preset_mode_config(0x12C, args.index, device.get_usb_type())
    elif "HYPATIA" == args.module: # 8071
        conf.set_preset_mode_config(0x160, args.index, device.get_usb_type()) 
    elif "HYPATIA2" == args.module:
        conf.set_preset_mode_config(0x173, args.index, device.get_usb_type())
    elif "Stacy" == args.module: # 8071
        conf.set_preset_mode_config(0x188, args.index, device.get_usb_type()) 
    elif "StacyJunior" == args.module:
        conf.set_preset_mode_config(0x189, args.index, device.get_usb_type())
    elif "8036" == args.module:
        conf.set_preset_mode_config(0x120, args.index, device.get_usb_type())
    elif "80362" == args.module:
        conf.set_preset_mode_config(0x181, args.index, device.get_usb_type())
    elif "8081" == args.module:
        conf.set_preset_mode_config(0x183, args.index, device.get_usb_type())
    elif "8062" == args.module:
        # conf.set_color_stream(
        #     COLOR_RAW_DATA_TYPE.COLOR_RAW_DATA_YUY2,
        #     1280,
        #     720,
        #     fps=30,
        # )
        # conf.set_depth_stream(
        #     DEPTH_TRANSFER_CTRL.DEPTH_IMG_NON_TRANSFER,  # DEPTH_TRANSFER_CTRL
        #     1280,
        #     720,
        #     fps=30,
        # )
        # conf.set_depth_data_type_with_advanced_setting(14, is_rectify=True, is_interleave_mode=True)
        conf.set_preset_mode_config(0x162, args.index, device.get_usb_type())
    else:
        print("Please input correct module name")
        sys.exit()
    # Manual set fps and depth bit:
    if args.depth_bit:
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

    while True:
        print("\n\n\n\tCamera module: {}, mode index: {}. USB: {}".format(
            args.module, args.index, device.get_usb_type()))
        preview_config(conf)
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
