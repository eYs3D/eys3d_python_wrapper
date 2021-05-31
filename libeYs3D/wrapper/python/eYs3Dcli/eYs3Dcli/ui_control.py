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
import os
import sys

from configshell_fb import ExecutionError

from .ui_node import UINode
from sample_code.cv_demo import cv_sample
from sample_code.pc_demo import pc_sample
from sample_code.callback_demo import callback_sample
from sample_code.accuracy_demo import accuracy_sample
from sample_code.record_playback import record_playback_sample


class Control(UINode):
    '''
    A control UI.
    Abstract Base Class, do not instantiate.
    '''
    def __init__(self, plugin, parent):
        UINode.__init__(self, plugin, parent)
        # self.parent = parent
        self.refresh()

    def set_fps(self, fps):
        self.parent.set_fps(fps)

    def set_depth_bits(self, depth_bit):
        self.parent.set_depth_bits(depth_bit)


class ModeControl(Control):
    '''
    A mode control UI.
    '''
    def __init__(self, plugin, parent):
        Control.__init__(self, plugin, parent)
        self.refresh()


class CVDemoControl(Control):
    '''
    A cv demo control UI.
    '''
    def __init__(self, plugin, parent, device, config, mode_info):
        Control.__init__(self, plugin, parent)
        self.camera_device = device
        self.config = config
        self.mode_info = mode_info

    def execute(self):
        cv_sample(self.camera_device, self.config)


class PCDemoControl(Control):
    '''
    A pointcloud demo control UI.
    '''
    def __init__(self, plugin, parent, device, config, mode_info):
        Control.__init__(self, plugin, parent)
        self.camera_device = device
        self.config = config
        self.mode_info = mode_info

    def execute(self):
        if self.config.get_config()['colorHeight'] is 0:
            print(Exception("This mode does not execute point cloud preview."))
        else:
            pc_sample(self.camera_device, self.config)


class CBDemoControl(Control):
    '''
    A callback demo control UI.
    '''
    def __init__(self, plugin, parent, device, config, mode_info):
        Control.__init__(self, plugin, parent)
        self.camera_device = device
        self.config = config
        self.mode_info = mode_info

    def execute(self):
        callback_sample(self.camera_device, self.config)


class AccuracyDemoControl(Control):
    '''
    A Accuracy demo control UI.
    '''
    def __init__(self, plugin, parent, device, config, mode_info):
        Control.__init__(self, plugin, parent)
        self.camera_device = device
        self.config = config
        self.mode_info = mode_info

    def execute(self):
        if self.config.get_config()['depthHeight'] is 0:
            print(Exception("This mode does not execute accuracy demo."))
        else:
            accuracy_sample(self.camera_device, self.config)


class RPDemoControl(Control):
    '''
    A Accuracy demo control UI.
    '''
    def __init__(self, plugin, parent, device, config, mode_info):
        Control.__init__(self, plugin, parent)
        self.camera_device = device
        self.config = config
        self.mode_info = mode_info

    def execute(self):
        if self.config.get_config()['depthHeight'] is 0:
            print(
                Exception("This mode does not execute record_playback_demo."))
        else:
            record_playback_sample(self.camera_device, self.config)


class DepthFilteringControl(Control):
    '''
    A depth filtering control UI.
    '''
    def __init__(self, plugin, parent):
        Control.__init__(self, plugin, parent)
        self.refresh()


class InterleaveControl(Control):
    '''
    A interleave control UI.
    '''
    def __init__(self, plugin, parent):
        Control.__init__(self, plugin, parent)
        self.refresh()


class PointCloudControl(Control):
    '''
    A Point Cloud control UI.
    '''
    def __init__(self, plugin, parent):
        Control.__init__(self, plugin, parent)
        self.refresh()
