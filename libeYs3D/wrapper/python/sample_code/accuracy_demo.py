"""A simple demo to demonstrate DepthAccuracy function.

User need to pass module name , mode index, region ratio and ground truth distance.
This demo would only preview depth frame and calculate the depth accuracy.

Ex: sh run_accuracy_demo.sh 8062 1 0.2 300

Notice: 
Region ratio and ground truth distance are optional.
It is normal if user could not pass region ratio. 

It does not guarantee the performance when depth accuracy is enabled.
"""
import sys
import time

import cv2
import argparse
import numpy as np
from threading import Lock

from eys3d import Pipeline, Config


def accuracy_sample(device, config):
    region_ratio = float(input("Please input region ratio ( 0 ~ 1.0 ): "))
    ground_truth = float(input("Please input ground truth ( 1 ~ 300)(mm): "))
    pipe = Pipeline(device=device)
    conf = config
    depth_resolution = conf.get_depth_stream_resolution()
    pipe.start(conf)

    # DepthAccuracy
    if region_ratio > 0:
        depthAccuracy = pipe.get_depthAccuracy()
        depthAccuracy.enable()
        depthAccuracy.set_region_ratio(region_ratio)
        depthAccuracy.set_groundTruth_distance(ground_truth)
        print("[Python][Accuracy] Enable? {}".format(
            depthAccuracy.is_enabled()))
        print("[Python][Accuracy] Ragion ratio: {:.2f}".format(
            depthAccuracy.get_region_ratio()))
        print("[Python][Accuracy] Ground Truth: {:.2f}".format(
            depthAccuracy.get_groundTruth_distance()))

    pipe.reset()
    while 1:
        dret, dframe = pipe.get_depth_frame()  #unblock mode
        if not dret:
            continue
        bgr_dframe = cv2.cvtColor(
            dframe.get_rgb_data().reshape(*depth_resolution, 3),
            cv2.COLOR_RGB2BGR)
        if region_ratio > 0:
            (h, w, _) = bgr_dframe.shape
            cv2.rectangle(bgr_dframe, (int(w * (1 - region_ratio) // 2),
                                       int(h * (1 - region_ratio) // 2)),
                          (int(w * (1 + region_ratio) // 2),
                           int(h * (1 + region_ratio) // 2)), (0, 255, 255), 5)
        cv2.imshow("Depth image", bgr_dframe)
        accuracy_info = dframe.get_depth_accuracy_info()
        accuracy_info_str = ""
        for key, value in accuracy_info.items():
            accuracy_info_str += "{}: {:.4f}\t".format(key, value)
        cv2.displayStatusBar("Depth image", accuracy_info_str, 1000)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            depthAccuracy.disable(
            )  # It need to disable manually to avoid seq fault before pipeline stopped.
            cv2.destroyAllWindows()
            break
    pipe.stop()
