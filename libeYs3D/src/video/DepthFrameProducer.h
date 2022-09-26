/*
 * Copyright (C) 2021 eYs3D Corporation
 * All rights reserved.
 * This project is licensed under the Apache License, Version 2.0.
 */

#pragma once

#include <stdint.h>                                   // for uint32_t, uint8_t
#include <memory>                                     // for unique_ptr
#include <list>

#include "video/FrameProducer.h"
#include "devices/CameraDevice.h"
#include "coders.h"
#include "PostProcessOptions.h"

namespace libeYs3D    {
namespace video    {

class DACalculateWorkItem    {
public:
    std::function<void(Frame *)> callback;
    Frame *frame;

public:
    DACalculateWorkItem(std::function<void(Frame *)> cb, Frame *frame)    {
        this->callback = cb;
        this->frame = frame;
    }

    ~DACalculateWorkItem()    {}
};
/**
 * This helper class allocate a temporary buffer as output of filter.
 */
class PostProcessHandle {
public:
    using PostProcessHandleCallback = std::function<int(bool)>;

private:
    std::vector<unsigned char> mCachedDepthBuffer;
    APCImageType::Value mCurrentImageType;
    void* mPostProcessHandle = nullptr;
    PostProcessOptions& mOptions;
    const size_t mWidth;
    const size_t mHeight;

    void* mDecimationHandle = nullptr;
    std::vector<unsigned char> mCachedDecimationBuffer;
    int32_t mDecimatedWidth = 0;
    int32_t mDecimatedHeight = 0;
    PostProcessHandleCallback& mCallback;
    bool mIsEnable;

public:
    PostProcessHandle(int32_t width, int32_t height, APCImageType::Value imageType,
                      PostProcessOptions& postProcessOptions, PostProcessHandleCallback& cb) :
        mDecimatedWidth(width), mDecimatedHeight(height),
        mCurrentImageType(imageType),
        mOptions(postProcessOptions),
        mWidth(width), mHeight(height), mCallback(cb), mIsEnable(postProcessOptions.isEnabled()) {
#ifndef WIN32
        DECIMATION_PARAMS decimationParams {
            .decimation_sub_sample_factor = mOptions.getDecimationFactor()
        };

        POST_PROCESS_PARAMS params {
            .spatial_filter_kernel_size = mOptions.getSpatialFilterKernelSize(),
            .spatial_filter_outlier_threshold = mOptions.getSpatialOutlierThreshold()
        };

        APC_InitDecimationFilter(&mDecimationHandle, mWidth, mHeight, (unsigned int*) &mDecimatedWidth,
                                 (unsigned int*) &mDecimatedHeight, imageType, decimationParams);

        APC_InitPostProcessCustomParameter(&mPostProcessHandle, mWidth, mHeight, imageType, params);
#endif
        size_t bufferSize = mWidth * mHeight * get_depth_image_format_byte_length_per_pixel(mCurrentImageType);
        mCachedDecimationBuffer.resize(bufferSize);
        mCachedDecimationBuffer.clear();
        mCachedDepthBuffer.resize(bufferSize);
        mCachedDepthBuffer.clear();
        mOptions.setFilteredWidth(getFilteredWidth());
        mOptions.setFilteredHeight(getFilteredHeight());
    }

    inline int32_t getFilteredWidth() const {
        return mIsEnable ? (int32_t) mDecimatedWidth : (int32_t) mWidth;;
    }

    inline int32_t getFilteredHeight() const {
        return mIsEnable ? (int32_t) mDecimatedHeight : (int32_t) mHeight;
    }

    inline void notifyCameraIfNeeded() {
        if (mIsEnable == mOptions.isEnabled()) return;

        mIsEnable = mOptions.isEnabled();
        mCallback(true);
    }

    inline int process(Frame* f) {
#ifndef WIN32
        const int32_t width = getFilteredWidth();
        const int32_t height = getFilteredHeight();

        f->width = width;
        f->height = height;
        f->processedBufferSize = width * height * get_depth_image_format_byte_length_per_pixel(mCurrentImageType);
        mOptions.setFilteredHeight(width);
        mOptions.setFilteredWidth(height);

        if (!mOptions.isEnabled()) {
            notifyCameraIfNeeded();
            return APC_POSTPROCESS_NOT_INIT;
        }

        if (f->dataVec.capacity() != mCachedDepthBuffer.capacity()) {
            LOG_WARN("PostProcessHandle", "Process mCachedDepthBuffer != sizeof inBuffer should not happen.");
            mCachedDepthBuffer.resize(f->dataVec.capacity());
        }

        int ret = APC_DecimationFilter(mDecimationHandle, f->dataVec.data(), mCachedDecimationBuffer.data(),
                                       mCurrentImageType);

        if (mCachedDecimationBuffer.capacity() != mCachedDepthBuffer.capacity()) {
            LOG_WARN("PostProcessHandle", "Process mCachedDepthBuffer != sizeof inBuffer should not happen.");
            mCachedDepthBuffer.resize(mCachedDecimationBuffer.capacity());
        }

        /**
         * Caution!! If put inBuffer as input and output. The result will totally wrong. (Last version could do.)
         */
        ret = APC_PostProcess(mPostProcessHandle, mCachedDecimationBuffer.data(), mCachedDepthBuffer.data(),
                              mCurrentImageType);

        mCachedDepthBuffer.swap(f->dataVec);

        notifyCameraIfNeeded();
        return ret;
#else
        return APC_NotSupport;
#endif
    }

    ~PostProcessHandle() {
#ifndef WIN32
        APC_ReleasePostProcess(mPostProcessHandle);
        APC_ReleaseDecimationFilter(mDecimationHandle);
#endif
        mPostProcessHandle = nullptr;
        mDecimationHandle = nullptr;
    }
};

class DepthFrameProducer : public FrameProducer    {
public:
    friend std::unique_ptr<FrameProducer> createDepthFrameProducer(CameraDevice *cameraDevice);
    
    virtual const char* getName() override    { return "DepthFrameProducer"; }
    virtual ~DepthFrameProducer() override;

protected:
    DepthFrameProducer(CameraDevice *cameraDevice);

    virtual int getRawFormatBytesPerPixel(uint32_t format) override;
    virtual int readFrame(Frame *frame) override;
    virtual int performPostProcessFilter(Frame *frame) override;
    int getFilteredWidth() override;
    int getFilteredHeight() override;
    virtual int produceRGBFrame(Frame *frame) override;
    virtual int performFiltering(Frame *frame) override;
    virtual int performInterleave(Frame *frame) override;
    virtual int performAccuracyComputation(Frame *frame) override;
    virtual int performROIComputation(Frame *frame) override;
    
    virtual void checkIMUDeviceCBEnablement() override;

    virtual void performSnapshotWork(Frame *frame) override;

    virtual void logProducerTick(const char *FMT, ...) override;
    int m_nLastInterLeaveDepthSerial;
    
protected:
    void virtual attachReaderWorkerCGgroup() override;
    void virtual attachRGBWorkerCGgroup() override;
    void virtual attachFilterWorkerCGgroup() override;
    void virtual attachCallbackWorkerCGgroup() override;
    
private:
    libeYs3D::base::Lock mLock;
    std::vector<uint16_t> mTableZ14ToD11;
    std::vector<uint16_t> mZ14ToD11;
    
    std::list<std::vector<int16_t>> mDepthList; // for calculateDepthTemporalNoise
    PostProcessHandle mPostProcessHandle;
    PostProcessHandle::PostProcessHandleCallback mPostProcessCameraParamsUpdateCallback;
    libeYs3D::base::ThreadPool<DACalculateWorkItem> mDACalculateThreadPool;
    libeYs3D::base::MessageChannel<int, 3> mFinishSignalForAccuracy;
    libeYs3D::base::MessageChannel<int, 1> mFinishSignalForROI;
    std::function<void(Frame *)> mCalculateDepthAccuracyInfo;
    std::function<void(Frame *)> mCalculateDepthSpatialNoise;
    std::function<void(Frame *)> mCalculateDepthTemporalNoise;
    //std::function<void(Frame *)> mCalculateROIComputation;
    
    void calculateDepthAccuracyInfo(Frame *frame);
    void calculateDepthSpatialNoise(Frame *frame);
    void calculateDepthTemporalNoise(Frame *frame);
    //void calculateROIComputation(Frame *frame);

    bool mIsFinishedForAccuracy;
    int mMessageCountForAccuracy;
    libeYs3D::video::Frame mFrameForAccuracy;
    libeYs3D::video::Frame mFrameTempForAccuracy;
    int64_t mCurrentTimeForAccuracy;
    int64_t mNewTimeForAccuracy;
    int mSignalControlForAccuracy;
    std::vector< WORD > GetDepthZOfROI(Frame *frame , int &nWidth, int &nHeight);
    void CalculateFittedPlane(double &a, double &b, double &d,
                              std::vector< WORD > &vecDepthZ, int nWidth , int nHeigth);
    void SortZ(std::vector< WORD > &vecDepthZ, double dblDeleteBoundaryRatio = 0.005);
    std::vector< double > vectorCrossProduct(std::vector< double > vecBefore , std::vector< double > vecAfter);
    double vectorDotProduct(std::vector< double > vecBefore , std::vector< double > vecAfter);


    double CalculateZAccuracy(std::vector< WORD > &vecDepthZ,
                                                 int nWidth, int nHeight,
                                                 double grandtrue,
                                                 double m_fDepthAccuracyDistanceMM,
                                                 std::vector< double > vecBefore, std::vector< double > vecAfter);
    //int mSignalMessageForAccuracy;

    //bool mIsFinishedForROI;
    //int mMessageCountForROI;
    //libeYs3D::video::Frame mFrameForROI;
    //libeYs3D::video::Frame mFrameTempForROI;
    //int64_t mCurrentTimeForROI;
    //int64_t mNewTimeForROI;
    //int mSignalControlForROI;
    //int mSignalMessageForROI;


};  // class FrameProducer

}  // namespace video
}  // namespace libeYs3D
