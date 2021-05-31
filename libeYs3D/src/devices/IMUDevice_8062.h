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

#include "devices/IMUDevice.h"

namespace libeYs3D    {

namespace sensors    {
    // forward declaration
    class IMUDataProducer;
}

namespace devices    {

// forward declaration
class CameraDevice;
class CameraDevice8062;

class IMUDevice8062 : public IMUDevice    {
public:
    virtual ~IMUDevice8062();
    
    virtual const char* getName() override { return "IMUDevice 8062"; }

protected:
    IMUDevice8062(IMUDeviceInfo info, CameraDevice *cameraDevice);

    virtual std::vector<IMUDevice::IMU_DATA_FORMAT> getSupportDataFormat() override;
    virtual int selectDataFormat(IMU_DATA_FORMAT format) override;
    virtual void readDataOutputFormat() override;

public:
    friend class CameraDevice;
    friend class CameraDevice8062;
};

} // end of namespace devices
} // end of namespace libeYs3D
