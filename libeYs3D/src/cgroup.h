/*
 * Copyright (C) 2015-2019 ICL/ITRI
 * All rights reserved.
 *
 * NOTICE:  All information contained herein is, and remains
 * the property of ICL/ITRI and its suppliers, if any.
 * The intellectual and technical concepts contained
 * herein are proprietary to ICL/ITRI and its suppliers and
 * may be covered by Taiwan and Foreign Patents,
 * patents in process, and are protected by trade secret or copyright law.
 * Dissemination of this information or reproduction of this material
 * is strictly forbidden unless prior written permission is obtained
 * from ICL/ITRI.
 */

#pragma once

#define CAMERA_READER_CGROUP      "eYs3D/readers"
#define IMU_READER_CGROUP         "eYs3D/readers"

#define COLOR_CODER_CGROUP        "eYs3D/coders"
#define DEPTH_RGB_CODER_CGROUP    "eYs3D/depth_rgb_coder"
#define DEPTH_FILTER_CODER_CGROUP "eYs3D/depth_filter_coder"
#define PC_CODER_CGROUP           "eYs3D/coders"

#define COLOR_CALLBACK_CGROUP     "eYs3D/callbacks"
#define DEPTH_CALLBACK_CGROUP     "eYs3D/callbacks"
#define PC_CALLBACK_CGROUP        "eYs3D/callbacks"
#define IMU_CALLBACK_CGROUP       "eYs3D/callbacks"

void initialize_cgroup();
void attach_to_cgroup(const char *cgroupName, const char *log_tag);
