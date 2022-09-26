/*
 * Copyright (C) 2022 eYs3D Corporation
 * All rights reserved.
 * This project is licensed under the Apache License, Version 2.0.
 */

#ifndef EYS3DPY_POSTPROCESSOPTIONS_H
#define EYS3DPY_POSTPROCESSOPTIONS_H

class PostProcessOptions {
public:

    int mSpatialFilterKernelSize = 5;          // 3 - 15 Larger smoother. This value should be in odd.
    float mSpatialFilterOutlierThreshold = 16; // 1 - 64 Smaller filter more
    int mDecimationFactor = 0;                 // Ceil(resolution / factor / 4) * 4

    int mFilteredWidth = 0;
    int mFilteredHeight = 0;

    bool mEnabled = false;

    PostProcessOptions() : PostProcessOptions(5, 16.0f, 1) { }

    PostProcessOptions(const int spatialKernelSize, const float spatialOutlierThreshold, const int decimationFactor) {
        mSpatialFilterKernelSize = spatialKernelSize;
        mSpatialFilterOutlierThreshold = spatialOutlierThreshold;
        mDecimationFactor = decimationFactor;
    }

    void setSpatialFilterKernelSize (const int spatialKernelSize) {
        mSpatialFilterKernelSize = spatialKernelSize;
    }

    inline int getSpatialFilterKernelSize () const {
        return mSpatialFilterKernelSize;
    }

    void setSpatialOutlierThreshold(const float spatialOutlierThreshold) {
        mSpatialFilterOutlierThreshold = spatialOutlierThreshold;
    }

    inline float getSpatialOutlierThreshold () const {
        return mSpatialFilterOutlierThreshold;
    }

    /**
     * Set current resolution divisor. Set before Camera::initStream and after initStream is completed.
     * Developer might invoke getFilteredHeight() / getFilteredWidth() to know the resized resolution.
     */
    void setDecimationFactor(unsigned short factor) {
        mDecimationFactor = factor;
    }
    /**
     * Get current resolution divisor. It won't affect anything when streaming.
     * @return current decimation factor.
     */
    inline int getDecimationFactor () const {
        return mDecimationFactor;
    }

    /**
     *  This value will be filled after Camera::initStream, ceil(width / DecimationFactor / 4) * 4
     *  e.g. ceil(1280 / 3 / 4) * 4 = 428
     *  And will be the same as Frame::width
     * @return Decimation filter resized width.
     */
    inline int getFilteredWidth () const {
        return mFilteredWidth;
    }

    /**
     *  This value will be filled after Camera::initStream. And will be the same as Frame::height.
     * @return Decimation filter resized height.
     */
    inline int getFilteredHeight () const {
        return mFilteredHeight;
    }

    /**
     * Control over depth post process filter enablement. Could be switched when device is streaming.
     * @param enable
     */
    void enable(const bool enable) {
        mEnabled = enable;
    }

    inline bool isEnabled() const {
        return mEnabled;
    }

    /**
     *
     * @param w Internal updated by CameraDevice, which inform user currently decimation height.
     * @return
     */
    inline void setFilteredWidth (int w) {
        mFilteredWidth = w;
    }

    /**
     *
     * @param h Internal updated by CameraDevice, which inform user currently decimation height.
     * @return
     */
    inline void setFilteredHeight (int h) {
        mFilteredHeight = h;
    }
};

#endif //EYS3DPY_POSTPROCESSOPTIONS_H
