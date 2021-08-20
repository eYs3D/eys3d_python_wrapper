import os
import sys

import argparse
import time
from datetime import datetime
import cv2
import numpy as np

from eys3d import FrameSetPipeline, Config
from eys3d import LIGHT_SOURCE_VALUE
from eys3d import logger
from eys3d.utils import get_EYS3D_HOME


class RecordStream:
    """Record stream based on eys3d module

    It will start stream through eys3d pipeline.
    Two streams (color and depth) will be open together 
    and then will be concatenated into a new frame
    New frame size will be adjusted to (W * 2 * ratio^2, H * ratio) in order to fit the screen size
    All the stream will be saved into "temp.mp4" and ready for playback.
    Bellow guide provides for control the playback:


    Args:
        pipe            (:obj:`class`)  : The eys3d pipeline class
        tempFilename    (str)           : The filename for saved video
        width           (int)           : Width for pipeline stream
        height          (int)           : Height for pipeline stream 
        record          (bool)          : True for record, otherwise is False
        ratio           (float)         : For adjusting concatenated frame size.


    Usage:
        Hot Keys:
            Space       : Play/Pause
            Q/q/Esc     : Quit
            W/w         : Enable/Disable auto white balance
            E/e         : Enable/Disable auto exposure
            R/r         : Enable/Disable low light compensation
            T/t         : light source switch (50Hz / 60Hz)
            .           : Increase white balance temperature (+ 100)
            ,           : Decrease white balance temperature (- 100)
            L/l         : Increase exposure time (+ 1.0)
            K/l         : Decrease exposure time (- 1.0)
            1 ~ 8       : Set manual global gain from 1 ~ 8.
            <F6>        : Dump camera properties info
            <F9>        : Set manual exposure time = 0.3 for test.
            <F10>       : Set manual exposure time = 5 for test.
            <F11>       : Set manual exposure time = 20 for test.
            <F12>       : Set manual exposure time = 30 for test.

    Note:
        1. The range of white balance is 2800 ~ 6500.
        2. The range of exposure time is (-13 ~ 3).
        3. AWB/AE needs to be disabled if you want to adjust white balance temperature / exposure time.
    """
    def __init__(self,
                 pipe,
                 tempFilename='temp.mp4',
                 width=1280,
                 height=720,
                 record=True,
                 ratio=0.75):
        # self.cap = cv2.VideoCapture(0)
        # self.check_camera_is_opened()
        self.record = record
        self.pipe = pipe
        self.width = width
        self.height = height
        self.tempFilename = tempFilename
        self.ratio = ratio
        if self.record:
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            self.out = cv2.VideoWriter(self.tempFilename, fourcc, 24.0,
                                       (int(self.width * 2 * self.ratio**2),
                                        int(self.height * self.ratio)))
        self.dev = self.pipe.get_device()

        # Initial module property
        self.__camera_property = self.dev.get_cameraProperty()

    @logger.catch()
    def get_frame(self):
        """The function for getting frame from pipeline.

        The function to get frame from eys3d pipeline and
        then concatenated color and depth frame into new frame to cv2.imshow.
        New frame size is (W * 2 * ratio^2, H).
        """
        ret, frameset = self.pipe.wait_frameset()
        if not ret:
            return False, None
        try:
            cframe = frameset.color_frame
            dframe = frameset.depth_frame
            color_rgb_image = cframe.get_rgb_data().reshape(
                cframe.get_height(), cframe.get_width(), 3)
            depth_rgb_image = dframe.get_rgb_data().reshape(
                dframe.get_height(), dframe.get_width(), 3)
            cframe_bgr = cv2.cvtColor(color_rgb_image, cv2.COLOR_RGB2BGR)
            dframe_bgr = cv2.cvtColor(depth_rgb_image, cv2.COLOR_RGB2BGR)
            if cframe_bgr.shape != dframe_bgr.shape:
                dframe_bgr = cv2.resize(dframe_bgr, (self.width, self.height),
                                        interpolation=cv2.INTER_AREA)
            frame = np.hstack((cframe_bgr, dframe_bgr))
            frame_resized = cv2.resize(frame,
                                       (int(self.width * 2 * self.ratio**2),
                                        int(self.height * self.ratio)))
            if self.record:
                self.out.write(frame_resized)
            return True, frame_resized
        except TypeError:
            logger.exception(TypeError)
            pass

    def show(self):
        """The function to show frame through openCV.

        These demo the property of eys3d module.
        Please refer usage for operation in detail.
        """
        # Initial status
        status = 'play'

        # Flag defined
        flag = dict({
            'wb':
            bool(self.__camera_property.get_AWB_status()),
            'exposure':
            bool(self.__camera_property.get_AE_status()),
            'low_light':
            bool(self.__camera_property.get_low_light_compensation_status()),
            'light_source':
            True if self.__camera_property.get_light_source_status()
            == LIGHT_SOURCE_VALUE.VALUE_50HZ else False
        })
        logger.info(
            "\n\tAuto White Balance:\t\t{0}\n\tWhite Balance Temperature:\t{1}\n\tAuto Exposure:\t\t\t{2}\n\tExposure time:\t\t\t{3}\n\tLow Light Compensation:\t\t{4}\n\tLight Source:\t\t\t{5} Hz\n"
            .format(flag['wb'],
                    self.__camera_property.get_white_balance_temperature(),
                    flag['exposure'],
                    self.__camera_property.get_exposure_value(),
                    flag['low_light'], 50 if flag['light_source'] else 60))
        while 1:
            try:
                ret, frame = self.get_frame()
                if ret == True:
                    cv2.imshow("Frame", frame)
                status = {
                    ord(' '): 'pause',
                    ord('q'): 'exit',
                    ord('Q'): 'exit',
                    ord('W'): 'white_balance',
                    ord('w'): 'white_balance',
                    ord('E'): 'exposure',
                    ord('e'): 'exposure',
                    ord('R'): 'low_light_compensation',
                    ord('r'): 'low_light_compensation',
                    ord('T'): 'light_source',
                    ord('t'): 'light_source',
                    195: 'dump_camera_properties',
                    198: 'exposure_time_1',  # F9 exposure time = 0.3
                    199: 'exposure_time_2',  # F10 exposure time = 5
                    200: 'exposure_time_3',  # F11 exposure time = 20
                    201: 'exposure_time_4',  # F12 exposure time = 30
                    ord('1'): 'global_gain_1',  # global gain = 1
                    ord('2'): 'global_gain_2',  # global gain = 2
                    ord('3'): 'global_gain_3',  # global gain = 3
                    ord('4'): 'global_gain_4',  # global gain = 4
                    ord('5'): 'global_gain_5',  # global gain = 5
                    ord('6'): 'global_gain_6',  # global gain = 6
                    ord('7'): 'global_gain_7',  # global gain = 7
                    ord('8'): 'global_gain_8',  # global gain = 8
                    ord('.'): 'increase_wb_temperature',
                    ord(','): 'decrease_wb_temperature',
                    ord('L'): 'increase_exposure_value',
                    ord('l'): 'increase_exposure_value',
                    ord('K'): 'decrease_exposure_value',
                    ord('k'): 'decrease_exposure_value',
                    -1: status,
                    27: 'exit',
                }[cv2.waitKey(10)]
            except (KeyError, TypeError):
                continue
            if status is 'play':
                pass
            if status is 'pause':
                cv2.waitKey()
                status = 'play'
            if status is 'white_balance':
                flag['wb'] = not (flag['wb'])
                if flag['wb']:
                    self.__camera_property.enable_AWB()
                else:
                    self.__camera_property.disable_AWB()
                    temperature = self.__camera_property.get_white_balance_temperature(
                    )
                    self.__camera_property.set_white_balance_temperature(
                        temperature)
                time.sleep(0.1)
                logger.info("Auto white balance status is {}".format(
                    (bool(self.__camera_property.get_AWB_status()))))
                status = 'play'
            if status is 'exposure':
                flag['exposure'] = not (flag['exposure'])
                if flag['exposure']:
                    self.__camera_property.enable_AE()
                else:
                    self.__camera_property.disable_AE()
                    exposure_value = self.__camera_property.get_exposure_value(
                    )
                    self.__camera_property.set_exposure_value(exposure_value)
                time.sleep(0.1)
                logger.info("Auto exposure status is {}".format(
                    (bool(self.__camera_property.get_AE_status()))))
                status = 'play'
            if status is 'low_light_compensation':
                flag['low_light'] = not (flag['low_light'])
                if flag['low_light']:
                    self.__camera_property.enable_low_light_compensation()
                else:
                    self.__camera_property.disable_low_light_compensation()
                logger.info("Low light compensation status is {}".format(
                    bool(self.__camera_property.
                         get_low_light_compensation_status())))
                status = 'play'
            if status is 'light_source':
                flag['light_source'] = not (flag['light_source'])
                if flag['light_source']:
                    self.__camera_property.set_light_source(
                        LIGHT_SOURCE_VALUE.VALUE_50HZ)  # 50 hz
                else:
                    self.__camera_property.set_light_source(
                        LIGHT_SOURCE_VALUE.VALUE_60HZ)  # 60 hz
                logger.info("Light source is {} Hz".format(
                    50 if self.__camera_property.get_light_source_status() ==
                    LIGHT_SOURCE_VALUE.VALUE_50HZ else 60))
                status = 'play'
            if status is 'increase_wb_temperature':
                if not flag['wb']:
                    temperature = self.__camera_property.get_white_balance_temperature(
                    )
                    temperature = min(6500, temperature + 100)
                    self.__camera_property.set_white_balance_temperature(
                        temperature)
                    logger.info(
                        "White balance temperature is {}".format(temperature))
                else:
                    logger.info("Please disable auto white balance.")
                status = 'play'

            if status is 'decrease_wb_temperature':
                if not flag['wb']:
                    temperature = self.__camera_property.get_white_balance_temperature(
                    )
                    temperature = max(2800, temperature - 100)
                    self.__camera_property.set_white_balance_temperature(
                        temperature)
                    logger.info(
                        "White balance temperature is {}".format(temperature))
                else:
                    logger.info("Please disable auto white balance.")
                status = 'play'
                pass

            if status is 'increase_exposure_value':
                if not flag['exposure']:  # disable auto exposure
                    exposure_value = self.__camera_property.get_exposure_value(
                    )
                    exposure_value = min(3, exposure_value + 1)
                    self.__camera_property.set_exposure_value(exposure_value)
                    logger.info(
                        "Current exposure value is {}".format(exposure_value))
                else:
                    logger.info("Please disable auto exposure.")
                status = 'play'

            if status is 'decrease_exposure_value':
                if not flag['exposure']:  # disable auto exposure
                    exposure_value = self.__camera_property.get_exposure_value(
                    )
                    logger.info(
                        "Current exposure value is {}".format(exposure_value))
                    exposure_value = max(-13, (exposure_value - 1))
                    self.__camera_property.set_exposure_value(exposure_value)
                    logger.info(
                        "Current exposure value is {}".format(exposure_value))
                else:
                    logger.info("Please disable auto exposure.")
                status = 'play'

            if status is 'exposure_time_1':
                if not flag['exposure']:  # disable auto exposure
                    exposure_time = 0.3
                    self.__camera_property.set_manual_exposure_time(
                        exposure_time)
                    logger.info("Set manaul exposure time = {}".format(
                        self.__camera_property.get_manual_exposure_time()))
                else:
                    logger.info("Please disable auto exposure.")
                status = 'play'

            if status is 'exposure_time_2':
                if not flag['exposure']:  # disable auto exposure
                    exposure_time = 5
                    self.__camera_property.set_manual_exposure_time(
                        exposure_time)
                    logger.info("Set manaul exposure time = {}".format(
                        self.__camera_property.get_manual_exposure_time()))
                else:
                    logger.info("Please disable auto exposure.")
                status = 'play'

            if status is 'exposure_time_3':
                if not flag['exposure']:  # disable auto exposure
                    exposure_time = 20
                    self.__camera_property.set_manual_exposure_time(
                        exposure_time)
                    logger.info("Set manaul exposure time = {}".format(
                        self.__camera_property.get_manual_exposure_time()))
                else:
                    logger.info("Please disable auto exposure.")
                status = 'play'

            if status is 'exposure_time_4':
                if not flag['exposure']:  # disable auto exposure
                    exposure_time = 30
                    self.__camera_property.set_manual_exposure_time(
                        exposure_time)
                    logger.info("Set manaul exposure time = {}".format(
                        self.__camera_property.get_manual_exposure_time()))
                else:
                    logger.info("Please disable auto exposure.")
                status = 'play'

            if 'global_gain' in status:
                gain = status[-1]
                if not flag['exposure']:  # disable auto exposure
                    self.__camera_property.set_manual_global_gain(float(gain))
                    logger.info("Set mamual global gain = {}".format(
                        self.__camera_property.get_manual_global_gain()))
                else:
                    logger.info("Please disable auto exposure.")
                status = 'play'
            if status is 'dump_camera_properties':
                self.dev.dump_camera_device_properties()
                logger.info("Dump camera properties")
                status = 'play'
            if status is 'exit':
                cv2.destroyWindow('Frame')
                break
        if self.record:
            self.out.release()

    def playback(self):
        """Playback the record file throught another class.

        Please refer PlaybackStream description in detail.
        """
        self.playback_stream = PlaybackStream(self.tempFilename, 24)
        self.playback_stream.playback()
        self.playback_stream.release()

    def release(self):
        """Release the device.

        Release the device safety.
        """
        self.pipe.stop()


class PlaybackStream:
    """Class for playback previous recored file

    Class for playback stream demo.
    It designed based on OpenCV.
    
    Usage:
        Hot Keys:
            Space       : Play/Pause
            Q/q/Esc     : Quit
            F/f         : Increase fps
            S/s         : Decrease fps
            Right Arrow : Next frame
            Left Arror  : Previous frame

    Note: Range of frame speed is 0.5 ~ 2.0.
    """
    def __init__(self, inputFilename="temp.mp4", frame_rate=None):
        self.cap = cv2.VideoCapture(inputFilename)
        self.total_of_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.base_frame_rate = self.cap.get(
            cv2.CAP_PROP_FPS) if frame_rate is None else frame_rate
        self.speed = 1.0
        self.frame_rate = self.base_frame_rate

    def playback(self):
        logger.info("Start to playback")
        i = 0
        # Initial status
        status = 'play'
        # Flag defined
        play_flag = True

        prev_time = 0
        time_elapsed = 1. / self.frame_rate
        font = cv2.FONT_HERSHEY_SIMPLEX

        if self.cap.isOpened() is False:
            raise Exception("Device not found.")
        ret, frame = self.cap.read()
        while ret:
            if i >= self.total_of_frames - 1:
                i = 0
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = self.cap.read()
            #cv2.putText(frame, str(self.speed), (3, 30), font, 1, (0, 255, 255, 0.5), 1, cv2.LINE_AA)
            cv2.imshow("Playback", frame)
            time_elapsed = time.time() - prev_time

            try:
                status = {
                    ord(' '): 'pause',
                    ord('q'): 'exit',
                    ord('Q'): 'exit',
                    ord('f'): 'fast',
                    ord('F'): 'fast',
                    ord('s'): 'slow',
                    ord('S'): 'slow',
                    83: 'next_frame',
                    81: 'prev_frame',
                    -1: status,
                    27: 'exit',
                }[cv2.waitKey(int(1 / self.frame_rate * 1000))]
            except KeyError:
                continue
            if status is 'stay':
                play_flag = False
                continue
            if status is 'pause':
                play_flag = not (play_flag)
                status = 'play'
            if status is 'play':
                if ret and time_elapsed >= 1. / self.frame_rate:
                    prev_time = time.time()
                if play_flag:
                    # time.sleep((0.1 - self.frame_rate/1000.0)**21021)
                    i += 1
                continue
            if status is 'fast':
                self.speed = min(2, self.speed + 0.25)
                self.frame_rate = min(120.0, self.base_frame_rate * self.speed)
                logger.info("Speed: {}, frame rate: {}".format(
                    self.speed, self.frame_rate))
                #cv2.putText(frame, str(self.speed), (3, 30), font, 1, (0, 255, 255, 0.5), 1, cv2.LINE_AA)
                cv2.imshow("Playback", frame)
                status = 'stay'
            if status is 'slow':
                self.speed = max(0.5, self.speed - 0.25)
                self.frame_rate = max(3.0, self.base_frame_rate * self.speed)
                logger.info("Speed: {}, frame rate: {}".format(
                    self.speed, self.frame_rate))
                #cv2.putText(frame, str(self.speed), (3, 30), font, 1, (0, 255, 255, 0.5), 1, cv2.LINE_AA)
                cv2.imshow("Playback", frame)
                status = 'stay'
            if status is 'next_frame':
                i = min(self.total_of_frames, i + 5)
                status = 'stay'
            if status is 'prev_frame':
                i = max(0, i - 5)
                status = 'stay'
            if status is 'exit':
                self.release()
                cv2.destroyWindow("Playback")
                break

    def release(self):
        self.cap.release()


def record_playback_sample(device, config):

    while 1:
        record = input("Do you want to record video(True/False)?: ")
        if record in ("True", "true", "T", "t"):
            record = True
            EYS3D_HOME = get_EYS3D_HOME()
            savedFilename = os.path.join(
                EYS3D_HOME, "video_recording", "record-{}.mp4".format(
                    datetime.now().strftime("%m%d-%H:%M:%S")))
            logger.info("Recored file: {}.".format(savedFilename))
            break
        elif record in ("False", "false", "F", "f"):
            record = False
            savedFilename = "temp.mp4"
            logger.info("Should be recorded file? {}.".format(record))
            break

    pipe = FrameSetPipeline(device=device)
    conf = config
    # Getting size from config
    height_color_frame, width_color_frame = conf.get_color_stream_resolution()
    height_depth_frame, width_depth_frame = conf.get_depth_stream_resolution()
    pipe.start(conf)
    # Enable interleave if interleave mode
    pipe.reset()
    stream = RecordStream(pipe,
                          record=record,
                          width=width_color_frame,
                          height=height_color_frame,
                          tempFilename=savedFilename)
    stream.show()  # Preview and recorded
    if record == True:
        stream.playback()  # Playback recorded file
    stream.release()
