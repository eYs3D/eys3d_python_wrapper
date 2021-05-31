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
#include "video/FrameProducer.h"
#include "video/PCProducer.h"
#include "sensors/SensorDataProducer.h"
#include "base/synchronization/Lock.h"
#include "base/synchronization/ConditionVariable.h"
#include "utils.h"
#include "debug.h"
#include "macros.h"

#include <stdio.h>

#define DEFAULT_TIMEOUT_MS   3200
#define DEFAULT_TIMEOUT_US   3200000

namespace libeYs3D    {
namespace devices    {

class Pipeline    {
public:
    enum RESULT    {
        SYNC_ERROR = -2,
        STOPPED = -1,
        OK = 0,
        TIMEOUT,
        QUEUE_EMPTY,
        QUEUE_FULL
    };

template <typename T, size_t CAPACITY>
class CircularQueue    {
public:
    Pipeline::RESULT enQueue(const T *item, int32_t timeoutMs = DEFAULT_TIMEOUT_MS)    {
        libeYs3D::base::AutoLock lock(mLock);
        
        while(true)    {
            if(mStopped)    return RESULT::STOPPED;

            if((mRear != mFront) || (mCount == 0))    {
                mCount += 1;
                mRear = (mRear + 1) % mCapacity;
                mItems[mRear].clone(item);
            
                if(mCount == 1)    mCond.signal();
                                
                break;
            } else    { // queue full, ((mRear == mFront) && (mCount == mCapacity))
                if(timeoutMs == 0)    {
                    mFront = (mFront + 1) % mCapacity;
                    mRear = (mRear + 1) % mCapacity;
                    mItems[mRear].clone(item);

                    break;
                } else if(timeoutMs > 0)    {
#ifndef WIN32
                    if(false == mCond.timedWaitDebug(&mLock,
                                          now_in_microsecond_high_res_time_REALTIME() +
                                          (timeoutMs * 1000)))
#else
                    if(false == mCond.timedWait(&mLock,
                                          now_in_microsecond_high_res_time_REALTIME() +
                                          (timeoutMs * 1000)))
#endif
                        return RESULT::SYNC_ERROR;
                    else
                        if(mCount == mCapacity)    return Pipeline::RESULT::TIMEOUT;
                } else    { // timeoutMs < 0, wait forever
                    // instead of using mCond.wait(), checking if queue is stopped is required
#ifndef WIN32
                    if(false == mCond.timedWaitDebug(&mLock,
                                          now_in_microsecond_high_res_time_REALTIME() +
                                          DEFAULT_TIMEOUT_US))
#else
                    if(false == mCond.timedWait(&mLock,
                                          now_in_microsecond_high_res_time_REALTIME() +
                                          DEFAULT_TIMEOUT_US))
#endif
                        return RESULT::SYNC_ERROR;
                }
            }
        } // end of while(true)
        
        return RESULT::OK;
    }
    
    Pipeline::RESULT deQueue(T *item, int32_t timeoutMs = DEFAULT_TIMEOUT_MS)    {
        libeYs3D::base::AutoLock lock(mLock);
        
        if(mStopped)    return Pipeline::RESULT::STOPPED;
        
        while(mCount == 0)    {
            if(mStopped)    return Pipeline::RESULT::STOPPED;
            
            if(timeoutMs == 0)    {
                return Pipeline::RESULT::QUEUE_EMPTY;
            } else if(timeoutMs > 0)    {
#ifndef WIN32
                if(false == mCond.timedWaitDebug(&mLock,
                                      now_in_microsecond_high_res_time_REALTIME() +
                                      (timeoutMs * 1000)))
#else
                if(false == mCond.timedWait(&mLock,
                                      now_in_microsecond_high_res_time_REALTIME() +
                                      (timeoutMs * 1000)))
#endif
                    return Pipeline::RESULT::SYNC_ERROR;
                    
                if(mCount == 0)    return Pipeline::RESULT::TIMEOUT;
            } else    { // wait forever
                // instead of using mCond.wait() to check if the queue is stopped
#ifndef WIN32
                if(false == mCond.timedWaitDebug(&mLock,
                                      now_in_microsecond_high_res_time_REALTIME() +
                                      (DEFAULT_TIMEOUT_MS * 1000)))
#else
                if(false == mCond.timedWait(&mLock,
                                      now_in_microsecond_high_res_time_REALTIME() +
                                      (DEFAULT_TIMEOUT_MS * 1000)))
#endif
                    return Pipeline::RESULT::SYNC_ERROR;
            }
        }
        
        if(mCount == mCapacity)    mCond.signal();

        mCount -= 1;
        mFront = (mFront + 1) % mCapacity;
        item->clone(&mItems[mFront]);

        return Pipeline::RESULT::OK;
    }
    
    void reset()    {
        libeYs3D::base::AutoLock lock(mLock);
        
        mFront = 0;
        mRear = 0;
        mCount = 0;
    }
    
    void stop()    {
        libeYs3D::base::AutoLock lock(mLock);
        
        if(mStopped)    return;
        
        mStopped = true;
        mCond.broadcast();
    }
    
    CircularQueue(const char *name)    {
        snprintf(mName, sizeof(mName), "%s", name);
    }

    ~CircularQueue()    { stop(); }
    
private:
    char mName[128];
    T mItems[CAPACITY];
    libeYs3D::base::Lock mLock;
    libeYs3D::base::ConditionVariable mCond;
    size_t mFront = 0;
    size_t mRear = 0;
    size_t mCount = 0;
    size_t mCapacity = CAPACITY;
    
    bool mStopped = false;
};

public:
    /**
     * Retrieves and removes the head of this queue, or returns null if this queue is empty.
     * \return
     *     STOPPED: The pipeline has been stopped
     *     OK:  OK
     *     QUEUE_EMPTY: The pipeline is empty
     */
    RESULT pollColorFrame(libeYs3D::video::Frame *frame);
    RESULT pollDepthFrame(libeYs3D::video::Frame *frame);
    RESULT pollPCFrame(libeYs3D::video::PCFrame *pcFrame);
    RESULT pollIMUData(libeYs3D::sensors::SensorData *imuData);

    /**
     * Retrieves and removes the head of this queue if available.
     * If not avaiable, it waits until timeoutMs elapse
     * \param[in] timeoutMs   Max time in milliseconds to wait
     *     timeoutMs == 0: don't wait, == pull ....
     *     timeoutMs < 0: wait until a queue slot is available
     * \return
     *     STOPPED: The pipeline has been stopped
     *     OK:  OK
     *     TIMEOUT: Timeout of timeoutMs exceeded
     */
    RESULT waitForColorFrame(libeYs3D::video::Frame *frame,
                             int32_t timeoutMs = DEFAULT_TIMEOUT_MS);
    RESULT waitForDepthFrame(libeYs3D::video::Frame *frame,
                             int32_t timeoutMs = DEFAULT_TIMEOUT_MS);
    RESULT waitForPCFrame(libeYs3D::video::PCFrame *pcFrame,
                          int32_t timeoutMs = DEFAULT_TIMEOUT_MS);
    RESULT waitForIMUData(libeYs3D::sensors::SensorData *imuData,
                          int32_t timeoutMs = DEFAULT_TIMEOUT_MS);
    
    /**
     * Insert the rear of this queue if the pipe queue is not full
     * If full, it waits until timeoutMs elapse
     * \param[in] timeoutMs   Max time in milliseconds to wait
     *     timeoutMs == 0: don't wait, insert intermediately
     *     timeoutMs < 0: wait until a queue slot is available
     */
    RESULT insertColorFrame(const libeYs3D::video::Frame *frame,
                            int32_t timeoutMs = DEFAULT_TIMEOUT_MS);
    RESULT insertDepthFrame(const libeYs3D::video::Frame *frame,
                            int32_t timeoutMs = DEFAULT_TIMEOUT_MS);
    RESULT insertPCFrame(const libeYs3D::video::PCFrame *pcFrame,
                         int32_t timeoutMs = DEFAULT_TIMEOUT_MS);
    RESULT insertIMUData(const libeYs3D::sensors::SensorData *imuData,
                         int32_t timeoutMs = DEFAULT_TIMEOUT_MS);
    
    void reset();
    //void start();

    virtual ~Pipeline();

private:
    explicit Pipeline(CameraDevice *cameraDevice);
    
    void stop();

    bool colorImageCallback(const libeYs3D::video::Frame* frame);
    bool depthImageCallback(const libeYs3D::video::Frame* frame);
    bool pcFrameCallback(const libeYs3D::video::PCFrame *pcFrame);
    bool imuDataCallback(const libeYs3D::sensors::SensorData *sensorData);

private:
    CameraDevice *mCameraDevice;
    
    bool mStopped = false;
    
    libeYs3D::video::Producer::Callback mColorImageCallback;
    libeYs3D::video::Producer::Callback mDepthImageCallback;
    libeYs3D::video::PCProducer::PCCallback mPCFrameCallback;
    libeYs3D::sensors::SensorDataProducer::AppCallback mIMUDataCallback;
    
    static constexpr int kMaxFrameCount = 64; // 1 seconds @ 60FPS
    static constexpr int kMaxIMUDataCount = (kMaxFrameCount << 2);
    CircularQueue<libeYs3D::video::Frame, kMaxFrameCount> mColorFrameQueue;
    CircularQueue<libeYs3D::video::Frame, kMaxFrameCount> mDepthFrameQueue;
    CircularQueue<libeYs3D::video::PCFrame, (kMaxFrameCount >> 1)> mPCFrameQueue;
    CircularQueue<libeYs3D::sensors::SensorData, kMaxIMUDataCount> mIMUDataQueue;

public:
    friend class CameraDevice;
};

} // end of namespace devices
} // end of namespace libeYs3D
