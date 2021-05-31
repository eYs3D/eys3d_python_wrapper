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

#include <stdint.h>
#include "string"

namespace libeYs3D    {
namespace devices    {

// forward declaration
class CameraDevice;

struct DepthAccuracyInfo    {
    float fDistance = 0.0f;
    float fFillRate = 0.0f;
    float fZAccuracy = 0.0f;
    float fTemporalNoise = 0.0f;
    float fSpatialNoise = 0.0f;
    float fAngle = 0.0f;
    float fAngleX = 0.0f;
    float fAngleY = 0.0f;
};

class DepthAccuracyOptions    {
public:
    ~DepthAccuracyOptions() = default;

    void resetDefault();
    
    void enable(bool enable);
    bool isEnabled()    { return mEnabled; }

    void setRegionRatio(float regionRatio);
    float getRegionRatio();
    
    void setGroundTruthDistanceMM(float groundTruthDistanceMM);
    float getGroundTruthDistanceMM();
    
    int toString(char *buffer, int bufferLength) const;
    int toString(std::string &string) const;
    
    bool operator==(const DepthAccuracyOptions &rhs) const {
        return this->mEnabled == rhs.mEnabled &&
               this->mRegionRatio == rhs.mRegionRatio &&
               this->mGroundTruthDistanceMM == rhs.mGroundTruthDistanceMM;
    }

protected:
    DepthAccuracyOptions();

    bool mEnabled;
    float mRegionRatio;
    float mGroundTruthDistanceMM;

public:
    friend class CameraDevice;
};

} // end of namespace devices
} // end of namespace libeYs3D
