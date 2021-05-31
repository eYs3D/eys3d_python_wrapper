'''
 Copyright (C) 2015-2019 ICL/ITRI
 All rights reserved.

 NOTICE:  All information contained herein is, and remains
 the property of ICL/ITRI and its suppliers, if any.
 The intellectual and technical concepts contained
 herein are proprietary to ICL/ITRI and its suppliers and
 may be covered by Taiwan and Foreign Patents,
 patents in process, and are protected by trade secret or copyright law.
 Dissemination of this information or reproduction of this material
 is strictly forbidden unless prior written permission is obtained
 from ICL/ITRI.
'''

from configshell_fb import ExecutionError

from .ui_node import UINode
from .ui_control import CVDemoControl, ModeControl, DepthFilteringControl, InterleaveControl, PCDemoControl, CBDemoControl, AccuracyDemoControl, RPDemoControl

from eys3d import ModeConfig, Config, DECODE_TYPE


class ModeConfigUI(UINode):
    '''
    A ModeConfig UI.
    '''
    def __init__(self, name, parent, camera_device):
        UINode.__init__(self, name, parent)
        self.camera_device = camera_device
        self.pid = int(self.camera_device.get_device_info()['dev_info']['PID'])
        self.usb_type = camera_device.get_usb_type()
        self.mode_config = ModeConfig(self.pid, 1, self.usb_type)

        self.refresh()

    def refresh(self):
        self._children = set([])
        max_index = self.mode_config.get_mode_count()
        base_index = self.mode_config.get_current_index()
        for i in range(max_index):
            self.mode_config.select_current_index(base_index + i)
            config = Config()
            config.set_preset_mode_config(self.pid, (base_index + i),
                                          self.usb_type)
            Mode(self.camera_device, config, self.mode_config, self)

    def get_module_info(self):
        print(
            "\n\n\t\t\tCamera module information\n\t\t\t************************************"
        )
        for k, v in self.camera_device.get_device_info().items():
            print("\t\t\t{}: {}".format(k, v))


class Mode(UINode):
    '''
    A Mode UI
    '''
    def __init__(self, device, config, mode_config, parent):
        self.dev = device
        self.conf = config
        self.mode_config = mode_config
        self.mode_info = self.mode_config.get_current_mode_info()
        node_name = "Mode_{}".format(self.mode_info.iMode)
        UINode.__init__(self, node_name, parent)
        self.refresh()
        self.config_dict = {}  # dictionary for config
        self.__update_config()

    def refresh(self):
        self._children = set([])
        config_dict = self.conf.get_config()
        if not (config_dict['colorHeight'] == 0
                or config_dict['depthHeight'] == 0):
            PCDemoControl("PC_demo", self, self.dev, self.conf, self.mode_info)
            RPDemoControl("Record_Playback_demo", self, self.dev, self.conf,
                          self.mode_info)
        CVDemoControl("CV_demo", self, self.dev, self.conf, self.mode_info)
        CBDemoControl("Callback_demo", self, self.dev, self.conf,
                      self.mode_info)
        if config_dict['depthHeight'] is not 0:
            AccuracyDemoControl("Accuracy_demo", self, self.dev, self.conf,
                                self.mode_info)

    def get_module_info(self):
        print(
            "\n\n\t\t\tCamera module information\n\t\t\t************************************"
        )
        for k, v in self.dev.get_device_info().items():
            print("\t\t\t{}: {}".format(k, v))

    def set_fps(self, fps):
        try:
            fps = int(fps)
        except ValueError:
            print(ValueError)
        if fps not in self.mode_info.vecColorFps and fps not in self.mode_info.vecDepthFps:
            print("The fps is not available for this mode.")
            print("The acceptable value : {}".format(
                self.mode_info.vecColorFps if len(self.mode_info.vecColorFps)
                else self.mode_info.vecDepthFps))
        else:
            self.config_dict["fps"] = fps
            self.conf.set_fps(fps)

    def set_depth_bits(self, depth_bit):
        try:
            depth_bit = int(depth_bit)
        except ValueError:
            print(ValueError)
        if depth_bit not in self.mode_info.vecDepthType:
            print("The depth bits is not available for this mode.")
            print("The acceptable value: {}".format(
                self.mode_info.vecDepthType))
        else:
            self.config_dict["depth_bit"] = depth_bit
            self.conf.set_depth_data_type(depth_bit)

    def summary(self):
        summary = ""
        if self.config_dict["color_width"]:
            summary += "Color: {0}*{1} {2}, ".format(
                self.config_dict["color_width"],
                self.config_dict["color_height"], self.config_dict["format"])
        if self.config_dict["depth_width"]:
            summary += ("Depth: {0}*{1} {2}, ".format(
                self.config_dict["depth_width"],
                self.config_dict["depth_height"], "YUV"))
        if self.config_dict["fps"]:
            summary += ("Fps: {}, ".format(self.config_dict["fps"]))

        if self.config_dict["usb"]:
            summary += "USB: {}, ".format(self.config_dict["usb"])

        if self.config_dict["depth_bit"]:
            summary += "Depthmap bits: {}, ".format(
                self.config_dict["depth_bit"])

        if self.config_dict["fps"] == self.config_dict["interleavefps"]:
            summary += "ILM: On"
        else:
            summary += "ILM: Off"

        return (summary, True)

    def __update_config(self):
        self.config_dict["color_width"] = self.mode_info.L_Resolution.Width
        self.config_dict["color_height"] = self.mode_info.L_Resolution.Height
        self.config_dict["depth_width"] = self.mode_info.D_Resolution.Width
        self.config_dict["depth_height"] = self.mode_info.D_Resolution.Height
        self.config_dict[
            "format"] = "YUV" if self.mode_info.eDecodeType_L == DECODE_TYPE.YUYV else "MJPEG"
        ep0fps = 0 if not self.mode_info.vecColorFps else self.mode_info.vecColorFps[
            0]
        ep1fps = 0 if not self.mode_info.vecDepthFps else self.mode_info.vecDepthFps[
            0]
        self.config_dict["fps"] = ep0fps if ep0fps else ep1fps
        self.config_dict["depth_bit"] = self.mode_info.vecDepthType[0] if len(
            self.mode_info.vecDepthType) != 0 else 0
        self.config_dict["usb"] = self.mode_info.iUSB_Type
        self.config_dict["interleavefps"] = self.mode_info.iInterLeaveModeFPS
