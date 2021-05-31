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

from eys3d import Device, EYS3DSystem

from configshell_fb import ExecutionError

from .ui_node import UINode
from .ui_control import ModeControl, DepthFilteringControl, InterleaveControl
from .ui_modeConfig import ModeConfigUI

class CameraDevices(UINode):
    '''
    The camera devices container UI.
    '''
    def __init__(self, parent):
        UINode.__init__(self, 'Camera_Devices', parent)
        self.refresh()

    def refresh(self):
        self._children = set([])

        # TODO: dynamically create CameraDevice nodes here
        system = EYS3DSystem()
        device_count = system.get_camera_device_count()
        if device_count is 0:
            raise Exception("The depth camera device is not found")
        device = []
        for i in range(device_count):
            device.append(Device(i))
        #device[0] = Device(0)
        mode_name = [d.get_device_info()['serial_number'] for d in device]

        for i in range(len(device)):
            CameraDevice(mode_name[i], self, device[i])
        #CameraDevice("QHD Depth Camera: QHD Depth Camer", self)
        #CameraDevice("Full HD Depth Camera: Full HD Depth Camer", self)

    def summary(self):
        return ("%d camera devices" % len(self._children), True)


class CameraDevice(UINode):
    '''
    A camera device UI.
    '''
    def __init__(self, name, parent, camera_device):
        UINode.__init__(self, name, parent)
        self.camera_device = camera_device
        self.refresh()

    def refresh(self):
        self._children = set([])

        #ModeInfo("Mode information", self)
        ModeConfigUI("Mode_config", self, self.camera_device)
        # ModeControl("mode_control", self)
        # DepthFilteringControl("depth_filtering_control", self)
        # InterleaveControl("interleave_control", self)

    def get_module_info(self):
        print("\n\n\t\t\tCamera module information\n\t\t\t************************************")
        for k, v in self.camera_device.get_device_info().items():
            print("\t\t\t{}: {}".format(k, v))

    def summary(self):
        dev_name = self.camera_device.get_device_info()['dev_info']['dev_name']

        return (dev_name, True)
