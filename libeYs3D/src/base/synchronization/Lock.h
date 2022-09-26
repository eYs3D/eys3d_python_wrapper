// Copyright (C) 2014 The Android Open Source Project
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
 * Copyright (C) 2021 eYs3D Corporation
 * All rights reserved.
 * This project is licensed under the Apache License, Version 2.0.
 */

#pragma once

#include "base/Compiler.h"

#define ANDROID_IF_DEBUG(x)

#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN 1
#include <windows.h>
#else
#include <pthread.h>
#endif

#include <assert.h>

namespace libeYs3D    {
namespace base {

class AutoLock;
class AutoWriteLock;
class AutoReadLock;

// A wrapper class for mutexes only suitable for using in static context,
// where it's OK to leak the underlying system object. Use Lock for scoped or
// member locks.
class StaticLock {
public:
    using AutoLock = base::AutoLock;
#ifdef _WIN32
    StaticLock() { ::InitializeSRWLock(&mLock); };
#else
    constexpr StaticLock() = default;
#endif
    // Acquire the lock.
    void lock() {
#ifdef _WIN32
        ::AcquireSRWLockExclusive(&mLock);
#else
        ::pthread_mutex_lock(&mLock);
#endif
        ANDROID_IF_DEBUG(mIsLocked = true;)
    }

    bool tryLock() {
        bool ret = false;
#ifdef _WIN32
        ret = ::TryAcquireSRWLockExclusive(&mLock);
#else
        ret = ::pthread_mutex_trylock(&mLock) == 0;
#endif
        ANDROID_IF_DEBUG(mIsLocked = ret;)
        return ret;
    }

    ANDROID_IF_DEBUG(bool isLocked() const { return mIsLocked; })

    // Release the lock.
    void unlock() {
        ANDROID_IF_DEBUG(mIsLocked = false;)
#ifdef _WIN32
        ::ReleaseSRWLockExclusive(&mLock);
#else
        ::pthread_mutex_unlock(&mLock);
#endif
    }

protected:
    friend class ConditionVariable;

#ifdef _WIN32
    // Benchmarks show that on Windows SRWLOCK performs a little bit better than
    // CRITICAL_SECTION for uncontended mode and much better in case of
    // contention.
    SRWLOCK mLock = SRWLOCK_INIT;
#else
    pthread_mutex_t mLock = PTHREAD_MUTEX_INITIALIZER;
#endif
    // Both POSIX threads and WinAPI don't allow move (undefined behavior).
    DISALLOW_COPY_ASSIGN_AND_MOVE(StaticLock);

    ANDROID_IF_DEBUG(bool mIsLocked = false;)
};

// Simple wrapper class for mutexes used in non-static context.
class Lock : public StaticLock {
public:
    using StaticLock::AutoLock;

    constexpr Lock() = default;
#ifndef _WIN32
    // The only difference is that POSIX requires a deallocation function call
    // for its mutexes.
    ~Lock() { ::pthread_mutex_destroy(&mLock); }
#endif
};

class ReadWriteLock {
public:
    using AutoWriteLock = base::AutoWriteLock;
    using AutoReadLock = base::AutoReadLock;

#ifdef _WIN32
    ReadWriteLock() { ::InitializeSRWLock(&mLock); }
    ~ReadWriteLock() = default;
    void lockRead() { ::AcquireSRWLockShared(&mLock); }
    void unlockRead() { ::ReleaseSRWLockShared(&mLock); }
    void lockWrite() { ::AcquireSRWLockExclusive(&mLock); }
    void unlockWrite() { ::ReleaseSRWLockExclusive(&mLock); }

private:
    SRWLOCK mLock = SRWLOCK_INIT;
#else   // !_WIN32
    ReadWriteLock() { ::pthread_rwlock_init(&mLock, NULL); }
    ~ReadWriteLock() { ::pthread_rwlock_destroy(&mLock); }
    void lockRead() { ::pthread_rwlock_rdlock(&mLock); }
    void unlockRead() { ::pthread_rwlock_unlock(&mLock); }
    void lockWrite() { ::pthread_rwlock_wrlock(&mLock); }
    void unlockWrite() { ::pthread_rwlock_unlock(&mLock); }

private:
    pthread_rwlock_t mLock;
#endif  // !_WIN32

    friend class ConditionVariable;
    DISALLOW_COPY_ASSIGN_AND_MOVE(ReadWriteLock);
};

// Helper class to lock / unlock a mutex automatically on scope
// entry and exit.
// NB: not thread-safe (as opposed to the Lock class)
class AutoLock {
public:
    AutoLock(StaticLock& lock) : mLock(lock) { mLock.lock(); }

    AutoLock(AutoLock&& other) : mLock(other.mLock), mLocked(other.mLocked) {
        other.mLocked = false;
    }

    void lock() {
        assert(!mLocked);
        mLock.lock();
        mLocked = true;
    }

    void unlock() {
        assert(mLocked);
        mLock.unlock();
        mLocked = false;
    }

    bool isLocked() const { return mLocked; }

    ~AutoLock() {
        if (mLocked) {
            mLock.unlock();
        }
    }

private:
    StaticLock& mLock;
    bool mLocked = true;

    friend class ConditionVariable;
    // Don't allow move because this class has a non-movable object.
    DISALLOW_COPY_AND_ASSIGN(AutoLock);
};

class AutoWriteLock {
public:
    AutoWriteLock(ReadWriteLock& lock) : mLock(lock) { mLock.lockWrite(); }

    void lockWrite() {
        assert(!mWriteLocked);
        mLock.lockWrite();
        mWriteLocked = true;
    }

    void unlockWrite() {
		assert(mWriteLocked);
        mLock.unlockWrite();
        mWriteLocked = false;
    }

    ~AutoWriteLock() {
        if (mWriteLocked) {
            mLock.unlockWrite();
        }
    }

private:
    ReadWriteLock& mLock;
    bool mWriteLocked = true;
    // This class has a non-movable object.
    DISALLOW_COPY_ASSIGN_AND_MOVE(AutoWriteLock);
};

class AutoReadLock {
public:
    AutoReadLock(ReadWriteLock& lock) : mLock(lock) { mLock.lockRead(); }

    void lockRead() {
        assert(!mReadLocked);
        mLock.lockRead();
        mReadLocked = true;
    }

    void unlockRead() {
        assert(mReadLocked);
        mLock.unlockRead();
        mReadLocked = false;
    }

    ~AutoReadLock() {
        if (mReadLocked) {
            mLock.unlockRead();
        }
    }

private:
    ReadWriteLock& mLock;
    bool mReadLocked = true;
    // This class has a non-movable object.
    DISALLOW_COPY_ASSIGN_AND_MOVE(AutoReadLock);
};

}  // namespace base
}  // namespace libeYs3D
