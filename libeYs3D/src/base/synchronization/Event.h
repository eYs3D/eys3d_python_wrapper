// Copyright 2020 The Android Open Source Project
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

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

#include "base/synchronization/MessageChannel.h"

// super minimal wrapper around MessageChannel to make it less verbose to
// specify simple events and waiting on them
//
// WARNING: This does not behave like most 'event' classes; if two threads call
// wait(), then signal() will only unblock one of the threads (there's no
// 'broadcast' feature). Not to be used widely.
//
// Once you need broadcasting or anything more complicated than a single waiter
// and single signaler, please use a different method (such as plain condition
// variables with mutexes)
namespace libeYs3D    {
namespace base {

class Event {
public:
    void wait() {
        int res;
        mChannel.receive(&res);
    }

    bool timedWait(int64_t wallTimeUs) {
        auto res = mChannel.timedReceive(wallTimeUs);
        if (res) return true;
        return false;
    }

    void signal() {
        mChannel.trySend(0);
    }

private:
    MessageChannel<int, 1> mChannel;
};

}  // namespace base
}  // namespace libeYs3D
