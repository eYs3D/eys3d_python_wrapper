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

#include "CameraDevice.h"

namespace libeYs3D    {
namespace devices    {

class CameraDevice8059: public CameraDevice    {
public:
    virtual int initStream(libeYs3D::video::COLOR_RAW_DATA_TYPE colorFormat,
                           int32_t colorWidth, int32_t colorHeight, int32_t actualFps,
                           libeYs3D::video::DEPTH_RAW_DATA_TYPE depthFormat,
                           int32_t depthWidth, int32_t depthHeight,
                           DEPTH_TRANSFER_CTRL depthDataTransferCtrl,
                           CONTROL_MODE ctrlMode,
                           int rectifyLogIndex,
                           libeYs3D::video::Producer::Callback colorImageCallback,
                           libeYs3D::video::Producer::Callback depthImageCallback,
                           libeYs3D::video::PCProducer::PCCallback pcFrameCallback,
                           libeYs3D::sensors::SensorDataProducer::AppCallback imuDataCallback = nullptr) override;
    
    virtual bool isInterleaveModeSupported() override;
    
    virtual bool isIMUDeviceSupported() override   { return true; }

    virtual ~CameraDevice8059() = default;

protected:
    explicit CameraDevice8059(DEVSELINFO *devSelInfo, DEVINFORMATION *deviceInfo);

    virtual int getZDTableIndex();

    //virtual int initIMUDevice() override;
    
public:
    friend class CameraDeviceFactory;
};

} // end of namespace devices
} // end of namespace libeYs3D
