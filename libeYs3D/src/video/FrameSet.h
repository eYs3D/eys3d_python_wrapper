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

#include "video/Frame.h"
#include "video/PCFrame.h"

namespace libeYs3D {
namespace video    {

// A small structure to encapsulate frame data.
struct FrameSet    {
    struct Frame colorFrame;
    struct Frame depthFrame;
    struct PCFrame pcFrame;
};

} // namespace video
} // namespace libeYs3D
