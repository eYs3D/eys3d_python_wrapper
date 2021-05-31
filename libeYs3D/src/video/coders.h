/*
 * Copyright (C) 2015-2017 ICL/ITRI
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

#ifdef WIN32
#  include "eSPDI_Common.h"
#else
#  include "eSPDI_def.h"
#endif
//#include "devices/CameraDevice.h"

#include <stdint.h>

// forward declaration
namespace libeYs3D    {
    namespace devices    {
        class CameraDevice;
    }
}

using libeYs3D::devices::CameraDevice;

namespace libeYs3D    {
namespace video    {

struct Frame;

static inline EtronDIImageType::Value depth_raw_type_to_depth_image_type(uint32_t depth_raw_type)    {
    return EtronDIImageType::DepthDataTypeToDepthImageType((unsigned short)depth_raw_type);
}

static inline int get_color_image_format_byte_length_per_pixel(EtronDIImageType::Value format)    {
    switch (format){
        case EtronDIImageType::COLOR_MJPG:
        case EtronDIImageType::COLOR_YUY2:
            return 2;
        case EtronDIImageType::COLOR_RGB24:
            return 3;
        default:
            return 0;
    }
}

static inline int get_depth_image_format_byte_length_per_pixel(EtronDIImageType::Value format)    {
    switch (format){
        case EtronDIImageType::DEPTH_8BITS:
            return 4;
        case EtronDIImageType::DEPTH_8BITS_0x80:
            return 2;
        case EtronDIImageType::DEPTH_11BITS:
            return 2;
        case EtronDIImageType::DEPTH_14BITS:
            return 2;
        default:
            return 0;
    }
}

int color_image_produce_rgb_frame(const CameraDevice *cameraDevice, Frame *frame);
int depth_image_produce_rgb_frame(const CameraDevice *cameraDevice, Frame *frame);

int convert_yuv_to_rgb_buffer(uint8_t *yuv, uint8_t *rgb,
                              int32_t width, int32_t height,
                              uint64_t* rgb_actual_size);

#if 0
int turbo_jpeg_jpeg2yuv(uint8_t* jpeg_buffer, uint64_t jpeg_size, uint8_t *yuv_buffer,
                        uint64_t* yuv_actual_size, int32_t* yuv_type);
int turbo_jpeg_yuv2rgb(uint8_t* yuv_buffer, uint64_t yuv_size, int32_t width, int32_t height,
                       int sub_sample, uint8_t* rgb_buffer, uint64_t* rgb_actual_size);
#endif
} // endo of namespace video
} // endo of namespace libeYs3D
