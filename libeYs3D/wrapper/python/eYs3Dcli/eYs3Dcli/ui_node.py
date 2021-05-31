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
import sys
import six

from configshell_fb import ConfigNode, ExecutionError
from .version import __version__ 

class UINode(ConfigNode):
    '''
    eYs3Dcli basic UI node.
    '''
    def __init__(self, name, parent=None, shell=None):
        ConfigNode.__init__(self, name, parent, shell)

    def refresh(self):
        '''
        Refreshes and updates the objects tree from the current path.
        '''
        for child in self.children:
            child.refresh()

    def ui_command_get_version(self):
        print("\n\n\t\t\teYs3D python package version: {}".format(__version__))

    def ui_command_get_module_info(self):
        try:
            self.get_module_info()
        except AttributeError:
            print("This node is no `get_module_info` action!!")

    def ui_command_set_fps(self, fps):
        try:
            self.set_fps(fps)
        except AttributeError:
            print("This node is no `set_fps` action !!")

    def ui_command_set_depth_bits(self, depth_bit):
        try:
            self.set_depth_bits(depth_bit)
        except AttributeError:
            print("This node is no `set_depth_bits` action !!")

    def ui_command_refresh(self):
        '''
        Refreshes and updates the objects tree from the current path.
        '''
        self.refresh()

    def ui_command_status(self):
        '''
        Displays the current node's status summary.
        SEE ALSO
        ========
        ls
        '''
        description, is_healthy = self.summary()
        self.shell.log.info("%s" % (description))

    def ui_command_execute(self):
        try:
            self.execute()
        except AttributeError:
            print("This node is no `execute` action!!")
    
    def ui_command_exit(self):
        try:
            self.camera_device.release()
        except AttributeError:
            pass
        return 'EXIT'

    def assert_root(self):
        '''
        For commands requiring root privileges, disable command if not the root
        node's as_root attribute is False.
        '''
        root_node = self.get_root()
        if hasattr(root_node, 'as_root') and not self.get_root().as_root:
            raise ExecutionError("This privileged command is disabled: " +
                                 "you are not root.")

    def new_node(self, new_node):
        '''
        Used to honor global 'auto_cd_after_create'.
        Either returns None if the global is False, or the new_node if the
        global is True. In both cases, set the @last bookmark to last_node.
        '''
        self.shell.prefs['bookmarks']['last'] = new_node.path
        self.shell.prefs.save()
        if self.shell.prefs['auto_cd_after_create']:
            self.shell.log.info("Entering new node %s" % new_node.path)
            # Piggy backs on cd instead of just returning new_node,
            # so we update navigation history.
            return self.ui_command_cd(new_node.path)
        else:
            return None
