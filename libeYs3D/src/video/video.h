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

namespace libeYs3D    {
namespace video    {

typedef enum    {
    COLOR_RAW_DATA_YUY2 = EtronDIImageType::COLOR_YUY2,
    COLOR_RAW_DATA_MJPG = EtronDIImageType::COLOR_MJPG,
} COLOR_RAW_DATA_TYPE;

#define DEPTH_RAW_DATA_INTERLEAVE_MODE_OFFSET    16

// reference eSPDI/eSPDI_def.h
typedef enum    {
    DEPTH_RAW_DATA_OFF_RAW = ETronDI_DEPTH_DATA_OFF_RAW,         /* raw (depth off, only raw color) */
    DEPTH_RAW_DATA_DEFAULT = ETronDI_DEPTH_DATA_DEFAULT,         /* raw (depth off, only raw color) */
    DEPTH_RAW_DATA_8_BITS = ETronDI_DEPTH_DATA_8_BITS,           /* rectify, 1 byte per pixel */
    DEPTH_RAW_DATA_14_BITS = ETronDI_DEPTH_DATA_14_BITS,         /* rectify, 2 byte per pixel */
    DEPTH_RAW_DATA_8_BITS_x80 = ETronDI_DEPTH_DATA_8_BITS_x80,   /* rectify, 2 byte per pixel but using 1 byte only */
    DEPTH_RAW_DATA_11_BITS = ETronDI_DEPTH_DATA_11_BITS,         /* rectify, 2 byte per pixel but using 11 bit only */
    DEPTH_RAW_DATA_OFF_RECTIFY = ETronDI_DEPTH_DATA_OFF_RECTIFY, /* rectify (depth off, only rectify color) */
    DEPTH_RAW_DATA_8_BITS_RAW = ETronDI_DEPTH_DATA_8_BITS_RAW,         /* raw */
    DEPTH_RAW_DATA_14_BITS_RAW = ETronDI_DEPTH_DATA_14_BITS_RAW,       /* raw */
    DEPTH_RAW_DATA_8_BITS_x80_RAW = ETronDI_DEPTH_DATA_8_BITS_x80_RAW, /* raw */
    DEPTH_RAW_DATA_11_BITS_RAW = ETronDI_DEPTH_DATA_11_BITS_RAW,       /* raw */
    DEPTH_RAW_DATA_14_BITS_COMBINED_RECTIFY = ETronDI_DEPTH_DATA_14_BITS_COMBINED_RECTIFY,
    DEPTH_RAW_DATA_11_BITS_COMBINED_RECTIFY = ETronDI_DEPTH_DATA_11_BITS_COMBINED_RECTIFY, // multi-baseline
    
    // For Interleave mode depth data type
    DEPTH_RAW_DATA_ILM_OFF_RAW = ETronDI_DEPTH_DATA_ILM_OFF_RAW,
    DEPTH_RAW_DATA_ILM_DEFAULT = ETronDI_DEPTH_DATA_ILM_DEFAULT,
    DEPTH_RAW_DATA_ILM_8_BITS = ETronDI_DEPTH_DATA_ILM_8_BITS,
    DEPTH_RAW_DATA_ILM_14_BITS = ETronDI_DEPTH_DATA_ILM_14_BITS,
    DEPTH_RAW_DATA_ILM_8_BITS_x80 = ETronDI_DEPTH_DATA_ILM_8_BITS_x80,
    DEPTH_RAW_DATA_ILM_11_BITS = ETronDI_DEPTH_DATA_ILM_11_BITS,
    DEPTH_RAW_DATA_ILM_OFF_RECTIFY = ETronDI_DEPTH_DATA_ILM_OFF_RECTIFY,
    DEPTH_RAW_DATA_ILM_8_BITS_RAW = ETronDI_DEPTH_DATA_ILM_8_BITS_RAW,
    DEPTH_RAW_DATA_ILM_14_BITS_RAW = ETronDI_DEPTH_DATA_ILM_14_BITS_RAW,
    DEPTH_RAW_DATA_ILM_8_BITS_x80_RAW = ETronDI_DEPTH_DATA_ILM_8_BITS_x80_RAW,
    DEPTH_RAW_DATA_ILM_11_BITS_RAW = ETronDI_DEPTH_DATA_ILM_11_BITS_RAW,
    DEPTH_RAW_DATA_ILM_14_BITS_COMBINED_RECTIFY = ETronDI_DEPTH_DATA_ILM_14_BITS_COMBINED_RECTIFY,
    DEPTH_RAW_DATA_ILM_11_BITS_COMBINED_RECTIFY = ETronDI_DEPTH_DATA_ILM_11_BITS_COMBINED_RECTIFY,
} DEPTH_RAW_DATA_TYPE;

} // namespace video
} // namespace libeYs3D
